"""Train a baseline fraud classifier and evaluate a later time period."""
import argparse, json
from pathlib import Path
import duckdb, joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, roc_auc_score, average_precision_score

NUM=["amount","oldbalanceOrg","oldbalanceDest","org_txn_prior_24h","org_amount_prior_24h"]
CAT=["type"]
FEATURES=NUM+CAT

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    frame=duckdb.connect().execute("SELECT * FROM read_parquet(?) ORDER BY step",[str(Path(a.input).resolve())]).df()
    # Chronological holdout: earlier 80% of time for fit, later period for evaluation.
    cutoff=frame.step.quantile(.8)
    train=frame[frame.step<=cutoff]; test=frame[frame.step>cutoff]
    pre=ColumnTransformer([
      ("num",make_pipeline(SimpleImputer(strategy="median"),StandardScaler()),NUM),
      ("cat",OneHotEncoder(handle_unknown="ignore"),CAT)])
    model=make_pipeline(pre,LogisticRegression(max_iter=300,class_weight="balanced"))
    model.fit(train[FEATURES],train.isFraud)
    score=model.predict_proba(test[FEATURES])[:,1]
    y=test.isFraud.to_numpy()
    # Compare thresholds and the existing simulator rule at the same holdout.
    rows=[]
    for threshold in (.10,.25,.50,.75):
      pred=score>=threshold
      rows.append({"strategy":f"model_{threshold:.2f}","threshold":threshold,"alerts":int(pred.sum()),
        "alert_rate":float(pred.mean()),"precision":float(precision_score(y,pred,zero_division=0)),
        "recall":float(recall_score(y,pred,zero_division=0)),
        "fraud_amount_captured":float(test.loc[pred,"amount"].where(test.loc[pred,"isFraud"].eq(1),0).sum()),
        "legitimate_alerts":int(((pred)&(y==0)).sum())})
    baseline=test.isFlaggedFraud.astype(bool).to_numpy()
    rows.append({"strategy":"existing_simulator_flag","threshold":None,"alerts":int(baseline.sum()),
      "alert_rate":float(baseline.mean()),"precision":float(precision_score(y,baseline,zero_division=0)),
      "recall":float(recall_score(y,baseline,zero_division=0)),
      "fraud_amount_captured":float(test.loc[baseline,"amount"].where(test.loc[baseline,"isFraud"].eq(1),0).sum()),
      "legitimate_alerts":int(((baseline)&(y==0)).sum())})
    metrics={"train_rows":len(train),"test_rows":len(test),"time_cutoff":float(cutoff),
      "roc_auc":float(roc_auc_score(y,score)),"average_precision":float(average_precision_score(y,score)),
      "strategies":rows}
    (out/"evaluation.json").write_text(json.dumps(metrics,indent=2))
    joblib.dump(model,out/"fraud_model.joblib")
    test[["step","type","amount","isFraud","isFlaggedFraud"]].assign(predicted_fraud_probability=score).to_parquet(out/"scored_test.parquet",index=False)
    print(json.dumps(metrics,indent=2))
if __name__=="__main__": main()

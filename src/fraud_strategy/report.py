"""Create hourly and transaction-type monitoring summaries."""
import argparse
from pathlib import Path
import duckdb

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    con=duckdb.connect(); path=str(Path(a.input).resolve()).replace("'","''")
    for name,sql in {
      "hourly_strategy_monitoring.csv":"""SELECT step,COUNT(*) transaction_count,SUM(amount) transaction_amount,
        SUM(isFraud) fraud_count,SUM(CASE WHEN isFraud=1 THEN amount ELSE 0 END) fraud_amount,
        SUM(isFlaggedFraud) flagged_count FROM read_parquet('{p}') GROUP BY step ORDER BY step""",
      "segment_baseline.csv":"""SELECT type,COUNT(*) transaction_count,SUM(amount) transaction_amount,
        SUM(isFraud) fraud_count,SUM(CASE WHEN isFraud=1 THEN amount ELSE 0 END) fraud_amount,
        AVG(isFraud::DOUBLE) fraud_rate,SUM(isFlaggedFraud) flagged_count
        FROM read_parquet('{p}') GROUP BY type ORDER BY fraud_amount DESC"""
    }.items():
      con.execute(sql.format(p=path)).df().to_csv(out/name,index=False)
    print(f"Reports written to {out}")
if __name__=="__main__": main()

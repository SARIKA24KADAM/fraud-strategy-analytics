"""Prepare PaySim data and point-in-time account activity features with DuckDB."""
import argparse
from pathlib import Path
import duckdb

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    # account-history windows exclude current row; post-event fields and IDs are not predictors.
    con=duckdb.connect()
    source=str(Path(a.input).resolve()).replace("'","''")
    target=str(Path(a.output).resolve()).replace("'","''")
    con.execute(f"""
      COPY (
        SELECT step, type, amount, oldbalanceOrg, oldbalanceDest,
               isFraud, isFlaggedFraud,
               COALESCE(org_txn_prior_24h,0) AS org_txn_prior_24h,
               COALESCE(org_amount_prior_24h,0) AS org_amount_prior_24h
        FROM (
          SELECT *,
            COUNT(*) OVER (
              PARTITION BY nameOrig ORDER BY CAST(step AS INTEGER)
              RANGE BETWEEN 24 PRECEDING AND 1 PRECEDING
            ) AS org_txn_prior_24h,
            SUM(amount) OVER (
              PARTITION BY nameOrig ORDER BY CAST(step AS INTEGER)
              RANGE BETWEEN 24 PRECEDING AND 1 PRECEDING
            ) AS org_amount_prior_24h
          FROM read_csv_auto('{source}', header=true)
        )
      ) TO '{target}' (FORMAT PARQUET)
    """)
    print(f"Wrote point-in-time features to {target}")
if __name__=="__main__": main()

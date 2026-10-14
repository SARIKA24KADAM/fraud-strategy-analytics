-- DuckDB queries. Run from repository root after preparing features.parquet.
SELECT type, COUNT(*) AS transaction_count, SUM(amount) AS transaction_amount,
       SUM(isFraud) AS fraud_count,
       SUM(CASE WHEN isFraud=1 THEN amount ELSE 0 END) AS fraud_amount,
       AVG(isFraud::DOUBLE) AS fraud_rate
FROM read_parquet('data/processed/features.parquet')
GROUP BY type ORDER BY fraud_amount DESC;

-- Hourly simulator rule monitoring; isFlaggedFraud is a comparator only.
SELECT step, COUNT(*) AS transaction_count, SUM(amount) AS transaction_amount,
       SUM(isFraud) AS fraud_count, SUM(isFlaggedFraud) AS flagged_count
FROM read_parquet('data/processed/features.parquet')
GROUP BY step ORDER BY step;

-- Review candidates from the chronological holdout scored by train.py.
SELECT type, COUNT(*) AS review_candidates,
       SUM(CASE WHEN isFraud=1 THEN 1 ELSE 0 END) AS fraud_captured,
       SUM(CASE WHEN isFraud=0 THEN 1 ELSE 0 END) AS legitimate_alerts
FROM read_parquet('reports/scored_test.parquet')
WHERE predicted_fraud_probability >= 0.50
GROUP BY type ORDER BY review_candidates DESC;

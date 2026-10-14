# Data dictionary

PaySim is a public synthetic mobile-money dataset. The simulator produces transaction records; the data is not from TD or real customers.

| Column | Meaning | Project use |
|---|---|---|
| step | Simulator hour index | Time ordering and monitoring |
| type | Transaction type | Segment/product proxy |
| amount | Transaction amount | Predictor and exposure measure |
| nameOrig, nameDest | Simulator account identifiers | Origin ID used only to derive prior activity; excluded as predictors |
| oldbalanceOrg, oldbalanceDest | Pre-transaction balances | Candidate predictors |
| newbalanceOrg, newbalanceDest | Post-transaction balances | Excluded to avoid post-event leakage |
| isFraud | Simulated target label | Training target and retrospective evaluation only |
| isFlaggedFraud | Existing simulator rule flag | Baseline comparison only; excluded as predictor |

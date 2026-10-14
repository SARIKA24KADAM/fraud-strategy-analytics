# Fraud strategy design

## Decision supported
Assess whether a candidate probability model merits a controlled pilot by comparing fraud dollars captured, legitimate alert volume, and operational review demand for each transaction type.

## Analysis workflow
1. Establish the existing simulator-flag baseline by type and hour.
2. Train on earlier observations and evaluate on a later period.
3. Compare several model thresholds with the existing flag.
4. Report fraud capture, precision/recall, alert rate, and legitimate alerts; estimate review demand against an explicit capacity assumption.
5. Recommend further validation or a reversible shadow-mode pilot only if evidence supports it.

A model score is a prioritization signal in this portfolio exercise. It does not authorize automatically declining a transaction.

## Trade-offs
Lower thresholds may capture more fraud but create more false-positive reviews. Transaction type is a proxy segment; this dataset does not record authentication friction, abandonment, actual customer harm, or investigator effort. Report these as limitations rather than inferred outcomes.

## Executive readout
Summarize the time period, baseline, threshold, fraud dollars captured, legitimate alerts, and capacity assumption. State uncertainty and simulator limits alongside any recommendation.

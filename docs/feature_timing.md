# Feature timing and leakage controls

Fraud strategies can use only information available at decision time. This project excludes post-transaction balances (`newbalanceOrg`, `newbalanceDest`) and the simulator's `isFlaggedFraud` flag from model predictors. The fraud label is used only as the target and retrospective outcome.

Raw simulator account identifiers are used only to derive origin-account activity in the prior 24 hourly steps and are not written to the feature table. The current event is excluded from those window calculations. Model evaluation uses a later time range than training.

These controls reduce obvious leakage but do not establish production readiness. Multiple events share hourly timestamps, so within-hour ordering is unavailable. A real system needs event-time definitions, late-event handling, point-in-time feature validation, and independent leakage review.

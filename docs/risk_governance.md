# Risk governance and responsible use

This portfolio prototype uses synthetic data. It is not a bank fraud control and must not be used to decide whether real people or payments are legitimate.

| Risk | Control or limitation |
|---|---|
| False declines or customer friction | Scores are for analysis; no automatic decline. Actual customer impact is not measured. |
| Missed fraud or evolving threats | Report recall and dollars missed; synthetic labels are not realistic threat coverage. |
| Operations overload | Show alert volume and compare it with an explicit capacity assumption. |
| Uneven outcomes | Segment available data by type and amount; PaySim lacks appropriate real customer outcomes for a meaningful fairness audit. |
| Leakage | Exclude post-event fields, target, and existing rule flag from predictors; use a chronological holdout. |
| Privacy | Use only the public synthetic file; never add confidential banking data. |
| Simulator mismatch | Results are exploratory and cannot be generalized to deployed fraud operations. |

Before any real pilot: use representative point-in-time institution data; complete independent validation, privacy/security and fairness assessments; obtain model-risk and operational approval; test thresholds against capacity; define monitoring and stop conditions; maintain decision audit trails and a tested rollback.

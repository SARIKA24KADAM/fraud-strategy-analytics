"""Streamlit viewer for generated fraud strategy reports."""
from pathlib import Path
import json

import pandas as pd
import streamlit as st

REPORTS = Path(__file__).parent / "reports"
st.set_page_config(page_title="Fraud Strategy Analytics", layout="wide")
st.title("Transaction Fraud Strategy Analytics")
st.caption("PaySim synthetic-data demonstration; not a production fraud decision tool.")

hourly_path = REPORTS / "hourly_strategy_monitoring.csv"
segment_path = REPORTS / "segment_baseline.csv"
metrics_path = REPORTS / "evaluation.json"

if not hourly_path.exists() or not segment_path.exists():
    st.info("Generate reports using the commands in README.md.")
    st.stop()

hourly = pd.read_csv(hourly_path)
segments = pd.read_csv(segment_path)
left, right = st.columns(2)

with left:
    st.subheader("Hourly activity and simulated fraud")
    hourly_metrics = [c for c in ("transaction_count", "fraud_count") if c in hourly]
    if hourly_metrics:
        st.line_chart(hourly.set_index("step")[hourly_metrics])
    st.dataframe(hourly, use_container_width=True, hide_index=True)

with right:
    st.subheader("Fraud by transaction type")
    segment_metrics = [c for c in ("fraud_count", "fraud_amount") if c in segments]
    if segment_metrics:
        st.bar_chart(segments.set_index("type")[segment_metrics])
    st.dataframe(segments, use_container_width=True, hide_index=True)

if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text())
    strategies = pd.DataFrame(metrics["strategies"])
    st.subheader("Model and rule strategy comparison")
    st.metric("Holdout ROC AUC", f"{metrics['roc_auc']:.3f}")
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.caption("Fraud capture versus review alert rate")
        st.scatter_chart(
            strategies,
            x="alert_rate",
            y="recall",
            color="strategy",
            size="fraud_amount_captured",
            use_container_width=True,
        )
    with chart_right:
        st.caption("Fraud dollars captured by strategy")
        st.bar_chart(strategies.set_index("strategy")[["fraud_amount_captured"]])
    quality = strategies.set_index("strategy")[["precision", "recall"]]
    st.caption("Precision and recall by strategy")
    st.bar_chart(quality)
    st.dataframe(strategies, use_container_width=True, hide_index=True)

st.warning("See docs/risk_governance.md. Synthetic results do not predict performance on real payment activity.")

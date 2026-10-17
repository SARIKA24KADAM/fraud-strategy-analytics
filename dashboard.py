"""Interactive graphs for the generated PaySim fraud strategy reports."""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
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

hourly = pd.read_csv(hourly_path).sort_values("step")
segments = pd.read_csv(segment_path).sort_values("fraud_amount", ascending=False)

st.header("Hourly activity")
activity_col, amount_col = st.columns(2)
with activity_col:
    st.subheader("Transaction and fraud counts")
    count_data = hourly.melt(
        id_vars="step",
        value_vars=["transaction_count", "fraud_count"],
        var_name="measure",
        value_name="transactions",
    )
    st.plotly_chart(
        px.line(
            count_data,
            x="step",
            y="transactions",
            color="measure",
            labels={"step": "Simulated hour", "transactions": "Count", "measure": ""},
        ),
        use_container_width=True,
    )
with amount_col:
    st.subheader("Fraud amount over time")
    st.plotly_chart(
        px.area(
            hourly,
            x="step",
            y="fraud_amount",
            labels={"step": "Simulated hour", "fraud_amount": "Fraud amount"},
        ),
        use_container_width=True,
    )

st.header("Fraud by transaction type")
type_amount, type_rate = st.columns(2)
with type_amount:
    st.subheader("Fraud amount")
    st.plotly_chart(
        px.bar(
            segments,
            x="type",
            y="fraud_amount",
            color="type",
            labels={"type": "Transaction type", "fraud_amount": "Fraud amount"},
        ),
        use_container_width=True,
    )
with type_rate:
    st.subheader("Fraud rate and existing simulator alerts")
    rate_data = segments.melt(
        id_vars="type",
        value_vars=["fraud_rate", "flagged_count"],
        var_name="measure",
        value_name="value",
    )
    st.plotly_chart(
        px.bar(
            rate_data,
            x="type",
            y="value",
            color="measure",
            barmode="group",
            labels={"type": "Transaction type", "value": "Rate / count", "measure": ""},
        ),
        use_container_width=True,
    )

if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    strategies = pd.DataFrame(metrics.get("strategies", []))
    if not strategies.empty:
        st.header("Model and rule strategy comparison")
        st.metric("Holdout ROC AUC", f"{metrics['roc_auc']:.3f}")
        comparison, dollars = st.columns(2)
        with comparison:
            st.subheader("Fraud capture versus alert rate")
            st.plotly_chart(
                px.scatter(
                    strategies,
                    x="alert_rate",
                    y="recall",
                    color="strategy",
                    size="fraud_amount_captured",
                    hover_data=["precision", "alerts", "legitimate_alerts"],
                    labels={"alert_rate": "Alert rate", "recall": "Fraud recall"},
                ),
                use_container_width=True,
            )
        with dollars:
            st.subheader("Fraud amount captured")
            st.plotly_chart(
                px.bar(
                    strategies.sort_values("fraud_amount_captured", ascending=False),
                    x="strategy",
                    y="fraud_amount_captured",
                    color="strategy",
                    labels={"strategy": "Strategy", "fraud_amount_captured": "Fraud amount"},
                ),
                use_container_width=True,
            )
        st.subheader("Precision and recall")
        quality = strategies.melt(
            id_vars="strategy",
            value_vars=["precision", "recall"],
            var_name="metric",
            value_name="value",
        )
        st.plotly_chart(
            px.bar(
                quality,
                x="strategy",
                y="value",
                color="metric",
                barmode="group",
                labels={"strategy": "Strategy", "value": "Score", "metric": ""},
            ),
            use_container_width=True,
        )

with st.expander("View report data"):
    st.subheader("Hourly monitoring")
    st.dataframe(hourly, use_container_width=True, hide_index=True)
    st.subheader("Transaction type summary")
    st.dataframe(segments, use_container_width=True, hide_index=True)
    if metrics_path.exists():
        st.subheader("Strategy metrics")
        st.dataframe(strategies, use_container_width=True, hide_index=True)

st.warning(
    "See docs/risk_governance.md. Synthetic results do not predict performance on real payment activity."
)

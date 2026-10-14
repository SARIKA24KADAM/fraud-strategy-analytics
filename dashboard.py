"""Streamlit viewer for generated monitoring reports."""
from pathlib import Path
import pandas as pd
import streamlit as st
R=Path(__file__).parent/"reports"
st.set_page_config(page_title="Fraud Strategy Analytics",layout="wide")
st.title("Transaction Fraud Strategy Analytics")
st.caption("PaySim synthetic-data demonstration — not a production fraud decision tool.")
a,b=st.columns(2)
hourly=R/"hourly_strategy_monitoring.csv"; segment=R/"segment_baseline.csv"; metrics=R/"evaluation.json"
if not hourly.exists() or not segment.exists():
    st.info("Generate reports using the commands in README.md."); st.stop()
h=pd.read_csv(hourly); s=pd.read_csv(segment)
with a:
    st.subheader("Hourly activity and simulated fraud")
    st.line_chart(h.set_index("step")[["transaction_count","fraud_count"]])
    st.dataframe(h,use_container_width=True,hide_index=True)
with b:
    st.subheader("Performance by transaction type")
    st.bar_chart(s.set_index("type")[["fraud_count","fraud_amount"]])
    st.dataframe(s,use_container_width=True,hide_index=True)
if metrics.exists():
    import json
    st.subheader("Holdout strategy comparison")
    m=json.loads(metrics.read_text())
    st.metric("ROC AUC",f"{m['roc_auc']:.3f}")
    st.dataframe(pd.DataFrame(m["strategies"]),use_container_width=True,hide_index=True)
st.warning("See docs/risk_governance.md. Synthetic results do not predict performance on bank transactions.")

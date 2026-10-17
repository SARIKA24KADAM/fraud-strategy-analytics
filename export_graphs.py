"""Export PNG charts from the generated PaySim strategy reports."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
OUTPUT = REPORTS / "graphs"


def export_graphs():
    hourly = pd.read_csv(REPORTS / "hourly_strategy_monitoring.csv")
    segments = pd.read_csv(REPORTS / "segment_baseline.csv")
    OUTPUT.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly["step"], hourly["transaction_count"], label="Transactions", linewidth=1.5)
    ax.plot(hourly["step"], hourly["fraud_count"], label="Fraud transactions", linewidth=1.5)
    ax.set(title="Hourly transaction and fraud counts", xlabel="Simulated hour", ylabel="Count")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT / "hourly_activity.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly["step"], hourly["fraud_amount"], color="#c0392b", linewidth=1.5)
    ax.fill_between(hourly["step"], hourly["fraud_amount"], color="#c0392b", alpha=0.15)
    ax.set(title="Simulated fraud amount by hour", xlabel="Simulated hour", ylabel="Fraud amount")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT / "hourly_fraud_amount.png", dpi=180)
    plt.close(fig)

    ordered = segments.sort_values("fraud_amount", ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(ordered["type"], ordered["fraud_amount"], color="#2874a6")
    ax.set(title="Simulated fraud amount by transaction type", xlabel="Fraud amount", ylabel="Transaction type")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT / "fraud_by_transaction_type.png", dpi=180)
    plt.close(fig)

    metrics_path = REPORTS / "evaluation.json"
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        strategies = pd.DataFrame(metrics.get("strategies", []))
        if not strategies.empty:
            fig, ax = plt.subplots(figsize=(9, 5))
            for _, row in strategies.iterrows():
                ax.scatter(row["alert_rate"], row["recall"], s=70, label=row["strategy"])
                ax.annotate(row["strategy"], (row["alert_rate"], row["recall"]), xytext=(5, 4),
                            textcoords="offset points", fontsize=8)
            ax.set(title="Fraud capture versus alert rate", xlabel="Alert rate", ylabel="Recall")
            ax.grid(alpha=0.25)
            fig.tight_layout()
            fig.savefig(OUTPUT / "strategy_alert_rate_vs_recall.png", dpi=180)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(strategies["strategy"], strategies["fraud_amount_captured"], color="#198754")
            ax.set(title="Fraud amount captured by strategy", xlabel="Strategy", ylabel="Fraud amount captured")
            ax.tick_params(axis="x", labelrotation=25)
            ax.grid(axis="y", alpha=0.25)
            fig.tight_layout()
            fig.savefig(OUTPUT / "strategy_fraud_amount_captured.png", dpi=180)
            plt.close(fig)

    print(f"PNG graphs written to {OUTPUT}")


if __name__ == "__main__":
    export_graphs()

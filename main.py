# =========================
# main.py ._.
# Full experiment runner ._.
# by mrsizzze
# =========================

from simulation.engine import SimulationEngine
from simulation.analysis import FatigueAnalyzer
from simulation.visualization import (
    plot_attention_over_time,
    plot_reaction_distribution,
)

import pandas as pd

def run_experiment(
    duration: float = 100.0,
    alert_rate: float = 0.5,
    dt: float = 1.0,
    export_csv: bool = True,
):

    # =========================
    # create simulation engine ._.
    # =========================

    engine = SimulationEngine(
        duration=duration,
        alert_rate=alert_rate,
        dt=dt,
    )

    # =========================
    # run simulation ._.
    # =========================

    events = engine.run()

    # =========================
    # analyze results ._.
    # =========================

    analyzer = FatigueAnalyzer(events)
    report = analyzer.compute_metrics()

    # =========================
    # print structured report ._.
    # =========================

    print("\n===== ALERT FATIGUE REPORT =====")
    print(f"Total alerts: {report.total_alerts}")
    print(f"Ignored alerts: {report.ignored_alerts}")
    print(f"Ignored HIGH severity: {report.ignored_high_severity}")
    print(f"Fatigue start time: {report.fatigue_start_time}")
    print(f"Average attention: {report.average_attention:.3f}")
    print(f"Critical miss rate: {report.critical_miss_rate:.3f}")

    # =========================
    # export data ._.
    # =========================

    df = analyzer.export_timeseries()

    if export_csv:
        df.to_csv("experiment_results.csv", index=False)
        print("\nResults exported to experiment_results.csv")

    # =========================
    # visualization ._.
    # =========================

    plot_attention_over_time(df)
    plot_reaction_distribution(df)

if __name__ == "__main__":
    run_experiment()
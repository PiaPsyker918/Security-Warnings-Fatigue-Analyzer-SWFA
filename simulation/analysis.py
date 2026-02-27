# =========================
# simulation/analysis.py ._.
# alert fatigue metrics and statistical analysis ._.
# by mrsizzze
# =========================

from dataclasses import dataclass
from typing import List
import numpy as np
import pandas as pd
from core import Reaction, Severity
from simulation.engine import SimulationEvent

# =========================
# result container ._.
# =========================

@dataclass(slots=True)
class FatigueReport:
    total_alerts: int
    ignored_alerts: int
    ignored_high_severity: int
    fatigue_start_time: float | None
    average_attention: float
    critical_miss_rate: float

# =========================
# core analyzer ._.
# =========================

class FatigueAnalyzer:
    def __init__(self, events: List[SimulationEvent]):
        self.events = events
        self.df = self._build_dataframe(events)

# =========================
# dataFrame builder ._.
# =========================

    def _build_dataframe(self, events: List[SimulationEvent]) -> pd.DataFrame:
        data = [
            {
                "timestamp": e.timestamp,
                "severity": float(e.severity),
                "reaction": e.reaction.value,
                "attention": e.attention,
                "is_high": e.severity == Severity.HIGH,
                "is_ignored": e.reaction == Reaction.IGNORE,
            }
            for e in events
        ]
        df = pd.DataFrame(data)
        if not df.empty:
            df.sort_values("timestamp", inplace=True)
            df.reset_index(drop=True, inplace=True)

        return df

# =========================
# fatigue detection logic ._.
# =========================

    def detect_fatigue_point(
        self,
        attention_threshold: float = 0.5,
        window: int = 5,
    ) -> float | None:
        if self.df.empty:
            return None
        rolling_attention = (
            self.df["attention"]
            .rolling(window=window, min_periods=1)
            .mean()
        )
        below_threshold = rolling_attention < attention_threshold
        if below_threshold.any():
            idx = below_threshold.idxmax()
            return float(self.df.loc[idx, "timestamp"])

        return None

# =========================
# metrics computation ._.
# =========================

    def compute_metrics(self) -> FatigueReport:
        if self.df.empty:
            return FatigueReport(
                total_alerts=0,
                ignored_alerts=0,
                ignored_high_severity=0,
                fatigue_start_time=None,
                average_attention=1.0,
                critical_miss_rate=0.0,
            )
        total_alerts = len(self.df)
        ignored_alerts = int(self.df["is_ignored"].sum())
        high_df = self.df[self.df["is_high"]]
        ignored_high = int(
            high_df[high_df["is_ignored"]].shape[0]
        )
        fatigue_point = self.detect_fatigue_point()
        avg_attention = float(self.df["attention"].mean())
        critical_miss_rate = (
            ignored_high / len(high_df)
            if len(high_df) > 0
            else 0.0
        )

        return FatigueReport(
            total_alerts=total_alerts,
            ignored_alerts=ignored_alerts,
            ignored_high_severity=ignored_high,
            fatigue_start_time=fatigue_point,
            average_attention=avg_attention,
            critical_miss_rate=critical_miss_rate,
        )

# =========================
# time-series export ._.
# =========================

    def export_timeseries(self) -> pd.DataFrame:
        
        return self.df.copy()

# =========================
# simulation/engine.py ._.
# by mrsizzze
# =========================

from dataclasses import dataclass
from typing import List
import numpy as np

from core import Alert, Severity, Reaction, User


# =========================
# simulation event ._.
# =========================

@dataclass(slots=True)
class SimulationEvent:
    timestamp: float
    severity: Severity
    reaction: Reaction
    attention: float


# =========================
# simulation engine ._.
# =========================

class SimulationEngine:

    def __init__(
        self,
        duration: float = 100.0,
        alert_rate: float = 0.5,
        dt: float = 1.0,
    ):
        self.duration = duration
        self.alert_rate = alert_rate
        self.dt = dt

        self.user = User()
        self.current_time = 0.0
        self.events: List[SimulationEvent] = []

        self.rng = np.random.default_rng()

    # =========================
    # run simulation ._.
    # =========================
    def run(self) -> List[SimulationEvent]:

        while self.current_time < self.duration:

            self.user.step(self.dt)

            if self.rng.random() < self.alert_rate:

                severity = self._sample_severity()

                alert = Alert(
                    severity=severity,
                    type="generic",
                    timestamp=self.current_time,
                )

                reaction, attention = self.user.react_to_alert(alert)

                event = SimulationEvent(
                    timestamp=self.current_time,
                    severity=severity,
                    reaction=reaction,
                    attention=attention,
                )

                self.events.append(event)

            self.current_time += self.dt

        return self.events

    # =========================
    # severity sampling ._.
    # =========================
    def _sample_severity(self) -> Severity:

        r = self.rng.random()

        if r < 0.6:
            return Severity.LOW
        elif r < 0.9:
            return Severity.MEDIUM
        else:
            return Severity.HIGH
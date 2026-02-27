# =========================
# simulation-scenarios.py ._.
# Alert scenario definitions and loaders ._.
# by mrsizzze
# =========================

from dataclasses import dataclass
from typing import List, Iterable
import json
import yaml

from core import Alert, Severity

# =========================
# scenario definition ._.
# =========================

@dataclass(slots=True)
class AlertScenario:
    name: str
    alerts: List[Alert]

# =========================
# programmatic scenario generators ._.
# =========================

def constant_rate_scenario(
    name: str,
    severity: Severity,
    alert_type: str,
    interval: float,
    count: int,
) -> AlertScenario:
    alerts: List[Alert] = []
    time = 0.0
    for _ in range(count):
        alerts.append(
            Alert(
                severity=severity,
                type=alert_type,
                timestamp=time,
            )
        )
        time += interval

    return AlertScenario(name=name, alerts=alerts)

def mixed_severity_scenario(
    name: str,
    pattern: List[Severity],
    alert_type: str,
    interval: float,
) -> AlertScenario:
    alerts: List[Alert] = []
    time = 0.0
    for sev in pattern:
        alerts.append(
            Alert(
                severity=sev,
                type=alert_type,
                timestamp=time,
            )
        )
        time += interval

    return AlertScenario(name=name, alerts=alerts)

# =========================
# file based scenario loaders ._.
# =========================

def load_scenario_from_dict(data: dict, name: str) -> AlertScenario:
    alerts: List[Alert] = []

    for entry in data.get("alerts", []):
        alerts.append(
            Alert(
                severity=Severity(entry["severity"]),
                type=entry["type"],
                timestamp=float(entry["timestamp"]),
            )
        )
    alerts.sort(key=lambda a: a.timestamp)

    return AlertScenario(name=name, alerts=alerts)

def load_scenario_from_json(path: str) -> AlertScenario:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    name = data.get("name", path)
    return load_scenario_from_dict(data, name)

def load_scenario_from_yaml(path: str) -> AlertScenario:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    name = data.get("name", path)

    return load_scenario_from_dict(data, name)

# =========================
# scenario utilities ._.
# =========================

def iter_alerts(scenario: AlertScenario) -> Iterable[Alert]:
    for alert in scenario.alerts:
        yield alert

# just utils -_-
# by PiaPsyker918

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PNG = ROOT / "png"
PNG.mkdir(exist_ok=True)

from collections import Counter
from core.user import User, Alert

def run_simulation(severity, n=5000):
    user = User()
    c = Counter()

    for _ in range(n):
        action, _ = user.react_to_alert(Alert(severity, "", 0))
        c[action] += 1

    return c

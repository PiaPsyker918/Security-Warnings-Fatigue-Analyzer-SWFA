
# by PiaPsyker918

from core.user import User, Severity, Alert
import matplotlib.pyplot as plt
from pathlib import Path

def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)

    for f in [0.05, 0.15, 0.3, 0.6]:
        user = User(fatigue_rate=f)
        att = []

        for _ in range(200):
            user.react_to_alert(Alert(Severity.MEDIUM, "", 0))
            att.append(user.get_attention())

        plt.plot(att, label=f"f={f}")

    plt.legend()
    plt.savefig(OUT / "fatigue_sweep.png")

if __name__ == "__main__":
    run()

# by PiaPsyker918

import matplotlib.pyplot as plt
from core.user import User, Alert, Severity
from pathlib import Path

def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(parents=True, exist_ok=True)

    user = User()

    att = []

    # нагрузка
    for _ in range(100):
        user.react_to_alert(Alert(Severity.MEDIUM, "", 0))
        att.append(user.get_attention())

    # отдых
    for _ in range(100):
        user.step(1.0)
        att.append(user.get_attention())

    plt.plot(att)
    plt.title("Fatigue → Recovery")


    plt.savefig(OUT / "fatigue_recovery_plot.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    run()
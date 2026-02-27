
# by PiaPsyker918

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from pathlib import Path
from core.user import User, Alert, Severity

def run():

    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(parents=True, exist_ok=True)


    user = User()
    att = []

    for t in range(300):
        _, a = user.react_to_alert(Alert(Severity.MEDIUM, "security", t))
        att.append(a)

    plt.figure(figsize=(8,4))
    plt.plot(att)
    plt.grid()
    plt.title("Attention decay")

    plt.savefig(OUT / "attention_decay.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    run()
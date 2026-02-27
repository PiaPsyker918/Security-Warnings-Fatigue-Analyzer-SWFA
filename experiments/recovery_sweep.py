
# by PiaPsyker918

from core.user import User
import matplotlib.pyplot as plt
from pathlib import Path

def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)

    for r in [0.01, 0.05, 0.1, 0.2]:
        user = User(initial_attention=0.2, recovery_rate=r)
        att = []

        for _ in range(200):
            user.step(1.0)
            att.append(user.get_attention())

        plt.plot(att, label=f"r={r}")

    plt.legend()
    plt.savefig(OUT / "recovery_sweep.png")

if __name__ == "__main__":
    run()

# by PiaPsyker918

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from core.user import User, Alert, Severity, Reaction

def run():

    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(parents=True, exist_ok=True)


    def simulate(severity, n=3000):
        user = User()
        reads = []

        for _ in range(n):
            action, _ = user.react_to_alert(Alert(severity, "", 0))
            reads.append(action == Reaction.READ)

        return reads


    def cumulative_rate(arr):
        arr = np.array(arr, dtype=float)
        return np.cumsum(arr) / np.arange(1, len(arr)+1)


    low = simulate(Severity.LOW)
    high = simulate(Severity.HIGH)


    plt.figure(figsize=(8, 4))
    plt.plot(cumulative_rate(low), label="LOW")
    plt.plot(cumulative_rate(high), label="HIGH")

    plt.xlabel("alerts")
    plt.ylabel("P(read)")
    plt.title("Read probability vs severity")
    plt.legend()
    plt.grid()

    plt.savefig(OUT / "severity_compare.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    run()
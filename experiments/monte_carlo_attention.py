
# Monte Carlo experiments / Monte Carlo simulations, are a broad class of computational algorithms based on repeated random sampling for obtaining numerical results. 
# The underlying concept is to use randomness to solve deterministic problems.
# by PiaPsyker918

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from core.user import User, Alert, Severity

def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)


    RUNS = 80
    STEPS = 300

    all_runs = []

    for _ in range(RUNS):
        user = User()
        att = []

        for _ in range(STEPS):
            user.react_to_alert(Alert(Severity.MEDIUM, "", 0))
            att.append(user.get_attention())

        all_runs.append(att)

    arr = np.array(all_runs)

    mean = arr.mean(axis=0)
    std = arr.std(axis=0)

    plt.figure(figsize=(8, 4))
    plt.plot(mean, label="mean attention")
    plt.fill_between(range(STEPS), mean - std, mean + std, alpha=0.3, label="± std")

    plt.legend()
    plt.title("Monte-Carlo Attention Dynamics")

    plt.savefig(OUT / "monte_carlo_attention.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    run()
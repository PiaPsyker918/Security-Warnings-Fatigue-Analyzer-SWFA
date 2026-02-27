
# by PiaPsyker918

import matplotlib.pyplot as plt
from experiments.utils import PNG
from core.user import Severity, Reaction
from experiments.utils import run_simulation

def run():
    low = run_simulation(Severity.LOW)
    high = run_simulation(Severity.HIGH)

    labels = ["READ", "IGNORE", "ERROR"]

    low_vals = [low[r] for r in Reaction]
    high_vals = [high[r] for r in Reaction]

    x = range(len(labels))

    plt.bar(x, low_vals, width=0.4, label="LOW")
    plt.bar([i+0.4 for i in x], high_vals, width=0.4, label="HIGH")

    plt.xticks([i+0.2 for i in x], labels)
    plt.legend()
    plt.title("Severity effect on reactions")

    plt.savefig(PNG / "severity_comparison.png", dpi=150)
    plt.close()

if __name__ == "__main__":
    run()
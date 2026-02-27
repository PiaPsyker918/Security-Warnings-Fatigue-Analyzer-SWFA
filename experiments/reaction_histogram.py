
# by PiaPsyker918

import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

from core.user import User, Alert, Severity

def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)


    user = User()

    c = Counter()

    for _ in range(8000):
        action, _ = user.react_to_alert(Alert(Severity.HIGH, "", 0))
        c[action.value] += 1


    labels = list(c.keys())
    values = list(c.values())

    plt.bar(labels, values)
    plt.title("Reaction distribution (HIGH severity)")

    plt.savefig(OUT / "reaction_hist.png", dpi=150)
    plt.show()
    
if __name__ == "__main__":
    run()
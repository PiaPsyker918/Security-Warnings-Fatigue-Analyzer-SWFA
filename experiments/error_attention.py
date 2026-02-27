
# by PiaPsyker918

from core.user import User, Severity, Alert
import matplotlib.pyplot as plt
from pathlib import Path

def run():

    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)
    
    errors = []
    levels = []
    
    for a0 in [0.1, 0.3, 0.5, 0.7, 1.0]:
        user = User(initial_attention=a0)
        err = 0
    
        for _ in range(2000):
            action, _ = user.react_to_alert(Alert(Severity.HIGH, "", 0))
            if action == action.ERROR:
                err += 1
    
        levels.append(a0)
        errors.append(err / 2000)
    
    plt.plot(levels, errors, marker="o")
    plt.xlabel("initial attention")
    plt.ylabel("error rate")
    plt.savefig(OUT / "error_vs_attention.png")

if __name__ == "__main__":
    run()

# by PiaPsyker918

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

from core.user import User, Alert, Reaction

def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)


    attentions = np.linspace(0.05, 1.0, 20)
    severities = np.linspace(0.1, 1.0, 20)

    Z = np.zeros((len(attentions), len(severities)))

    N = 600

    for i, a0 in enumerate(attentions):
        for j, sev in enumerate(severities):
            user = User(initial_attention=a0)

            errors = 0
            for _ in range(N):
                action, _ = user.react_to_alert(Alert(sev, "", 0))
                if action == Reaction.ERROR:
                    errors += 1

            Z[i, j] = errors / N


    X, Y = np.meshgrid(severities, attentions)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection="3d")

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel("severity")
    ax.set_ylabel("initial attention")
    ax.set_zlabel("error rate")

    plt.savefig(OUT / "error_surface_3d.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    run()
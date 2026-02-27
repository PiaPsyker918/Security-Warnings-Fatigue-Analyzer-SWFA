#import numpy as np
#import matplotlib.pyplot as plt
#from pathlib import Path
#
#from core.user import User, Alert, Severity, Reaction
#
#
#def run():
#    OUT = Path(__file__).resolve().parents[1] / "output"
#    OUT.mkdir(exist_ok=True)
#
#    attentions = np.linspace(0.05, 1.0, 20)
#    severities = np.linspace(0.1, 1.0, 20)
#
#    error_heat = np.zeros((len(attentions), len(severities)))
#    attention_heat = np.zeros((len(attentions), len(severities)))
#
#    N = 800
#
#    for i, a0 in enumerate(attentions):
#        for j, sev in enumerate(severities):
#
#            user = User(initial_attention=a0)
#
#            errors = 0
#            attention_values = []
#
#            for _ in range(N):
#                action, _ = user.react_to_alert(
#                    Alert(sev, "", 0)
#                )
#                user.step(1.0)
#
#                attention_values.append(user.get_attention())
#
#                if action == Reaction.ERROR:
#                    errors += 1
#
#            error_heat[i, j] = errors / N
#            attention_heat[i, j] = np.mean(attention_values)
#
#    # ERROR HEATMAP
#    plt.figure(figsize=(7, 6))
#    plt.imshow(
#        error_heat,
#        origin="lower",
#        extent=[0.1, 1.0, 0.05, 1.0],
#        aspect="auto"
#    )
#    plt.colorbar(label="Error rate")
#    plt.xlabel("Severity")
#    plt.ylabel("Initial attention")
#    plt.title("Error Rate Heatmap")
#    plt.savefig(OUT / "error_heatmap.png", dpi=150)
#    plt.show()
#
#    # ATTENTION HEATMAP
#    plt.figure(figsize=(7, 6))
#    plt.imshow(
#        attention_heat,
#        origin="lower",
#        extent=[0.1, 1.0, 0.05, 1.0],
#        aspect="auto"
#    )
#    plt.colorbar(label="Mean attention")
#    plt.xlabel("Severity")
#    plt.ylabel("Initial attention")
#    plt.title("Attention Heatmap")
#    plt.savefig(OUT / "attention_heatmap.png", dpi=150)
#    plt.show()
#
#
#if __name__ == "__main__":
#    run()

# by PiaPsyker918

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from core.user import User, Alert, Severity, Reaction


def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)

    attentions = np.linspace(0.05, 1.0, 20)
    severities = np.linspace(0.1, 1.0, 20)

    error_heat = np.zeros((len(attentions), len(severities)))
    stable_mask = np.zeros_like(error_heat)

    N = 800

    for i, a0 in enumerate(attentions):
        for j, sev in enumerate(severities):

            user = User(initial_attention=a0)

            errors = 0
            attention_values = []

            for _ in range(N):
                action, _ = user.react_to_alert(
                    Alert(sev, "", 0)
                )
                user.step(1.0)

                attention_values.append(user.get_attention())

                if action == Reaction.ERROR:
                    errors += 1

            mean_attention = np.mean(attention_values)
            error_rate = errors / N

            error_heat[i, j] = error_rate

            if mean_attention > 0.1 and error_rate < 0.7:
                stable_mask[i, j] = 1

    # ERROR HEATMAP
    plt.figure(figsize=(7, 6))
    plt.imshow(
        error_heat,
        origin="lower",
        extent=[0.1, 1.0, 0.05, 1.0],
        aspect="auto"
    )
    plt.colorbar(label="Error rate")

    plt.contour(
        stable_mask,
        levels=[0.5],
        colors="white",
        linewidths=2,
        extent=[0.1, 1.0, 0.05, 1.0]
    )

    plt.xlabel("Severity")
    plt.ylabel("Initial attention")
    plt.title("Error Heatmap with Stable Region")
    plt.show()


if __name__ == "__main__":
    run()
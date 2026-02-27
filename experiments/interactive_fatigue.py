
# by PiaPsyker918

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from pathlib import Path

from core.user import User, Alert, Severity

def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)


    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    line, = ax.plot([])
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 300)


    def simulate(fatigue):
        user = User(fatigue_rate=fatigue)
        att = []

        for _ in range(300):
            user.react_to_alert(Alert(Severity.MEDIUM, "", 0))
            att.append(user.get_attention())

        return att


    def update(val):
        att = simulate(slider.val)
        line.set_data(range(len(att)), att)
        fig.canvas.draw_idle()


    slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
    slider = Slider(slider_ax, "fatigue_rate", 0.01, 0.6, valinit=0.15)

    slider.on_changed(update)

    update(0.15)

    plt.savefig(OUT / "interactive_snapshot.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    run()

# by PiaPsyker918

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path

from core.user import User, Alert, Severity

def run():

    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)


    user = User()

    fig, ax = plt.subplots()
    line, = ax.plot([], [])

    ax.set_xlim(0, 300)
    ax.set_ylim(0, 1)

    att = []

    def update(frame):
        user.react_to_alert(Alert(Severity.MEDIUM, "", 0))
        att.append(user.get_attention())

        line.set_data(range(len(att)), att)
        return line,


    ani = animation.FuncAnimation(fig, update, frames=300, interval=20)

    ani.save(OUT / "attention.gif", writer="pillow")

if __name__ == "__main__":
    run()
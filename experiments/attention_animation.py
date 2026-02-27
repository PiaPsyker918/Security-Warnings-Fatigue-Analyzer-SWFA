
# by PiaPsyker918

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path

from core.user import User, Alert, Severity

def run():
    OUT = Path(__file__).resolve().parents[1] / "output"
    OUT.mkdir(exist_ok=True)


    user = User()

    fig, ax = plt.subplots(figsize=(8, 4))
    line, = ax.plot([], [])

    att = []

    ax.set_xlim(0, 400)
    ax.set_ylim(0, 1)
    ax.set_title("Attention over time (animation)")
    ax.set_xlabel("step")
    ax.set_ylabel("attention")
    ax.grid()


    def update(frame):
        if frame < 250:
            user.react_to_alert(Alert(Severity.MEDIUM, "", 0))
        else:
            user.step(1.0)

        att.append(user.get_attention())

        line.set_data(range(len(att)), att)
        return line,


    ani = animation.FuncAnimation(
        fig,
        update,
        frames=400,
        interval=20,
        blit=True
    )

    ani.save(OUT / "attention_animation.gif", writer="pillow")

    plt.show()

if __name__ == "__main__":
    run()
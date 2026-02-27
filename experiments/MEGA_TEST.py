
# by PiaPsyker918

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from core.user import User, Alert, Severity, Reaction


def run(
    steps: int = 1000000,
    error_sensitivity: float = 2.0,
    temperature: float = 1.0,
    seed: int = 42,
):

    print("=== STRESS TEST ===")
    print(f"steps: {steps}")
    print(f"error_sensitivity: {error_sensitivity}")
    print(f"temperature: {temperature}")
    print()

    rng = np.random.default_rng(seed)

    user = User(
        rng=rng,
        error_sensitivity=error_sensitivity,
        temperature=temperature,
    )

    attention_values = []
    error_count = 0

    for t in range(steps):

        if t < steps * 0.4:
            severity = Severity.HIGH
        elif t < steps * 0.8:
            severity = rng.choice([Severity.LOW, Severity.MEDIUM, Severity.HIGH])
        else:
            severity = Severity.HIGH

        action, _ = user.react_to_alert(
            Alert(severity=severity, type="", timestamp=0)
        )

        user.step(1.0)

        attention_values.append(user.get_attention())

        if action == Reaction.ERROR:
            error_count += 1

    attention_values = np.array(attention_values)

    print("Final attention:", attention_values[-1])
    print("Mean attention:", np.mean(attention_values))
    print("Error rate:", error_count / steps)
    print("Min attention:", np.min(attention_values))
    print("Max attention:", np.max(attention_values))

    plt.figure(figsize=(10, 4))
    plt.plot(attention_values)
    plt.title("Attention under stress test")
    plt.xlabel("step")
    plt.ylabel("attention")
    plt.show()


if __name__ == "__main__":
    run()
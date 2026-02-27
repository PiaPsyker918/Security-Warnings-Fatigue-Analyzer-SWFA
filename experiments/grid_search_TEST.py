
# by PiaPsyker918

import itertools
import csv
import numpy as np

from core.user import User, Alert, Severity


def evaluate(error_sensitivity, temperature, n_steps=5000, seed=42):
    rng = np.random.default_rng(seed)
    user = User(
        rng=rng,
        error_sensitivity=error_sensitivity,
        temperature=temperature,
    )

    attention_values = []
    error_count = 0

    for _ in range(n_steps):
        reaction, attention = user.react_to_alert(
            Alert(severity=Severity.MEDIUM, type="", timestamp=0.0)
        )

        user.step(1.0)

        attention_values.append(attention)

        if reaction.value == "error":
            error_count += 1

    mean_attention = np.mean(attention_values)
    error_rate = error_count / n_steps

    return mean_attention, error_rate


def run():
    error_values = [0.5, 1, 2, 3, 4]
    temperature_values = [0.7, 1.0, 1.3, 1.6]

    results = []

    for e, t in itertools.product(error_values, temperature_values):
        mean_a, err = evaluate(e, t)
        results.append((e, t, mean_a, err))
        print(f"e={e}, t={t} → A={mean_a:.3f}, err={err:.3f}")

    with open("grid_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["error_sensitivity", "temperature", "mean_attention", "error_rate"])
        writer.writerows(results)


if __name__ == "__main__":
    run()
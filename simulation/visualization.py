# =========================
# simulation-visualization.py ._.
# visualization utilities ._.
# by mrsizzze
# =========================

import matplotlib.pyplot as plt
import pandas as pd

def plot_attention_over_time(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["attention"])
    plt.xlabel("Time")
    plt.ylabel("Attention")
    plt.title("User Attention Over Time")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.show()

def plot_reaction_distribution(df: pd.DataFrame) -> None:
    counts = df["reaction"].value_counts()
    plt.figure(figsize=(6, 4))
    plt.bar(counts.index, counts.values)
    plt.xlabel("Reaction")
    plt.ylabel("Count")
    plt.title("Reaction Distribution")
    plt.show()
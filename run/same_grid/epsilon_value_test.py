from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np

from experiment.attack.stationary.guess_trajectory import (
    grr_estimated_guess,
    olh_estimated_guess,
    oue_estimated_guess,
    rappor_estimated_guess,
)


K = 20
EPSILON_VALUES = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]

DATASET_PATH = Path("../../dataset/geolife/geolife_grid.dat")
OUTPUT_PLOT_PATH = Path("geolife.png")

PLOT_TITLE = "Geolife"
Y_LABEL = "Ratio Of Guess"
X_LABEL = "Epsilon Values"


@dataclass(frozen=True)
class ProtocolGuessConfig:
    name: str
    guess_fn: Callable[[list[np.ndarray], int, float], float]
    color: str
    marker: str


PROTOCOLS = [
    ProtocolGuessConfig("GRR", grr_estimated_guess, "purple", "o"),
    ProtocolGuessConfig("RAPPOR", rappor_estimated_guess, "grey", "s"),
    ProtocolGuessConfig("OUE", oue_estimated_guess, "blue", "x"),
    ProtocolGuessConfig("OLH", olh_estimated_guess, "green", "d"),
]


def read_user_grid_values(dataset_path: Path) -> list[np.ndarray]:
    users_grid_values = []

    with dataset_path.open() as file:
        for line in file:
            grid_values = [int(value) for value in line.strip().split()]
            users_grid_values.append(np.array(grid_values))

    return users_grid_values


def run_experiment(users_grid_values: list[np.ndarray]) -> dict[str, list[float]]:
    results = {protocol.name: [] for protocol in PROTOCOLS}

    for epsilon in EPSILON_VALUES:
        print(f"Epsilon Value Is: {epsilon}")

        for protocol in PROTOCOLS:
            guess_probability = protocol.guess_fn(users_grid_values, K, epsilon)
            results[protocol.name].append(guess_probability)

            print(f"{protocol.name}: {guess_probability}")

    return results


def print_results(results: dict[str, list[float]]) -> None:
    for protocol_name, probabilities in results.items():
        print(f"Probability Of Guess For {protocol_name}: {probabilities}")


def plot_results(results: dict[str, list[float]]) -> None:
    plt.rcParams.update({"font.size": 12})
    plt.figure(figsize=(4 * 1.33, 4 * 1.33))
    plt.title(PLOT_TITLE)

    for protocol in PROTOCOLS:
        plt.plot(
            EPSILON_VALUES,
            results[protocol.name],
            linewidth=2,
            color=protocol.color,
            marker=protocol.marker,
            markersize=10,
            mew=1.5,
            fillstyle="none",
            clip_on=False,
            label=protocol.name,
        )

    plt.ylim(0, 1)
    plt.xticks(fontsize=15)
    plt.ylabel(Y_LABEL)
    plt.xlabel(X_LABEL)
    plt.grid(linestyle=":")
    plt.legend(prop={"size": 12}, ncol=2, columnspacing=0.75)

    plt.savefig(OUTPUT_PLOT_PATH, format="png", dpi=300, bbox_inches="tight")
    plt.show()


def main() -> None:
    users_grid_values = read_user_grid_values(DATASET_PATH)

    results = run_experiment(users_grid_values)

    print_results(results)
    plot_results(results)


if __name__ == "__main__":
    main()

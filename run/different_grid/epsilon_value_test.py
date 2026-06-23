import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt

from dataset.helper import read_dataset
from experiment.attack.transit.guess_trajectory import (
    guess_plain_user_trajectory,
    guess_plain_user_trajectory_olh,
)
from hidden_markov_model.HMM import HMM
from LDP.protocols.GRR import GRR
from LDP.protocols.OLH import OLH
from LDP.protocols.OUE import OUE
from LDP.protocols.RAPPOR import RAPPOR


K = 20
EPSILON_VALUES = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]

DATASET_PATH = Path("../../dataset/geolife/geolife_grid.dat")
DATASET_NAME = "Geolife"
DATASET_TYPE = "geolife"
METRIC_TYPE = "PA"
OUTPUT_PLOT_PATH = Path("plot.png")


@dataclass(frozen=True)
class ProtocolConfig:
    name: str
    protocol_cls: type
    guess_fn: Callable


PROTOCOLS = [
    ProtocolConfig("GRR", GRR, guess_plain_user_trajectory),
    ProtocolConfig("RAPPOR", RAPPOR, guess_plain_user_trajectory),
    ProtocolConfig("OUE", OUE, guess_plain_user_trajectory),
    ProtocolConfig("OLH", OLH, guess_plain_user_trajectory_olh),
]


def run_experiment(user_trajectories: list) -> dict[str, list[float]]:
    results = {protocol.name: [] for protocol in PROTOCOLS}

    for epsilon in EPSILON_VALUES:
        print(f"Epsilon Value: {epsilon}")

        for protocol in PROTOCOLS:
            ldp_protocol = protocol.protocol_cls(K, epsilon)
            hmm_model = HMM(K, epsilon)

            probability = protocol.guess_fn(
                ldp_protocol,
                hmm_model,
                user_trajectories,
                METRIC_TYPE,
                DATASET_TYPE,
            )

            results[protocol.name].append(probability)
            print(f"{protocol.name} is ready")

    return results


def get_memory_usage_mb() -> float:
    snapshot = tracemalloc.take_snapshot()
    total_size_bytes = sum(stat.size for stat in snapshot.statistics("lineno"))
    return total_size_bytes / (1024 * 1024)


def print_results(
    results: dict[str, list[float]], elapsed_time: float, memory_mb: float
) -> None:
    print(f"Total Size: {memory_mb:.2f} MB")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")

    for protocol_name, values in results.items():
        print(f"{protocol_name}: {values}")


def plot_results(results: dict[str, list[float]]) -> None:
    plot_styles = {
        "GRR": {"color": "purple", "marker": "o"},
        "RAPPOR": {"color": "grey", "marker": "s"},
        "OUE": {"color": "blue", "marker": "x"},
        "OLH": {"color": "yellow", "marker": "x"},
    }

    plt.rcParams.update({"font.size": 12})
    plt.figure(figsize=(4 * 1.33, 4 * 1.33))

    for protocol_name, values in results.items():
        style = plot_styles[protocol_name]

        plt.plot(
            EPSILON_VALUES,
            values,
            linewidth=2,
            color=style["color"],
            marker=style["marker"],
            markersize=10,
            mew=1.5,
            fillstyle="none",
            clip_on=False,
            label=protocol_name,
        )

    plt.xticks(fontsize=15)
    plt.title(DATASET_NAME)
    plt.ylabel(METRIC_TYPE)
    plt.xlabel("Epsilon Values")
    plt.grid(linestyle=":")
    plt.legend(prop={"size": 12}, ncol=2, columnspacing=0.75)

    plt.savefig(OUTPUT_PLOT_PATH, format="png", dpi=300, bbox_inches="tight")
    plt.show()


def main() -> None:
    user_trajectories = read_dataset(DATASET_PATH)

    tracemalloc.start()
    start_time = time.time()

    results = run_experiment(user_trajectories)

    elapsed_time = time.time() - start_time
    memory_mb = get_memory_usage_mb()

    print_results(results, elapsed_time, memory_mb)
    plot_results(results)

    tracemalloc.stop()


if __name__ == "__main__":
    main()

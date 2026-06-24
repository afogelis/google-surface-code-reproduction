"""Figure generation for the Google reproduction."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from .experiments import CycleErrorResult
from .noise import PUBLISHED_LOGICAL_ERROR_PER_CYCLE, PUBLISHED_LOGICAL_ERROR_UNCERTAINTY


def plot_fidelity_decay(results: Sequence[CycleErrorResult], *, ax: Axes | None = None) -> Axes:
    """Logical error probability vs number of rounds, one curve per distance.

    Reproduces the qualitative content of the experiment's fidelity-decay figure:
    error accumulates with rounds, and a larger distance accumulates it more
    slowly when operating below threshold.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 5))
    for result in sorted(results, key=lambda r: r.distance):
        ax.plot(
            result.rounds,
            result.logical_error_rates,
            marker="o",
            label=f"d = {result.distance} (eps = {result.epsilon:.4f})",
        )
    ax.set_xlabel("Number of rounds N")
    ax.set_ylabel("Logical error probability")
    ax.set_title("Logical error vs rounds (Google reproduction)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return ax


def plot_epsilon_vs_distance(
    results: Sequence[CycleErrorResult],
    *,
    show_published: bool = True,
    ax: Axes | None = None,
) -> Axes:
    """Logical error per cycle vs code distance, with published points overlaid."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 5))

    ordered = sorted(results, key=lambda r: r.distance)
    distances = [r.distance for r in ordered]
    epsilons = [r.epsilon for r in ordered]
    ax.plot(distances, epsilons, marker="s", label="simulation (this work)")

    if show_published:
        pub_d = sorted(PUBLISHED_LOGICAL_ERROR_PER_CYCLE)
        pub_eps = [PUBLISHED_LOGICAL_ERROR_PER_CYCLE[d] for d in pub_d]
        pub_err = [PUBLISHED_LOGICAL_ERROR_UNCERTAINTY[d] for d in pub_d]
        ax.errorbar(
            pub_d,
            pub_eps,
            yerr=pub_err,
            marker="D",
            linestyle="--",
            capsize=4,
            label="Google Nature 2023 (experiment)",
        )

    ax.set_yscale("log")
    ax.set_xlabel("Code distance d")
    ax.set_ylabel("Logical error per cycle (epsilon)")
    ax.set_title("Logical error per cycle vs distance")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    return ax

"""Extract logical error per cycle, the central quantity of the Google experiment.

The experiment characterises a logical qubit by its *logical error per cycle*
(epsilon): the probability that the logical state is corrupted in one round of
error correction. It is extracted from how the logical fidelity decays with the
number of rounds N:

    1 - 2 * p_fail(N) = (1 - 2 * epsilon) ** N

so a linear fit of ``log(1 - 2 p_fail)`` against ``N`` (through the origin) gives
``epsilon``. We run the companion simulator at several round counts and fit.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from surfacecode.experiment import run_memory_experiment
from surfacecode.types import ExperimentConfig


@dataclass(frozen=True)
class CycleErrorResult:
    """Fitted logical error per cycle at one code distance."""

    distance: int
    physical_error_rate: float
    epsilon: float
    rounds: tuple[int, ...]
    logical_error_rates: tuple[float, ...]


def extract_logical_error_per_cycle(
    *,
    distance: int,
    physical_error_rate: float,
    rounds: Sequence[int] = (1, 3, 5, 7, 9, 13, 17, 21, 25),
    shots: int = 40_000,
    basis: str = "Z",
    seed: int | None = 2023,
) -> CycleErrorResult:
    """Fit epsilon from logical failure probability vs number of rounds."""
    measured_rounds: list[int] = []
    logical_rates: list[float] = []
    for round_count in rounds:
        config = ExperimentConfig(
            distance=distance,
            rounds=round_count,
            p=physical_error_rate,
            shots=shots,
            basis=basis,  # type: ignore[arg-type]
            seed=seed,
        )
        result = run_memory_experiment(config)
        measured_rounds.append(round_count)
        logical_rates.append(result.logical_error_rate)

    epsilon = _fit_epsilon(np.asarray(measured_rounds), np.asarray(logical_rates))
    return CycleErrorResult(
        distance=distance,
        physical_error_rate=physical_error_rate,
        epsilon=epsilon,
        rounds=tuple(measured_rounds),
        logical_error_rates=tuple(logical_rates),
    )


def _fit_epsilon(rounds: np.ndarray, logical_rates: np.ndarray) -> float:
    """Linear fit of log(1 - 2 p_fail) vs rounds through the origin -> epsilon."""
    decay = 1.0 - 2.0 * np.clip(logical_rates, 0.0, 0.4999)
    log_decay = np.log(decay)
    # Slope through origin: sum(N*y)/sum(N*N).
    slope = float(np.sum(rounds * log_decay) / np.sum(rounds * rounds))
    return 0.5 * (1.0 - np.exp(slope))


def lambda_factor(epsilon_low: float, epsilon_high: float) -> float:
    """Error-suppression factor Lambda = epsilon(d) / epsilon(d+2).

    Lambda > 1 means increasing the distance suppresses logical errors (below
    threshold); Lambda ~ 1 is the near-threshold regime the experiment operated in.
    """
    if epsilon_high <= 0.0:
        return float("inf")
    return epsilon_low / epsilon_high

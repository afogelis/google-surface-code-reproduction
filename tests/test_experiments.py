import numpy as np

from grepro.experiments import (
    _fit_epsilon,
    extract_logical_error_per_cycle,
    lambda_factor,
)
from grepro.noise import GoogleNoiseParams


def test_fit_recovers_known_epsilon():
    true_epsilon = 0.02
    rounds = np.array([1, 3, 5, 9, 15, 25])
    decay = (1.0 - 2.0 * true_epsilon) ** rounds
    p_fail = 0.5 * (1.0 - decay)
    recovered = _fit_epsilon(rounds, p_fail)
    assert abs(recovered - true_epsilon) < 1e-6


def test_effective_rate_is_within_component_range():
    params = GoogleNoiseParams()
    effective = params.effective_depolarizing_rate()
    assert params.single_qubit_gate <= effective <= params.measurement


def test_extract_epsilon_below_threshold_is_small_and_positive():
    result = extract_logical_error_per_cycle(
        distance=3, physical_error_rate=0.004, rounds=(1, 3, 5, 9), shots=4000, seed=1
    )
    assert 0.0 < result.epsilon < 0.1


def test_distance_suppresses_epsilon_below_threshold():
    eps3 = extract_logical_error_per_cycle(
        distance=3, physical_error_rate=0.003, rounds=(1, 3, 5, 9, 13), shots=20000, seed=7
    ).epsilon
    eps5 = extract_logical_error_per_cycle(
        distance=5, physical_error_rate=0.003, rounds=(1, 3, 5, 9, 13), shots=20000, seed=7
    ).epsilon
    assert lambda_factor(eps3, eps5) > 1.0

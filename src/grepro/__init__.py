"""Simulation reproduction of Google Quantum AI's 2023 surface-code experiment."""

from .experiments import (
    CycleErrorResult,
    extract_logical_error_per_cycle,
    lambda_factor,
)
from .noise import (
    PUBLISHED_LOGICAL_ERROR_PER_CYCLE,
    GoogleNoiseParams,
)

__version__ = "0.1.0"

__all__ = [
    "CycleErrorResult",
    "GoogleNoiseParams",
    "PUBLISHED_LOGICAL_ERROR_PER_CYCLE",
    "extract_logical_error_per_cycle",
    "lambda_factor",
]

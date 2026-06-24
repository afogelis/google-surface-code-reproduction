"""Noise parameters for the Google surface-code reproduction.

Google's experiment (Nature 2023) is driven by per-component error rates: single-
and two-qubit gate errors, measurement and reset errors, and data-qubit idling.
Our simulator (the companion ``surface-code-simulator``) uses a single uniform
circuit-level depolarizing rate. To bridge the two we collapse the published
component rates into one effective rate via a simple weighted mean.

This is an approximation, not a faithful copy of the device noise. The component
figures below are representative order-of-magnitude values from the paper and its
supplement; the goal is to reproduce the *scaling behaviour* (how logical error
changes with code distance), not the exact device calibration. Values that we are
not confident citing precisely are flagged in the technical report.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class GoogleNoiseParams(BaseModel):
    """Representative per-component error rates (approximate, from Nature 2023)."""

    model_config = {"frozen": True}

    single_qubit_gate: float = Field(default=0.001, ge=0.0)
    two_qubit_gate: float = Field(default=0.006, ge=0.0)
    measurement: float = Field(default=0.02, ge=0.0)
    reset: float = Field(default=0.002, ge=0.0)
    data_idle: float = Field(default=0.003, ge=0.0)

    def effective_depolarizing_rate(self) -> float:
        """Collapse component rates into one uniform circuit-level rate.

        The two-qubit-gate and measurement errors dominate the surface-code cycle,
        so the mean is weighted towards them. The result is intended only to place
        the simulation in the same below-threshold regime as the experiment.
        """
        weights = {
            "single_qubit_gate": 1.0,
            "two_qubit_gate": 4.0,
            "measurement": 2.0,
            "reset": 1.0,
            "data_idle": 2.0,
        }
        total_weight = sum(weights.values())
        weighted = (
            weights["single_qubit_gate"] * self.single_qubit_gate
            + weights["two_qubit_gate"] * self.two_qubit_gate
            + weights["measurement"] * self.measurement
            + weights["reset"] * self.reset
            + weights["data_idle"] * self.data_idle
        )
        return weighted / total_weight


# Published logical error per cycle (Google Quantum AI, Nature 2023, Fig. 3):
# distance-3 ensemble vs distance-5, both near 3%.
PUBLISHED_LOGICAL_ERROR_PER_CYCLE: dict[int, float] = {3: 0.03028, 5: 0.02914}
PUBLISHED_LOGICAL_ERROR_UNCERTAINTY: dict[int, float] = {3: 0.00023, 5: 0.00016}

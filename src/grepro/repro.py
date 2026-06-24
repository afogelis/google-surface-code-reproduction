"""Reproduce the Google surface-code scaling result and write the report.

grepro            # run with defaults, write figures/ and reports/
grepro --p 0.004 --shots 40000
"""

from __future__ import annotations

import argparse
import os
from collections.abc import Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .experiments import CycleErrorResult, extract_logical_error_per_cycle, lambda_factor
from .figures import plot_epsilon_vs_distance, plot_fidelity_decay
from .noise import (
    PUBLISHED_LOGICAL_ERROR_PER_CYCLE,
    GoogleNoiseParams,
)


def run_reproduction(*, p: float, shots: int, seed: int = 2023) -> list[CycleErrorResult]:
    """Extract logical error per cycle for distances 3, 5 and 7."""
    return [
        extract_logical_error_per_cycle(distance=d, physical_error_rate=p, shots=shots, seed=seed)
        for d in (3, 5, 7)
    ]


def _build_report(results: list[CycleErrorResult], *, p: float, effective_p: float) -> str:
    by_distance = {r.distance: r for r in results}
    lam_35 = lambda_factor(by_distance[3].epsilon, by_distance[5].epsilon)
    lam_57 = lambda_factor(by_distance[5].epsilon, by_distance[7].epsilon)

    sim_rows = "\n".join(
        f"| {r.distance} | {r.epsilon:.4f} | "
        f"{PUBLISHED_LOGICAL_ERROR_PER_CYCLE.get(r.distance, float('nan')):.4f} |"
        for r in sorted(results, key=lambda r: r.distance)
    )

    return f"""# Reproducing Google's Surface-Code Scaling Experiment (Nature 2023)

A simulation reproduction of *Suppressing quantum errors by scaling a surface code logical qubit*
(Google Quantum AI, Nature 2023), focused on the central claim: increasing the code distance
suppresses the logical error per cycle.

## What is and is not reproduced

This is a **simulation** reproduction, not a hardware one. We reproduce:

- the experiment's **methodology** -- extracting logical error per cycle (epsilon) from the decay of
  logical fidelity with the number of rounds;
- the experiment's **central scaling claim** -- that below threshold, a larger code distance lowers
  epsilon (the suppression factor Lambda > 1).

We do **not** reproduce the device-specific absolute numbers, because we use a single uniform
circuit-level depolarizing model rather than Google's calibrated per-component noise. The published
values are shown alongside ours for context only.

## Method

Logical error per cycle is extracted by fitting

    1 - 2 p_fail(N) = (1 - 2 epsilon) ** N

over round counts N, using the companion `surface-code-simulator` (Stim + MWPM) to measure
p_fail(N). We run distances d = 3, 5, 7 at a representative below-threshold physical error rate
p = {p:.4f}.

A weighted mean of representative Google component error rates gives an effective uniform rate of
**{effective_p:.4f}**, which sits close to this simplified model's threshold (~0.6%). That the
experiment operates near threshold is itself consistent with the *modest* distance-5 improvement
reported in the paper.

## Results

Simulated logical error per cycle, with the published experimental values for context:

| distance d | epsilon (simulation) | epsilon (Google, experiment) |
|-----------|----------------------|------------------------------|
{sim_rows}

Error-suppression factors (Lambda > 1 means larger distance helps):

- Lambda(3 -> 5) = {lam_35:.3f}
- Lambda(5 -> 7) = {lam_57:.3f}

Below threshold the simulation reproduces the qualitative result of the paper: increasing the code
distance suppresses the logical error per cycle. Near threshold the suppression becomes marginal
(Lambda -> 1), mirroring why the experimental distance-5 logical qubit only modestly outperformed
the distance-3 ensemble.

## Figures

- `figures/fidelity_decay.png` -- logical error vs number of rounds per distance.
- `figures/epsilon_vs_distance.png` -- logical error per cycle vs distance, with published points.

## Limitations

- Uniform depolarizing noise replaces Google's calibrated component model, so absolute epsilon
  values are not expected to match the experiment.
- Leakage, crosstalk and non-Markovian effects present in hardware are not modelled.
- MWPM is used as the decoder; the paper also studied more advanced decoders.

## References

Google Quantum AI. Suppressing quantum errors by scaling a surface code logical qubit. Nature 2023;
614:676-681.

Fowler AG, Mariantoni M, Martinis JM, Cleland AN. Surface codes: Towards practical large-scale
quantum computation. Physical Review A 2012; 86:032324.
"""


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grepro", description=__doc__)
    parser.add_argument(
        "--p", type=float, default=0.004, help="Below-threshold physical error rate."
    )
    parser.add_argument("--shots", type=int, default=40_000)
    parser.add_argument("--seed", type=int, default=2023)
    parser.add_argument("--figures-dir", type=str, default="figures")
    parser.add_argument("--reports-dir", type=str, default="reports")
    args = parser.parse_args(argv)

    os.makedirs(args.figures_dir, exist_ok=True)
    os.makedirs(args.reports_dir, exist_ok=True)

    results = run_reproduction(p=args.p, shots=args.shots, seed=args.seed)

    ax = plot_fidelity_decay(results)
    ax.figure.tight_layout()
    ax.figure.savefig(os.path.join(args.figures_dir, "fidelity_decay.png"), dpi=150)
    plt.close(ax.figure)

    ax = plot_epsilon_vs_distance(results)
    ax.figure.tight_layout()
    ax.figure.savefig(os.path.join(args.figures_dir, "epsilon_vs_distance.png"), dpi=150)
    plt.close(ax.figure)

    effective_p = GoogleNoiseParams().effective_depolarizing_rate()
    report = _build_report(results, p=args.p, effective_p=effective_p)
    report_path = os.path.join(args.reports_dir, "TECHNICAL_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write(report)

    for result in results:
        print(f"d={result.distance}: epsilon={result.epsilon:.4f}")
    print(f"wrote figures to {args.figures_dir}/ and report to {report_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

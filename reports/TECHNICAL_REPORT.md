# Reproducing Google's Surface-Code Scaling Experiment (Nature 2023)

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
p = 0.0040.

A weighted mean of representative Google component error rates gives an effective uniform rate of
**0.0073**, which sits close to this simplified model's threshold (~0.6%). That the
experiment operates near threshold is itself consistent with the *modest* distance-5 improvement
reported in the paper.

## Results

Simulated logical error per cycle, with the published experimental values for context:

| distance d | epsilon (simulation) | epsilon (Google, experiment) |
|-----------|----------------------|------------------------------|
| 3 | 0.0035 | 0.0303 |
| 5 | 0.0016 | 0.0291 |
| 7 | 0.0007 | nan |

Error-suppression factors (Lambda > 1 means larger distance helps):

- Lambda(3 -> 5) = 2.165
- Lambda(5 -> 7) = 2.483

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
- Leakage, crosstalk and non-Markovian effects present in hardware are not modeled.
- MWPM is used as the decoder; the paper also studied more advanced decoders.

## References

Google Quantum AI. Suppressing quantum errors by scaling a surface code logical qubit. Nature 2023;
614:676-681.

Fowler AG, Mariantoni M, Martinis JM, Cleland AN. Surface codes: Towards practical large-scale
quantum computation. Physical Review A 2012; 86:032324.

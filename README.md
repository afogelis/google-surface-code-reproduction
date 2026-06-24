# Google Surface-Code Reproduction

A **simulation** reproduction of Google Quantum AI's 2023 result
*Suppressing quantum errors by scaling a surface code logical qubit* (Nature 614:676-681). It
reproduces the experiment's methodology and central scaling claim: below threshold, increasing the
code distance suppresses the logical error per cycle.

This is repo 6 (capstone A) of a seven-part [QEC research portfolio](../README.md) and builds on
[`surface-code-simulator`](https://github.com/afogelis/surface-code-simulator).

## What is and is not reproduced

- **Reproduced:** the extraction of *logical error per cycle* (epsilon) from logical-fidelity decay
  with the number of rounds, and the qualitative scaling -- larger distance, smaller epsilon
  (suppression factor Lambda > 1) -- plus the near-threshold regime where the improvement is modest.
- **Not reproduced:** the device-specific absolute error rates. We use a single uniform
  circuit-level depolarizing model, not Google's calibrated per-component noise, so the published
  values (~3.0% per cycle) are shown for context only, not as a target to hit.

This honest scoping is deliberate: a full hardware reproduction is impossible without the device,
so the value is in reproducing the *analysis and the physics conclusion*.

## What this demonstrates

- Reading a landmark experimental paper and re-deriving its key quantity in simulation.
- Rigorous methodology: fitting epsilon from fidelity decay, computing the Lambda suppression factor.
- Scientific honesty about the boundary between what simulation can and cannot reproduce.

## Install and run

```bash
pip install -e ".[dev]"
pytest
grepro --p 0.004 --shots 40000     # writes figures/ and reports/TECHNICAL_REPORT.md
```

## Outputs

- [`reports/TECHNICAL_REPORT.md`](reports/TECHNICAL_REPORT.md) — full write-up with results table, Lambda factors, caveats and references.
- `figures/fidelity_decay.png` — logical error vs rounds per distance.
- `figures/epsilon_vs_distance.png` — logical error per cycle vs distance, with the published points overlaid.

## Method (one paragraph)

Logical error per cycle is extracted by fitting `1 - 2 p_fail(N) = (1 - 2 epsilon)^N` over round
counts `N`, with `p_fail(N)` measured by Stim + MWPM via the companion simulator. Running distances
3, 5 and 7 below threshold yields the suppression factor `Lambda = epsilon(d)/epsilon(d+2)`.

## References

- Google Quantum AI. Suppressing quantum errors by scaling a surface code logical qubit. Nature 2023; 614:676-681.
- Fowler AG, Mariantoni M, Martinis JM, Cleland AN. Surface codes: Towards practical large-scale quantum computation. Physical Review A 2012; 86:032324.

## License

MIT — see [LICENSE](LICENSE).

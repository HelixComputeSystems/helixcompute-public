# ER-11 — governed-validation wall time

> **Release status:** `PUBLIC_RELEASE`

> **Measurement:** `MEASURED — GOVERNED VALIDATION PHASE`

> **Frozen verdict:** `MIXED`; qualification `FAIL`

At approximately `0.1%` affected scope, the experiment's specific frozen
canonical FULL route took `90.385×–93.327×` as long in governed validation as
the experimental Helix route across 44,224-, 250,000-, and 1,000,000-row
deterministic in-memory estates.

The corresponding predeclared FULL/Helix route-total range was
`3.421×–3.534×`. Governed validation is a bounded phase; route totals are
defined phase sums. Neither metric is end-to-end transaction or outer-worker
latency.

## Measurement protocol

Each published cell used one warmup followed by three sequential measured
transitions in fresh, non-overlapping route workers, beginning from retained
prepared state. Ratios are inverses of arithmetic-mean `perf_counter_ns`
samples.

FULL is one exact frozen Python canonical scan/hash/equality route. It is not an
optimized database or a universal full-computation baseline. See
[methodology](methodology.md) for the accounting boundary.

## Exactness and qualification

Across the complete frozen qualification, both routes were exact and validated
on the same 36 unique measured transitions (`36/36` each). Separately,
`333/333` mediated residual units were recorded as exactly localized and
repaired in dedicated correctness cells; those units were not present in the
published clean timing cells.

The median sparse Helix/FULL incremental-RSS ratio was
`1.5065586419753085`, above the frozen `1.50` ceiling. The memory gate and
overall qualification failed, the experiment remained `MIXED`, and the final
campaign was not run.

The measured advantage declined as affected scope increased. This release does
not publish a universal performance curve, crossover point, or routing rule.

## Threat and verification boundary

The supported model requires mediated authenticated updates or a separate
independent detector for out-of-model state mutation. The private
counterexample and attack construction are not published.

Run `python verify.py` to check this package's manifest, raw published samples,
arithmetic, exactness counters, RSS gate, and frozen verdict. The verifier does
not execute Helix or independently recompute semantic equality from unpublished
outputs.

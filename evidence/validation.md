# Governed-validation wall time

**Claim ID:** `ER-11`

**Evidence class:** `MEASURED — GOVERNED VALIDATION PHASE`

**Frozen verdict:** `MIXED`; qualification `FAIL`

At approximately `0.1%` affected scope, the frozen canonical FULL route's
governed-validation wall time was `90.385×–93.327×` the experimental Helix
route's across 44,224-, 250,000-, and 1,000,000-row deterministic in-memory
estates.

The corresponding predeclared FULL/Helix route-total range was
`3.421×–3.534×`. Governed validation is a bounded phase; route totals are
defined phase sums. Neither is end-to-end transaction or outer-worker latency.

[Inspect the ER-11 receipt →](releases/v1/receipts/ER-11-governed-validation/README.md)

## Protocol and comparator

Each published cell used one warmup followed by three sequential measured
transitions in fresh, non-overlapping route workers, beginning from retained
prepared state. Ratios are inverses of arithmetic-mean `perf_counter_ns`
samples.

FULL means the experiment's specific frozen Python canonical route, which
serializes and SHA-256-hashes every canonical row for both states and checks
complete state-array equality. It is not an optimized database or a universal
full-computation baseline.

## Exactness and frozen outcome

Across the complete frozen qualification, the same 36 unique measured
transitions were exercised by both routes; each route was exact and validated
`36/36`. Separately, `333/333` mediated residual units were recorded as exactly
localized and repaired in dedicated correctness cells. Those cells are not the
published clean timing cells.

The median sparse Helix/FULL incremental-RSS ratio was
`1.5065586419753085`, above the frozen `1.50` ceiling. The memory gate and
overall qualification failed, the experiment remained `MIXED`, and the final
campaign was not run.

The measured validation advantage declined as affected scope increased. This
release does not publish a universal crossover curve or routing threshold.

The supported threat boundary requires mediated authenticated updates or a
separate independent detector for out-of-model state mutation. The public
receipt publishes the boundary, not the private counterexample or attack
construction.

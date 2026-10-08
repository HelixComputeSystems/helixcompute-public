# ER-11 methodology and accounting boundary

This receipt reports a frozen bounded qualification. No benchmark was rerun.

Each published approximately-0.1% cell used one warmup and then three
sequential measured transitions in a fresh FULL worker and a separate fresh
Helix worker. The compared statistic is the arithmetic mean of three
`perf_counter_ns` governed-validation samples. Measurement begins from retained
prepared state.

## Canonical FULL comparator

FULL is the experiment's specific frozen Python route. It serializes and
SHA-256-hashes every canonical row for both states and checks complete
state-array equality. It is not an optimized database, vectorized validator,
or general full-recomputation baseline.

## Governed validation includes

- admission and governance checks;
- validation of the declared successor obligation;
- integrity-state update and consistency checks;
- candidate acceptance or promotion; and
- ordinary in-call Python and result-assembly overhead.

## Governed validation excludes

- initial retained-state preparation;
- upstream change discovery and transition materialization;
- authority and receiver reconstruction;
- the independent post-decision FULL examiner used for experimental scoring;
- process launch, handshake, monitoring, and output serialization; and
- persistence, network, storage, and external-system integration.

The independent examiner was interleaved between measured transitions and may
have affected cache state. The adjacent route totals are predeclared phase
sums that include prepared route setup, input materialization, warmup, and
measured calls while still excluding the independent examiner, process
overhead, persistence, network, and external I/O. They are not contiguous
outer-worker stopwatch latency.

## Correctness and disclosure

The `36/36` exactness result covers both routes across the complete frozen
qualification. The `333/333` localization-and-repair result comes from separate
mediated correctness cells. This receipt publishes aggregate counters, not the
private residual construction, validation machinery, or complete output pairs.

The public package therefore verifies the recorded result but cannot
independently recompute semantic equality or reproduce the experiment.

## Frozen outcome

The governed-validation wall and correctness gates passed. The incremental-RSS
gate failed at `1.5065586419753085 > 1.50`; overall qualification failed, the
experiment remained `MIXED`, and the final campaign was not run.

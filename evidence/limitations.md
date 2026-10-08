# Release-wide limitations

- Receipt verification checks the released record; it does not execute Helix
  Core or independently reproduce the experiments.
- Exactness is bounded to the stated fixtures and equality contracts.
- Logical transform counts are not total work, CPU, elapsed time, I/O, memory,
  or cost.
- Application-payload bytes are not network-wire bytes, cloud egress, or
  latency.
- Retained file bytes are not device writes, cloud cost, latest-only storage,
  or a universal smallest-encoding claim.
- The one-million-row results are representation-isolated; no behavior above
  one million rows or production memory behavior is claimed.
- Results from sparse/local workloads do not make sparse physical mutation the
  conceptual definition of Helix.
- FULL can be the correct route when retained validity or locality no longer
  pays. No public universal crossover threshold is claimed.
- `ER-11` is governed-validation wall time against one specific frozen Python
  canonical comparator, not end-to-end transaction latency or a database
  benchmark.
- `ER-11` used one warmup and three sequential measurements per published cell
  on one host. Its adjacent route totals were only `3.421×–3.534×` at the
  advertised approximately-0.1% scope.
- Experiment 4.1 remained `MIXED`: its incremental-RSS gate failed at
  `1.5065586419753085 > 1.50`, and the final campaign was not run.
- The public `ER-11` receipt verifies recorded exactness counters but cannot
  independently recompute semantic equality without unpublished outputs.
- No private implementation, representation layout, routing rule, proof or
  authentication mechanism, repair method, attack construction, or research
  lineage is licensed or disclosed by these receipts.

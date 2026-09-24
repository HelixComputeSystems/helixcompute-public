# Helix Compute — Public Evidence

This directory summarizes bounded experiments supporting the public Helix measurements.

These summaries describe:

- what was tested;
- what was measured;
- what comparison was used;
- what result was observed; and
- where the result stopped holding.

These summaries report measured outcomes and experimental boundaries without publishing implementation details.

## Evidence index

- [Transport](transport.md) — application payload bytes delivered to a separate receiver.
- [Historical storage](historical-storage.md) — retained file bytes for reconstructable history.
- [Scaling](scaling.md) — sparse-change measurements from 44,224 through 1,000,000 rows.
- [Boundaries and negative results](boundaries.md) — dense change, latest-state-only storage, lean incremental history, compression, and deduplication.

## Measurement language

**Measured** means directly observed within the stated experiment boundary: application payload bytes, retained file lengths, exact reconstruction results, and timing only where a summary explicitly reports it.

**Projected** means an arithmetic or economic calculation derived from measured byte reductions and separately published pricing. No projected cloud bill appears in these evidence summaries.

Every accepted reconstruction in the cited validation campaigns was exact. Rejected invalid inputs are reported as rejections, not as successful reconstructions. Results are bounded to the workloads, representations, and accounting rules described on each page.

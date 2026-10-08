# Methodology and accounting boundary

The source history contained 1,027,734 rows. Ten deterministic synthetic rows
were appended, producing a 1,027,744-row target. FULL applied one rolling
transform for every target historian row. The selective route applied one
rolling transform for every row in its single affected feature partition,
which contained 173 rows.

## Comparator, counter, and exactness scope

FULL applied the same Python rolling operator across the complete target state;
it was not an independently optimized historian or database comparator. The
recorded transform counts were derived from adapter loop coverage, not from
independent instrumentation of total CPU, I/O, memory, or end-to-end work.

The FULL and selective routes shared the workload operator. Their matching
canonical digests establish equality under the frozen benchmark contract, but
they are not validation against an external semantic oracle.

## Included

- FULL target-row rolling transforms;
- selective affected-partition rolling transforms; and
- the frozen equivalence-gate and canonical-digest result.

## Excluded

- source loading and canonical preparation;
- mutation and upstream change discovery;
- change-obligation resolution;
- retained-state maintenance, successor application, downstream summary work,
  and telemetry;
- equality validation cost, serialization, persistence, network, memory, CPU
  instructions, and elapsed time.

## Unknown

Total CPU work, end-to-end latency, and production economics are not
established by this counter.

## Provenance limitation

The execution worktree was dirty and content binding was partial: 28/28
enumerated files matched, but one dirty imported file and the
interpreter/third-party binaries were not contemporaneously content-bound.
The public verifier cannot turn these opaque runtime-byte commitments into a
clean-clone source binding.

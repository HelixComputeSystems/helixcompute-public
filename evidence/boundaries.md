# Claim boundaries

These limitations define what the public measurements mean. The private
research record contains additional negative results and experimental detail;
those materials are not required to substantiate the released claims.

## Work avoided is not automatically time saved

`ER-03` counts workload-defined rolling-row transforms. It does not count total
operations, elapsed time, CPU, I/O, memory, or cost.

## Representation bytes are not infrastructure bills

`ER-04` measures compressed application payload, not physical wire traffic or
cloud egress. `ER-05` measures retained application-file bytes for
reconstructable history, not device writes, cloud cost, latest-only retention,
or the smallest possible incremental encoding.

## Locality has an economic boundary

Helix does not claim that selective representation always wins. In a tested
dense condition, FULL was the smaller exact transport representation. No
universal crossover threshold is claimed or published.

The byte claims also do not establish that the same advantage survives every
downstream deduplication, compression, or storage stack.

## Scale evidence is isolated

`ER-06` reports representation-isolated one-million-row evidence. It is not a
successful combined production qualification, a memory-efficiency claim, or a
scaling law.

## Validation time is a phase measurement

`ER-11` compares governed-validation wall time against one frozen canonical
FULL comparator. It is not end-to-end latency. The complete frozen experiment
remained `MIXED`, failed its incremental-memory gate, and did not advance to
the final campaign.

Its supported threat model requires mediated authenticated updates or an
independent detector for out-of-model state mutation.

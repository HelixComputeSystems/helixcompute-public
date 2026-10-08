# Methodology

## Frozen evidence only

Evidence Release v1 packages results from completed, frozen campaigns. No
campaign was rerun, no gate was moved, and no private verdict was rewritten for
this release.

## Comparison discipline

Every receipt names its comparator and unit. Ratio direction is explicit, such
as `expanded FULL bytes / Helix bytes` or `FULL governed-validation wall /
Helix governed-validation wall`.

The release does not infer latency, CPU, physical network traffic, device
writes, cloud cost, or production economics from logical-work or
representation-byte measurements.

## Exactness

Exactness statements are bounded to their frozen fixture and equality
contract. A recorded digest or exactness counter does not establish universal
semantic correctness. Where complete outputs are not public, the verifier can
check the published record but cannot independently re-hash the original
outputs.

## Wall-time claim

`ER-11` is the only public wall-time claim. It covers a governed-validation
phase from retained prepared state. Each published cell used one warmup and
three sequential `perf_counter_ns` measurements per route in fresh,
non-overlapping workers. The comparator is one specific frozen Python
canonical scan/hash/equality route. Its adjacent route totals are defined phase
sums; neither measure is end-to-end transaction latency.

The receipt publishes the full accounting boundary needed to interpret the
claim while withholding private validation, proof, routing, and repair
implementation.

## Sanitization and authority binding

Each receipt carries opaque SHA-256 commitments to its controlling frozen
private authority bundle. Detailed filenames, private locations, source
identities, commits, and laboratory maps remain private. The public verifier
binds the sanitized package; it cannot dereference or re-hash private source
material.

## Verification and authenticity

Per-receipt verifiers use the Python standard library. The root verifier checks
claim bindings, arithmetic, manifest closure, and receipt execution. SHA-256
manifests detect byte drift; they are not signatures.

Evidence Release v1 was committed atomically and is identified by the immutable
`evidence-v1.0.0` tag. Every status-bearing artifact carries
`PUBLIC_RELEASE`; the tag and manifests bind the published bytes.

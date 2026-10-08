# ER-03 — Kraken rolling-row-transform count

**Release status:** `PUBLIC_RELEASE`

**Evidence class:** MEASURED

**Reproduction level:** `RECEIPT_VERIFICATION`

In the frozen 1,027,744-row historian fixture, FULL recorded 1,027,744
workload-defined rolling-row transforms and Helix recorded 173. The frozen
benchmark recorded matching complete canonical output digests and a passing
equivalence gate. FULL therefore performed approximately 5,941× as many of
these transforms; Helix performed 99.983% fewer.

The counts are not total work. They exclude source loading and preparation,
upstream change discovery, change-obligation resolution, retained-state
maintenance, validation, serialization, persistence, networking, and elapsed
time.

Run `python verify.py` in this directory to verify the package hash manifest,
count arithmetic, and recorded digest equality. The command does not rerun the
million-row workload or independently re-hash its unpublished outputs.

## Provenance limitation

The execution worktree was dirty and content binding was partial: 28/28
enumerated files matched, but one dirty imported file and the
interpreter/third-party binaries were not contemporaneously content-bound.
The private hashes are runtime-byte commitments, not a clean-clone source or
artifact-commit binding.

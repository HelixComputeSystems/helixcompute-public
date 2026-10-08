# Helix Compute — Public Evidence

> **Release status: `PUBLIC_RELEASE` — `evidence-v1.0.0`**

## Do More With Less Data.

**Keep what remains valid. Process what changed.**

Helix reduces repeated work when established state, validity, or derivable
structure survives a transition. This repository contains bounded measurement
receipts for that claim. It publishes evidence—not Helix Core or the private
research program that produced it.

## Strongest measured findings

| Finding | Measurement | Receipt |
| --- | --- | --- |
| **`1,027,744 → 173`** | **MEASURED LOGICAL WORK** — FULL performed approximately `5,941×` as many workload-defined rolling-row transforms; Helix performed `99.983%` fewer, with identical recorded canonical output | [`ER-03`](evidence/releases/v1/receipts/ER-03-kraken-transform-count/README.md) |
| **`90.4×–93.3×`** | **MEASURED GOVERNED-VALIDATION WALL** — the frozen canonical FULL route took this many times as long as the experimental Helix route at approximately `0.1%` affected scope | [`ER-11`](evidence/releases/v1/receipts/ER-11-governed-validation/README.md) |
| **Up to `7.939×`** | **MEASURED APPLICATION PAYLOAD** — expanded FULL bytes divided by Helix bytes in the tested sparse/local transport campaigns | [`ER-04`](evidence/releases/v1/receipts/ER-04-transport/README.md) |
| **Up to `6.774×`** | **MEASURED RETAINED HISTORY** — expanded FULL bytes divided by Helix bytes for tested reconstructable histories | [`ER-05`](evidence/releases/v1/receipts/ER-05-historical-storage/README.md) |

These are comparator-specific results. In a separately tested dense transport
condition, FULL was the smaller exact representation. In the history campaign,
a competent incremental comparator retained fewer application-file bytes than
Helix but did not carry identical authority semantics. No universal crossover
threshold or smallest-encoding claim is made.

Supporting evidence includes representation-isolated measurements through one
million rows with exact fresh-process reconstruction checks. See
[`ER-06`](evidence/releases/v1/receipts/ER-06-scaling/README.md).

## Read the receipts

Each receipt identifies the measured unit, comparator, conditions, exactness
scope, accounting boundary, and material limitations. The ER-11 result is a
validation-phase measurement—not an end-to-end transaction speedup—and its
technical receipt preserves the `MIXED` verdict and failed memory gate.

Start with the [evidence front door](evidence/README.md), inspect the
[machine-readable claim index](evidence/claims-v1.json), then run:

```text
python evidence/verify.py
```

That command verifies the published hashes, claim bindings, and arithmetic. It
does not execute Helix or independently reproduce the private experiments.

## Commercial boundary

The public release contains only the evidence needed to substantiate these
claims. Private implementations, routing logic, crossover research,
representation layouts, proof machinery, optimization work, attack methods,
and research failures remain private.

Helix does not claim to win on every workload. FULL remains the correct route
when retained validity or locality does not pay. See [claim
boundaries](evidence/boundaries.md) and [limitations](evidence/limitations.md).

## Public surfaces

- [Website](https://www.helixcompute.io/)
- [Evidence index](evidence/README.md)
- [Methodology](evidence/methodology.md)
- [Verification levels](evidence/reproduction-levels.md)

## Usage terms

Licensing is assigned file by file. See [LICENSE.md](LICENSE.md), the
[machine-readable scope](LICENSES/scope.json), and [USAGE.md](USAGE.md).
Nothing in this release grants rights to Helix Core or any private technology.

Copyright © 2026 Helix Compute Systems. Files not expressly licensed are all
rights reserved.

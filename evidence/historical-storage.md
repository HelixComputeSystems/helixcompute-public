# Reconstructable historical storage

**Claim ID:** `ER-05`

**Receipt:** [ER-05 historical storage](releases/v1/receipts/ER-05-historical-storage/README.md)

## What was measured

Three independently seeded deterministic generated histories each retained 40
sparse/local transitions. The comparison retained either a compressed expanded
FULL representation for every generation or periodic complete snapshots plus
Helix reconstruction artifacts.

| Snapshot interval | Expanded FULL history bytes / Helix bytes |
| --- | ---: |
| Every 5 transitions | `4.028407×–4.120915×` |
| Every 10 transitions | `6.527575×–6.774060×` |

Across the tested representations and policies, all 135 scheduled
fresh-process reconstructions were exact. The Helix-specific subset was
`54/54` exact.

## Measurement boundary

The measure is retained application-file length after required artifacts and
metadata were flushed. It is not device-level write amplification, cloud cost,
or a latest-state-only storage comparison.

The baseline is repeatedly retained expanded FULL history. This result does
not claim that Helix is the smallest possible incremental encoding. A tested
competent incremental comparator retained fewer application-file bytes than
Helix, but the formats did not preserve identical authority semantics. The
private reconstruction representation and implementation are not published.

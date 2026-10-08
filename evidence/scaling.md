# Representation-isolated one-million-row evidence

**Claim ID:** `ER-06`

**Receipt:** [ER-06 scaling](releases/v1/receipts/ER-06-scaling/README.md)

## What was measured

Two deterministic generated one-million-row sparse/local histories were tested
in representation-isolated campaigns: a fixed 32-row change and a 996-row
change (`0.0996%`). Periodic complete snapshots were included.

| Regime | Changed rows | Expanded FULL / Helix N=5 | Expanded FULL / Helix N=10 |
| --- | ---: | ---: | ---: |
| Fixed change | 32 | `3.663926×` | `5.493062×` |
| Fractional change | 996 | `3.596643×` | `5.325055×` |

Every tested representation completed in the isolated evidence set, and each
regime recorded `10/10` exact fresh-process reconstruction checks.

## Qualification

The 996-row result was completed across a primary pass and a frozen completion
pass after not every route began in the first pass under the predeclared
resource gate. It was not one uninterrupted combined pass.

The published evidence is representation-isolated. A separate combined
one-million-row campaign did not produce a successful combined qualification
and is not used as one here. The receipt establishes neither production memory
behavior nor performance above one million rows, and no scaling law is fitted.

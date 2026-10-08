# Transport representation

**Claim ID:** `ER-04`

**Receipt:** [ER-04 transport](releases/v1/receipts/ER-04-transport/README.md)

## What was measured

Three independently seeded deterministic generated histories each ran 40
sparse/local transitions from native Delta Change Data Feed. A separate
receiver accepted either a compressed expanded FULL representation for every
transition or Helix transition artifacts with a complete snapshot every five
or ten transitions.

Periodic snapshot traffic is included in the Helix totals. The common initial
snapshot was excluded symmetrically.

| Snapshot interval | Expanded FULL bytes / Helix bytes |
| --- | ---: |
| Every 5 transitions | `4.364290×–4.475920×` |
| Every 10 transitions | `7.594434×–7.939030×` |

All 240 Helix transitions and all 120 expanded-FULL transitions reconstructed
the expected receiver state exactly.

## Measurement boundary

These are compressed **application-payload bytes**, not TCP/IP wire bytes,
physical network traffic, cloud egress, cost, or latency. The largest ratio is
one measured campaign-policy cell, not an average or universal expectation.

The claim is bounded to the tested sparse/local histories and snapshot
policies. In a separately tested dense condition, FULL was the smaller exact
representation. No universal crossover threshold is published or claimed.

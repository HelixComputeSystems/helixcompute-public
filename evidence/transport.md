# Transport

## What was tested

The transport campaign ran three independently seeded sparse/local histories, each containing 40 transitions. It compared two representations delivered to a separate receiver over localhost TCP:

- a compressed expanded FULL representation for every transition; and
- Helix transition traffic with periodic complete snapshots every 5 or 10 transitions.

Periodic snapshot traffic was included in the Helix totals. The common initial snapshot required by both sides was excluded symmetrically from the transition comparison.

The byte measure is the application payload actually delivered across the TCP connection. It is not TCP/IP wire traffic, physical network traffic, or cloud egress.

## What was observed

| Snapshot interval | Expanded bytes divided by Helix bytes |
| --- | ---: |
| Every 5 transitions | 4.364x–4.476x |
| Every 10 transitions | 7.594x–7.939x |

Across the nominal campaigns, all 240 Helix transitions and all 120 expanded-FULL transitions reconstructed the expected state exactly.

Eight transport integrity and recovery scenarios also produced their predeclared outcomes. Seven invalid or malformed-sequence cases were rejected without accepting the invalid transition; the receiver-restart case recovered exact state and accepted the next valid transition.

The public headline — **up to 7.9x less application payload data moved in tested sparse/local workloads** — rounds the best observed campaign result, 7.939x. It is not an average or a universal expectation.

## Dense-change boundary

The advantage declined as a larger share of the state changed:

| Affected rows | Expanded bytes divided by Helix bytes |
| ---: | ---: |
| 5.65% | approximately 2.554x |
| 11.31% | approximately 1.278x |
| 50% | approximately 0.289x |

A ratio below 1 means Helix used more application payload bytes than the expanded representation. In the tested 50%-change control, dense change reversed the transport advantage.

These measurements describe outcomes and boundaries. They do not publish the representation format or the procedures used to construct, validate, or apply it.

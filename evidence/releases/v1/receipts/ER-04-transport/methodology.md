# Methodology and accounting boundary

Three independently seeded deterministic generated histories each ran 40
transitions from native delta-rs Delta Change Data Feed. A separate
receiver accepted either a compressed complete expanded snapshot for every
transition or Helix transition artifacts with complete snapshots every five or
ten transitions.

## Included

- exact compressed artifact payload bytes delivered over localhost TCP;
- every periodic snapshot for the reported N=5 and N=10 Helix totals; and
- receiver state digest comparison after every accepted transition.

## Excluded

- the common initial snapshot, excluded symmetrically;
- TCP/IP and Ethernet framing;
- physical NIC counters, public-network behavior, and cloud egress; and
- storage economics, pricing, and end-to-end application latency.

## Unknown

Production network overhead and performance on other encodings or workloads
remain unmeasured.

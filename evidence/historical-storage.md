# Historical storage

## What was tested

The historical-storage campaign ran three independently seeded sparse/local histories, each containing 40 transitions. It compared:

- a compressed expanded FULL representation retained for every generation; and
- periodic complete snapshots plus Helix reconstruction artifacts, with snapshots every 5 or 10 transitions.

The primary measure was the sum of actual retained file lengths after artifacts and required metadata or indexes were flushed and fsynced. It does not represent device-level write amplification.

## What was observed

| Snapshot interval | Expanded history bytes divided by Helix bytes |
| --- | ---: |
| Every 5 transitions | 4.028x–4.121x |
| Every 10 transitions | 6.528x–6.774x |

All 135 requested historical reconstructions across the expanded, Helix, and competent incremental representations were exact. The Helix-specific subset was 54/54 exact. In the dense controls, 60/60 requested reconstructions across the tested representations were exact.

The public headline — **up to 6.8x less expanded historical representation retained in tested workloads** — rounds the best observed campaign result, 6.774x. It compares reconstructable Helix history with retaining an expanded representation for every generation.

## Other baselines and boundaries

A competent forward-incremental comparator was smaller than Helix in the sparse histories. Helix used 8.56%–20.39% more retained bytes; equivalently, the comparator used 7.88%–16.94% fewer bytes.

If only current state was required, retaining one latest snapshot was substantially smaller. Helix reconstructable history used 6.05x–10.17x more bytes than one latest snapshot in these campaigns.

The dense controls further narrowed and then reversed the advantage:

| Affected rows | Every 5 transitions | Every 10 transitions |
| ---: | ---: | ---: |
| 5.653% | 1.793x | 1.991x |
| 11.306% | 1.188x | 1.217x |
| 50% | 0.359x | 0.332x |

At 50% change, the Helix historical representation was approximately 2.79x–3.01x larger than expanded history.

Helix's tested historical-storage advantage is against repeatedly retaining expanded generations. It is not universal compression superiority.

These measurements do not publish the private reconstruction representation or implementation.

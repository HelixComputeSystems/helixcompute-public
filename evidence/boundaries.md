# Where the measured advantage stops

## Dense change

Transport and historical-storage advantages deteriorated as affected state became dense. In the tested 50%-change cases, expanded FULL used fewer bytes than Helix.

## Latest-state-only storage

If only current state is required, retaining one latest snapshot was substantially smaller than Helix reconstructable history in the tested campaign. Helix's historical-storage result applies when reconstructable prior generations are required.

## Lean incremental history

The competent forward-incremental comparator was smaller than Helix in the tested sparse historical-storage campaigns. Helix deliberately retains additional verification and reconstruction information that a lean forward-only representation may omit.

## Compression and deduplication

A separate experiment used the one-million-row, approximately-0.1%-change history to ask whether Helix retained an advantage after lower-level byte reduction.

After ordinary Zstandard compression, compared with compressed expanded FULL:

- Helix with snapshots every 5 transitions used 70.89% fewer bytes.
- Helix with snapshots every 10 transitions used 79.60% fewer bytes.

After the tested content-defined deduplication plus the same compression:

- Helix with snapshots every 5 transitions used 5.65% fewer bytes.
- Helix with snapshots every 10 transitions used 6.40% fewer bytes.

The material-advantage threshold was frozen at 20% before measurement. Helix therefore did **not** retain a material advantage under that deduplication-plus-compression comparator. The competent incremental representation was smaller still in that experiment.

These are measured retained-representation bytes, not cloud bills, physical network-wire bytes, or device-write amplification. The experiment does not publish the chunking implementation or private experimental code.

## Interpretation

Helix is not universal compression. Its measured advantage appears when change is sufficiently small relative to state and reconstructable history or transition transport is useful.

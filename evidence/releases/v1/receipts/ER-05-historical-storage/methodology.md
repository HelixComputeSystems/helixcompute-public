# Methodology and accounting boundary

Three independently seeded deterministic generated 40-transition Delta Change
Data Feed histories retained either a compressed expanded FULL representation
for every generation or periodic complete snapshots plus Helix reconstruction
artifacts. Snapshot intervals were five and ten transitions.

## Included

- actual retained file lengths after artifacts and required retained metadata
  were flushed and fsynced;
- periodic complete snapshots and transition artifacts; and
- requested fresh-process historical reconstruction checks.

## Excluded

- filesystem allocation, journal traffic, and physical device writes;
- one-latest-snapshot storage economics;
- cloud storage pricing; and
- any assertion that Helix is the smallest possible incremental encoding.

## Interpretation

The measured ratio is specific to reconstructable history versus retaining a
compressed expanded representation for every generation. It is not a
latest-state-only result and does not establish universal compression
superiority.

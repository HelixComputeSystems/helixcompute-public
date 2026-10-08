# Methodology and accounting boundary

The scaling work tested periodic-snapshot representations for two sparse/local
regimes. The one-million-row fixed-change regime changed 32 rows; the
fractional regime changed 996 rows, or 0.0996%.

The public byte comparison is expanded FULL versus Helix with complete
snapshots every five or ten transitions. `N` is the periodic complete-snapshot
interval in transitions.

Each representation ran in a separate worker. Every tested representation
completed, and fresh processes reconstructed generations 9 and 10.

The fractional 996-row result combines a primary pass with a frozen completion
pass under the same frozen campaign boundaries. It is not one uninterrupted
combined qualification.

## Included

- exact application representation bytes;
- periodic snapshot bytes;
- representation-isolated completion outcomes; and
- fresh-process reconstruction checks.

Application payload and retained byte totals were equal in these frozen
campaigns only because each artifact was transmitted once and retained once.
That accounting identity is not a general network/storage equivalence.

## Excluded

- physical network framing and device write amplification;
- production service overhead and production Core memory behavior;
- dense one-million-row behavior; and
- all estate sizes above one million rows.

No scaling law is fitted. The receipt establishes bounded,
representation-isolated measurements through one million rows; it is not a
combined production qualification.

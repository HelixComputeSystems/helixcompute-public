# Sparse-change scaling

## What was tested

The scaling experiments increased the estate through these measured sizes:

- 44,224 rows;
- 100,000 rows;
- 250,000 rows;
- 500,000 rows; and
- 1,000,000 rows.

Two sparse regimes were tested: a fixed 32-row change and an approximately 0.1% change. The fixed-32-row regime was measured through 1,000,000 rows using isolated representation runs. The approximately-0.1% regime was also measured through 1,000,000 rows. The experiments compared retained and transported representation bytes against expanded FULL, with periodic complete snapshots included.

## Approximately 0.1% change

| Estate rows | Changed rows | Actual affected fraction | Every 5 transitions | Every 10 transitions |
| ---: | ---: | ---: | ---: | ---: |
| 44,224 | 48 | 0.10854% | 3.579x | 5.281x |
| 100,000 | 96 | 0.09600% | 3.593x | 5.317x |
| 250,000 | 252 | 0.10080% | 3.593x | 5.316x |
| 500,000 | 504 | 0.10080% | 3.594x | 5.319x |
| 1,000,000 | 996 | 0.09960% | 3.5966x | 5.3251x |

The ratios are expanded FULL bytes divided by Helix bytes. Across this measured range, the approximately-0.1% curve remained nearly flat and slightly increased at one million rows. No scaling law is fitted.

The fixed-32-row measurements likewise retained a byte advantage through one million rows. At one million rows, the measured ratios were 3.6639x for snapshots every 5 transitions and 5.4931x for snapshots every 10 transitions.

## Exactness and limits

All 90 completed reconstruction checks in the 44,224-to-500,000-row scaling campaign were exact. In each isolated one-million-row campaign, all five tested representations completed and 10/10 fresh-process reconstruction checks were exact.

The original combined one-million-row attempt reached its predeclared memory floor while holding multiple representations in one process. Isolated representation runs completed under the same limits, showing that stop was an overlapping-harness memory effect rather than a boundary reached by an individual tested representation.

No two-million-row experiment was performed. No claim is made beyond the measured one-million-row range, and these results do not establish production-system scaling.

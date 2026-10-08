# ER-06 — Representation-isolated one-million-row scaling

**Release status:** `PUBLIC_RELEASE`

**Evidence class:** MEASURED

**Frozen verdict:** PASS

Two frozen one-million-row sparse/local campaigns measured a fixed 32-row
change and a 996-row change. Each representation ran in an isolated worker.
All five tested representations completed in each regime, and 10/10 requested
fresh-process reconstruction checks were exact in each regime.

Expanded FULL bytes divided by Helix bytes were:

| Regime | N=5 | N=10 |
| --- | ---: | ---: |
| Fixed 32-row change | `3.663926×` | `5.493062×` |
| 996-row change | `3.596643×` | `5.325055×` |

The fixed-32 result completed in one representation-isolated campaign. The
996-row result combines a primary pass with a frozen completion pass under the
same campaign boundaries; it is not one uninterrupted combined qualification.
Neither result establishes production memory behavior or behavior above one
million rows.

Run `python verify.py` to check hashes, ratios, completion counts, and
exactness counts. It does not rerun the scaling campaigns.

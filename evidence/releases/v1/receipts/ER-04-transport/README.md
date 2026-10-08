# ER-04 — Sparse/local transport

**Release status:** `PUBLIC_RELEASE`

**Evidence class:** MEASURED

**Frozen verdict:** PASS

Across three frozen 40-transition campaigns, expanded FULL used
4.364290×–4.475920× the application-payload bytes used by Helix under the N=5
snapshot policy, and 7.594434×–7.939030× under N=10. The Helix totals include
periodic complete snapshot traffic.

All 240 Helix transitions and all 120 expanded-FULL transitions across the
N=5 and N=10 campaigns reconstructed the expected state exactly.

Run `python verify.py` to verify the manifest, per-campaign ratios, range, and
recorded exactness counts. This does not reproduce the transport campaign.

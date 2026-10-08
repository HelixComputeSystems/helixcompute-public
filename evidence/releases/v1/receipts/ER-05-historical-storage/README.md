# ER-05 — Reconstructable historical storage

**Release status:** `PUBLIC_RELEASE`

**Evidence class:** MEASURED

**Frozen campaign verdict:** PASS

Across three frozen 40-transition sparse/local campaigns, expanded FULL
history used 4.028407489997796×–4.120914703075985× the retained file bytes
used by Helix under N=5, and 6.527574829433984×–6.774059647451816× under
N=10.

Across all tested history representations and policies, all 135 requested
reconstructions were exact. The Helix-specific subset was 54/54 exact.

This receipt compares reconstructable Helix history with retaining a
compressed expanded FULL representation for every generation. It does not
claim that Helix is the smallest incremental encoding or the best choice when
only the latest state must be retained. A tested competent incremental
comparator retained fewer application-file bytes than Helix, but the formats
did not carry identical authority semantics.

Run `python verify.py` to check package hashes, recorded byte arithmetic, and
exactness counts. The command does not rebuild or reconstruct the histories.

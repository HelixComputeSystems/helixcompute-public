# Usage terms

**Status: `APPROVED_AND_EFFECTIVE_FOR_EVIDENCE_V1`**

Evidence Release v1 uses file-level licensing. The controlling path allocation
is [`LICENSES/scope.json`](LICENSES/scope.json); no license applies by wildcard
or to the repository as a whole.

## Verifier and test code — BSD-2-Clause

Only these seven files are licensed under the
[BSD 2-Clause License](LICENSES/BSD-2-Clause.txt):

- `evidence/verify.py`
- `evidence/releases/v1/receipts/ER-03-kraken-transform-count/verify.py`
- `evidence/releases/v1/receipts/ER-04-transport/verify.py`
- `evidence/releases/v1/receipts/ER-05-historical-storage/verify.py`
- `evidence/releases/v1/receipts/ER-06-scaling/verify.py`
- `evidence/releases/v1/receipts/ER-11-governed-validation/verify.py`
- `tests/test_evidence_release.py`

## Documentation and evidence — CC BY-ND 4.0

Only the public documentation, sanitized evidence records, and SHA-256
manifests expressly enumerated under `CC-BY-ND-4.0` in
[`LICENSES/scope.json`](LICENSES/scope.json) are licensed under the
[Creative Commons Attribution-NoDerivatives 4.0 International License](LICENSES/CC-BY-ND-4.0.txt).

The requested attribution is:

> Helix Compute Systems, *Helix Compute Evidence Release v1*,
> `evidence-v1.0.0`, https://github.com/HelixComputeSystems/helixcompute-public/tree/evidence-v1.0.0

The NoDerivatives term means modified evidence files may not be shared under
this license. Verification of an unmodified package is permitted; a changed
package is not the immutable Helix Evidence Release v1.

## Everything else — all rights reserved

All rights remain reserved for every file, asset, method, system, and other
material not expressly assigned in [`LICENSES/scope.json`](LICENSES/scope.json).
The two license-text files are reproduced subject to their own terms.

## Rights not granted

Publication does not grant or imply any right to:

- Helix Core or any private source, data, fixture, research record, or
  provenance map;
- private representations, routing, indexes, proof topology, authentication,
  repair machinery, optimization techniques, or mathematical and engineering
  methods;
- any patent, patent application, trademark, logo, trade dress, endorsement,
  or other right not expressly granted by the applicable file license; or
- any technology or material that is not physically present and expressly
  licensed in this release.

Running a verifier checks integrity and arithmetic of the public package. It
does not license, reproduce, or provide access to the private technology that
produced the frozen measurements.

## Accurate citation

Measurements must be cited with their stated metric, comparator, accounting
boundary, conditions, material limitations, and direct immutable receipt link.
Do not convert logical-work counts, validation-phase wall time, application
payload bytes, or retained file bytes into an unstated end-to-end, cost, or
universal-performance claim.

The standard BSD-2-Clause and CC BY-ND 4.0 warranty and liability terms apply
to the files within their respective scopes. No additional permission is
granted for automated collection, model training, or any other use beyond what
the applicable license permits.

Copyright © 2026 Helix Compute Systems.

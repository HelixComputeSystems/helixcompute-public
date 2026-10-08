# Evidence Release v1

**Status:** `PUBLIC_RELEASE` — `evidence-v1.0.0`

This immutable version contains five disclosure-reviewed receipt packages:

- `ER-03` — measured workload-defined transform count;
- `ER-04` — measured application-payload representation;
- `ER-05` — measured reconstructable-history representation;
- `ER-06` — supporting representation-isolated one-million-row evidence; and
- `ER-11` — measured governed-validation wall time with its `MIXED` verdict.

The package is sufficient to verify the released record and deliberately
insufficient to reconstruct Helix Core or the private research program.

Run `python ../../verify.py` from this directory, or `python evidence/verify.py`
from the repository root.

`MANIFEST.sha256` binds the release surface and each receipt manifest. Each
receipt manifest must cover every file in its receipt directory except the
manifest itself; the verifier rejects unmanifested additions.

See [APPROVAL.md](APPROVAL.md) for the recorded owner authorization and
[USAGE.md](../../../USAGE.md) for the exact file-level license allocation.

# Evidence Release v1 — owner approval record

**Status: `APPROVED_FOR_PUBLICATION`**

**Approval date:** 2026-10-08

**Release identifier:** `helix-evidence-v1`

**Immutable tag:** `evidence-v1.0.0`

The owner approved this public release as one atomic publication transition.
The authorization covers commit, tag, push, publication, clean-clone
verification, and pinning website evidence links to the immutable tag.

## Approved disclosure set

The only approved public claims are:

- `ER-03` — measured workload-defined rolling-row transforms;
- `ER-04` — measured application-payload representation;
- `ER-05` — measured reconstructable historical-storage representation;
- `ER-06` — representation-isolated scale evidence; and
- `ER-11` — measured governed-validation wall time with the frozen `MIXED`
  verdict, failed memory qualification, and no final campaign.

The exact permitted statements, comparators, accounting boundaries, exactness
scope, limitations, and forbidden inferences are controlled by
[`../../claims-v1.json`](../../claims-v1.json) and the five receipt packages.
No other private claim or research result is approved by this record.

## Approved licensing

- BSD-2-Clause applies only to the seven verifier/test files expressly listed
  in [`../../../LICENSES/scope.json`](../../../LICENSES/scope.json).
- CC BY-ND 4.0 applies only to the manifest-enumerated public documentation,
  sanitized evidence, and manifests expressly listed in that scope file.
- Everything else is all rights reserved. The standard license texts govern
  the files within their respective scopes; no repository-wide license or
  implied right to private technology is granted.

See [`../../../USAGE.md`](../../../USAGE.md) and
[`../../../LICENSE.md`](../../../LICENSE.md) for the effective public notice.

## Publication invariants

The release must remain one closed, reviewable surface:

1. exactly the five approved claims and five sanitized receipts;
2. `PUBLIC_RELEASE` and `publication_approved: true` in every controlling
   status-bearing record;
3. preserved frozen verdicts and material qualifications, especially ER-11's
   `MIXED` verdict and `1.5065586419753085 > 1.50` memory-gate failure;
4. closed-world SHA-256 coverage from receipt leaves through the release
   manifest;
5. exact file-level license allocation;
6. no private paths, repository identities, credentials, source maps, Core
   implementation, routing logic, proof topology, attack construction, or
   proprietary laboratory detail; and
7. receipt verification clearly distinguished from independent experimental
   reproduction.

If any invariant fails, publication must stop. The `evidence-v1.0.0` tag must
never be moved or rewritten; corrections require a new immutable release and a
documented supersession notice.

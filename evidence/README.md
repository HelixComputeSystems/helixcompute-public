# Helix Compute — Evidence Release v1

> **Release status: `PUBLIC_RELEASE` — `evidence-v1.0.0`**

## The evidence, first

### `~5,941×` FULL/Helix transform ratio

**MEASURED LOGICAL WORK**

FULL performed `1,027,744` workload-defined rolling-row transforms and Helix
performed `173`—approximately `5,941×` as many on FULL and `99.983%` fewer on
Helix—with identical recorded canonical output.

[Inspect ER-03 →](releases/v1/receipts/ER-03-kraken-transform-count/README.md)

### `90.4×–93.3×`

**MEASURED GOVERNED-VALIDATION WALL**

At approximately `0.1%` affected scope, the experiment's frozen canonical FULL
route took `90.385×–93.327×` as long as the experimental Helix route across
44,224-, 250,000-, and 1,000,000-row in-memory estates. The corresponding
predeclared route-total ratio was `3.421×–3.534×`.

[Inspect ER-11 →](releases/v1/receipts/ER-11-governed-validation/README.md)

### Up to `7.939×`

**MEASURED APPLICATION PAYLOAD**

Expanded FULL application-payload bytes divided by Helix application-payload
bytes in the tested sparse/local transport campaigns, including Helix's
periodic complete snapshots.

[Inspect ER-04 →](releases/v1/receipts/ER-04-transport/README.md)

### Up to `6.774×`

**MEASURED RETAINED HISTORY**

Expanded FULL retained file bytes divided by Helix retained file bytes for the
tested reconstructable histories.

[Inspect ER-05 →](releases/v1/receipts/ER-05-historical-storage/README.md)

## Comparator boundaries

- In a separately tested dense transport condition, FULL was the smaller exact
  application-payload representation. No universal crossover threshold is
  published or claimed.
- A tested competent incremental history comparator retained fewer
  application-file bytes than Helix, but the formats did not carry identical
  authority semantics. ER-05 therefore compares reconstructable expanded
  history; it is not a universal smallest-encoding claim.

## Supporting scale evidence

[`ER-06`](releases/v1/receipts/ER-06-scaling/README.md) records
representation-isolated one-million-row measurements and exact fresh-process
reconstruction checks. It is bounded scale evidence, not production
certification or a fitted scaling law.

## What this release verifies

Evidence Release v1 contains five public claim records and five sanitized
receipt packages. Each receipt includes:

- the exact permitted statement;
- frozen measurement extracts and units;
- comparator and accounting boundaries;
- relevant limitations and exactness scope;
- SHA-256 manifests; and
- a standard-library verifier.

The verifier establishes package integrity and arithmetic. It does not publish
Helix Core, rerun the private experiment, or turn receipt verification into
independent experimental reproduction.

## Claim index

| ID | Public role | Evidence class | Frozen verdict |
| --- | --- | --- | --- |
| [`ER-03`](releases/v1/receipts/ER-03-kraken-transform-count/README.md) | Headline logical-work result | MEASURED | PASS, with required qualifiers |
| [`ER-11`](releases/v1/receipts/ER-11-governed-validation/README.md) | Headline validation-phase wall result | MEASURED | MIXED; qualification failed its memory gate |
| [`ER-04`](releases/v1/receipts/ER-04-transport/README.md) | Headline transport-representation result | MEASURED | PASS |
| [`ER-05`](releases/v1/receipts/ER-05-historical-storage/README.md) | Headline historical-storage result | MEASURED | PASS |
| [`ER-06`](releases/v1/receipts/ER-06-scaling/README.md) | Supporting isolated-scale result | MEASURED | PASS within the isolated scope |

Read [methodology](methodology.md), [claim boundaries](boundaries.md),
[limitations](limitations.md), and [verification levels](reproduction-levels.md)
before generalizing any result.

## Disclosure boundary

This repository deliberately excludes private implementation source,
representation layouts, routing and crossover intelligence, proof and
authentication machinery, repair methods, attack construction, private
research lineage, and failed experimental designs. Those exclusions do not
change the published measurements or their material limitations.

Run:

```text
python evidence/verify.py
python -m unittest discover -s tests -v
```

The immutable release tag binds the approved five-claim disclosure set. See
the [approval record](releases/v1/APPROVAL.md) and [license scope](../LICENSES/scope.json).

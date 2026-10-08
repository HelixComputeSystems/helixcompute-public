#!/usr/bin/env python3
"""Verify Evidence Release v1 receipts without executing Helix workloads."""

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys


EVIDENCE = Path(__file__).resolve().parent
ROOT = EVIDENCE.parent
RELEASE = EVIDENCE / "releases" / "v1"
PUBLIC_STATUS = "PUBLIC_RELEASE"
EXPECTED_IDS = {"ER-03", "ER-04", "ER-05", "ER-06", "ER-11"}
CACHE_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache"}
EXPECTED_BSD_FILES = {
    "evidence/verify.py",
    "evidence/releases/v1/receipts/ER-03-kraken-transform-count/verify.py",
    "evidence/releases/v1/receipts/ER-04-transport/verify.py",
    "evidence/releases/v1/receipts/ER-05-historical-storage/verify.py",
    "evidence/releases/v1/receipts/ER-06-scaling/verify.py",
    "evidence/releases/v1/receipts/ER-11-governed-validation/verify.py",
    "tests/test_evidence_release.py",
}
EXPECTED_ALL_RIGHTS_RESERVED_FILES = {
    ".gitattributes",
    ".github/workflows/verify-evidence.yml",
    ".gitignore",
    "LICENSE.md",
    "LICENSES/scope.json",
}
EXPECTED_LICENSE_TEXTS = {
    "LICENSES/BSD-2-Clause.txt":
        "e547dcb8d849a1f354db7c171b8677ccd407a30b1576cc8cdf133e86f416413d",
    "LICENSES/CC-BY-ND-4.0.txt":
        "9cc97638cf0185884ac800144b6246c7772f94ff2cc70686afa9574aaea4fa2b",
}
REQUIRED_CLAIM_FIELDS = {
    "claim_id",
    "release_status",
    "publication_approved",
    "authority_status",
    "exact_permitted_statement",
    "evidence_class",
    "frozen_verdict",
    "conditions",
    "measurement",
    "accounting_boundary",
    "exactness_scope",
    "limitations",
    "reproduction_level",
    "receipt_path",
    "forbidden_inferences",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def verify_manifest(manifest: Path, base: Path, allowed_root: Path) -> set[str]:
    lines = manifest.read_text(encoding="utf-8").splitlines()
    if not lines:
        fail(f"empty manifest: {manifest}")
    seen = set()
    for line in lines:
        try:
            expected, relative = line.split("  ", 1)
        except ValueError:
            fail(f"malformed manifest line: {line!r}")
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            fail(f"invalid SHA-256 in {manifest.name}: {expected}")
        if relative in seen:
            fail(f"duplicate manifest path: {relative}")
        seen.add(relative)
        target = (base / relative).resolve()
        root = allowed_root.resolve()
        try:
            target.relative_to(root)
        except ValueError:
            fail(f"manifest target escapes allowed root: {relative}")
        if not target.is_file():
            fail(f"manifest target missing: {relative}")
        actual = sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            fail(f"SHA-256 mismatch: {relative}")
    return seen


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path}: {error}")


def release_files() -> set[Path]:
    return {
        path.resolve()
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and CACHE_PARTS.isdisjoint(path.parts)
    }


def verify_license_scope(actual_files: set[Path]) -> None:
    scope = load_json(ROOT / "LICENSES" / "scope.json")
    if scope.get("schema_version") != "1.0":
        fail("license scope schema version drift")
    if scope.get("release_id") != "helix-evidence-v1":
        fail("license scope release ID drift")
    if scope.get("effective_for_tag") != "evidence-v1.0.0":
        fail("license scope tag drift")
    if scope.get("approved_on") != "2026-10-08":
        fail("license scope approval date drift")

    assignments = {
        assignment.get("license"): assignment
        for assignment in scope.get("assignments", [])
    }
    if set(assignments) != {"BSD-2-Clause", "CC-BY-ND-4.0"}:
        fail("license assignment set drift")
    if len(scope.get("assignments", [])) != len(assignments):
        fail("duplicate license assignment")

    bsd_files = set(assignments["BSD-2-Clause"].get("files", []))
    cc_files = set(assignments["CC-BY-ND-4.0"].get("files", []))
    if bsd_files != EXPECTED_BSD_FILES:
        fail("BSD-2-Clause file scope drift")
    if assignments["BSD-2-Clause"].get("license_text") != "LICENSES/BSD-2-Clause.txt":
        fail("BSD-2-Clause license-text binding drift")
    if assignments["CC-BY-ND-4.0"].get("license_text") != "LICENSES/CC-BY-ND-4.0.txt":
        fail("CC-BY-ND-4.0 license-text binding drift")

    all_rights_reserved = set(scope.get("all_rights_reserved_files", []))
    if all_rights_reserved != EXPECTED_ALL_RIGHTS_RESERVED_FILES:
        fail("all-rights-reserved file scope drift")
    own_terms = set(scope.get("license_texts_governed_by_their_own_terms", []))
    if own_terms != set(EXPECTED_LICENSE_TEXTS):
        fail("license-text own-terms scope drift")

    scopes = (bsd_files, cc_files, all_rights_reserved, own_terms)
    for index, paths in enumerate(scopes):
        for other in scopes[index + 1:]:
            overlap = paths & other
            if overlap:
                fail(f"overlapping license scopes: {sorted(overlap)}")
    if any(not paths for paths in (bsd_files, cc_files)):
        fail("licensed file scope is empty")

    scoped_files = set()
    for relative in set().union(*scopes):
        target = (ROOT / relative).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"license target escapes release root: {relative}")
        if not target.is_file():
            fail(f"licensed or reserved file missing: {relative}")
        scoped_files.add(target)
    if scoped_files != actual_files:
        missing = sorted(
            path.relative_to(ROOT).as_posix()
            for path in actual_files - scoped_files
        )
        stale = sorted(
            path.relative_to(ROOT).as_posix()
            for path in scoped_files - actual_files
        )
        fail(f"license scope is not closed-world: missing={missing}, stale={stale}")

    for relative, expected in EXPECTED_LICENSE_TEXTS.items():
        if sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            fail(f"canonical license text drift: {relative}")


def resolve_schema_ref(root: dict, ref: str) -> dict:
    if not ref.startswith("#/"):
        fail(f"unsupported external schema reference: {ref}")
    value = root
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or token not in value:
            fail(f"unresolved schema reference: {ref}")
        value = value[token]
    if not isinstance(value, dict):
        fail(f"schema reference does not resolve to an object: {ref}")
    return value


def value_has_type(value: object, expected: str) -> bool:
    types = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "boolean": lambda item: isinstance(item, bool),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "null": lambda item: item is None,
    }
    if expected not in types:
        fail(f"unsupported schema type: {expected}")
    return types[expected](value)


def validate_schema(value: object, schema: dict, root: dict, location: str = "$") -> None:
    """Validate the JSON-Schema subset used by claim.schema.json."""
    if "$ref" in schema:
        validate_schema(value, resolve_schema_ref(root, schema["$ref"]), root, location)
        return
    if "const" in schema and value != schema["const"]:
        fail(f"schema validation at {location}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        fail(f"schema validation at {location}: value is outside the allowed enum")
    for child_schema in schema.get("allOf", []):
        validate_schema(value, child_schema, root, location)
    expected_type = schema.get("type")
    if expected_type and not value_has_type(value, expected_type):
        fail(f"schema validation at {location}: expected {expected_type}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            fail(f"schema validation at {location}: string is too short")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            fail(f"schema validation at {location}: string does not match {schema['pattern']!r}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            fail(f"schema validation at {location}: array has too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            fail(f"schema validation at {location}: array has too many items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_schema(item, item_schema, root, f"{location}[{index}]")
        if "contains" in schema:
            matches = 0
            for index, item in enumerate(value):
                try:
                    validate_schema(item, schema["contains"], root, f"{location}[{index}]")
                except SystemExit:
                    continue
                matches += 1
            if matches < schema.get("minContains", 1):
                fail(f"schema validation at {location}: too few matching items")
            if "maxContains" in schema and matches > schema["maxContains"]:
                fail(f"schema validation at {location}: too many matching items")
    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [name for name in required if name not in value]
        if missing:
            fail(f"schema validation at {location}: missing required properties {missing}")
        properties = schema.get("properties", {})
        for name, child in value.items():
            if name in properties:
                validate_schema(child, properties[name], root, f"{location}.{name}")
            elif schema.get("additionalProperties") is False:
                fail(f"schema validation at {location}: unexpected property {name!r}")
            elif isinstance(schema.get("additionalProperties"), dict):
                validate_schema(child, schema["additionalProperties"], root, f"{location}.{name}")


def verify_claims() -> list[Path]:
    schema = load_json(EVIDENCE / "claim.schema.json")
    index = load_json(EVIDENCE / "claims-v1.json")
    validate_schema(index, schema, schema)
    if index.get("release_status") != PUBLIC_STATUS:
        fail("release status is not PUBLIC_RELEASE")
    if index.get("publication_approved") is not True:
        fail("publication_approved must be true")
    if index.get("reproduction_level") != "RECEIPT_VERIFICATION":
        fail("release reproduction level changed")

    claims = index.get("claims", [])
    by_id = {}
    receipt_paths = set()
    for claim in claims:
        missing = REQUIRED_CLAIM_FIELDS - set(claim)
        if missing:
            fail(f"{claim.get('claim_id', '<unknown>')} missing fields: {sorted(missing)}")
        claim_id = claim["claim_id"]
        if claim_id in by_id:
            fail(f"duplicate claim ID: {claim_id}")
        if claim["release_status"] != PUBLIC_STATUS:
            fail(f"{claim_id} is not PUBLIC_RELEASE")
        if claim["publication_approved"] is not True:
            fail(f"{claim_id} publication approval must be true")
        if claim["reproduction_level"] != "RECEIPT_VERIFICATION":
            fail(f"{claim_id} overstates reproduction level")
        by_id[claim_id] = claim
        receipt_paths.add(claim["receipt_path"])
    if set(by_id) != EXPECTED_IDS:
        fail(f"claim IDs differ from expected set: {sorted(by_id)}")

    receipts = []
    bound_ids = set()
    for relative in sorted(receipt_paths):
        receipt = EVIDENCE / relative
        if not receipt.is_dir():
            fail(f"receipt directory missing: {relative}")
        package_claim = load_json(receipt / "claim.json")
        if package_claim.get("release_status") != PUBLIC_STATUS:
            fail(f"receipt is not PUBLIC_RELEASE: {relative}")
        if package_claim.get("publication_approved") is not True:
            fail(f"receipt publication approval must be true: {relative}")
        if package_claim.get("reproduction_level") != "RECEIPT_VERIFICATION":
            fail(f"receipt overstates reproduction level: {relative}")
        for claim_id in package_claim.get("claim_ids", []):
            if claim_id not in by_id:
                fail(f"receipt references unknown claim: {claim_id}")
            if package_claim["exact_permitted_statements"].get(claim_id) != by_id[claim_id]["exact_permitted_statement"]:
                fail(f"claim statement drift: {claim_id}")
            bound_ids.add(claim_id)
        for metadata_name in ("environment.json", "result.json", "source-binding.json"):
            metadata = load_json(receipt / metadata_name)
            if metadata.get("release_status") != PUBLIC_STATUS:
                fail(f"{metadata_name} is not PUBLIC_RELEASE: {relative}")
        binding = load_json(receipt / "source-binding.json")
        if binding.get("commitments_publicly_dereferenceable") is not False or binding.get("commitments_rehashed_by_public_verifier") is not False:
            fail(f"private authority commitment scope drift: {relative}")
        for artifact in binding.get("authority_artifacts", []):
            if not re.fullmatch(r"[0-9a-f]{64}", artifact.get("sha256", "")):
                fail(f"invalid source commitment in {relative}")
        manifested = verify_manifest(receipt / "MANIFEST.sha256", receipt, receipt)
        actual = {
            path.relative_to(receipt).as_posix()
            for path in receipt.rglob("*")
            if path.is_file()
            and path.name != "MANIFEST.sha256"
            and "__pycache__" not in path.parts
        }
        if manifested != actual:
            fail(
                f"receipt manifest is not closed-world for {relative}: "
                f"missing={sorted(actual - manifested)}, stale={sorted(manifested - actual)}"
            )
        receipts.append(receipt)
    if bound_ids != EXPECTED_IDS:
        fail(f"not every claim is bound to a receipt: {sorted(EXPECTED_IDS - bound_ids)}")
    return receipts


def main() -> None:
    release_manifest = verify_manifest(
        RELEASE / "MANIFEST.sha256", RELEASE, EVIDENCE.parent
    )
    receipts = verify_claims()
    expected_receipt_dirs = {receipt.resolve() for receipt in receipts}
    actual_receipt_dirs = {
        path.resolve()
        for path in (RELEASE / "receipts").iterdir()
        if path.is_dir()
    }
    if actual_receipt_dirs != expected_receipt_dirs:
        fail("unclaimed or missing receipt directory in release surface")
    required_release_entries = {
        "README.md",
        "APPROVAL.md",
        "../../README.md",
        "../../claims-v1.json",
        "../../claim.schema.json",
        "../../claim.public.schema.json",
        "../../methodology.md",
        "../../reproduction-levels.md",
        "../../limitations.md",
        "../../boundaries.md",
        "../../transport.md",
        "../../historical-storage.md",
        "../../scaling.md",
        "../../validation.md",
        "../../verify.py",
        "../../../README.md",
        "../../../USAGE.md",
        "../../../LICENSE.md",
        "../../../LICENSES/BSD-2-Clause.txt",
        "../../../LICENSES/CC-BY-ND-4.0.txt",
        "../../../LICENSES/scope.json",
        "../../../.gitattributes",
        "../../../.gitignore",
        "../../../.github/workflows/verify-evidence.yml",
        "../../../tests/test_evidence_release.py",
    }
    required_release_entries.update(
        f"receipts/{receipt.name}/MANIFEST.sha256" for receipt in receipts
    )
    missing_release_entries = required_release_entries - release_manifest
    unexpected_release_entries = release_manifest - required_release_entries
    if missing_release_entries or unexpected_release_entries:
        fail(
            "release manifest is not the exact frozen surface: "
            f"missing={sorted(missing_release_entries)}, "
            f"unexpected={sorted(unexpected_release_entries)}"
        )
    covered_files = {(RELEASE / "MANIFEST.sha256").resolve()}
    covered_files.update((RELEASE / relative).resolve() for relative in release_manifest)
    for receipt in receipts:
        covered_files.update(
            (receipt / relative).resolve()
            for relative in verify_manifest(
                receipt / "MANIFEST.sha256", receipt, receipt
            )
        )
    actual_files = release_files()
    if covered_files != actual_files:
        missing = sorted(
            path.relative_to(ROOT).as_posix()
            for path in actual_files - covered_files
        )
        stale = sorted(
            path.relative_to(ROOT).as_posix()
            for path in covered_files - actual_files
        )
        fail(f"release manifest is not closed-world: missing={missing}, stale={stale}")
    verify_license_scope(actual_files)
    for receipt in receipts:
        completed = subprocess.run(
            [sys.executable, str(receipt / "verify.py")],
            cwd=receipt,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode:
            sys.stderr.write(completed.stdout)
            sys.stderr.write(completed.stderr)
            fail(f"receipt verifier failed: {receipt.name}")
        print(completed.stdout.strip())
    print(f"PASS release: {len(EXPECTED_IDS)} schema-validated claims, {len(receipts)} receipts, all manifests and receipt checks")
    print("SCOPE: receipt verification only; no Helix workload was executed")
    print("STATUS: PUBLIC_RELEASE")


if __name__ == "__main__":
    main()

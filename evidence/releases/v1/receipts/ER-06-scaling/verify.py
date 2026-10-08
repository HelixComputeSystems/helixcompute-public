#!/usr/bin/env python3
"""Verify ER-06 receipt integrity and arithmetic; do not run Helix."""

from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TOLERANCE = Decimal("1e-14")


def verify_manifest() -> None:
    for line in (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        if sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise SystemExit(f"FAIL: SHA-256 mismatch: {name}")


def check_ratio(row: dict, policy: str) -> None:
    actual = Decimal(row["expanded_full_bytes"]) / Decimal(row[f"helix_{policy}_bytes"])
    expected = Decimal(row[f"expanded_full_div_helix_{policy}"])
    if abs(actual - expected) > TOLERANCE:
        raise SystemExit(f"FAIL: {policy} ratio mismatch")


def main() -> None:
    verify_manifest()
    data = json.loads((ROOT / "result.json").read_text(encoding="utf-8"))
    for key in ("isolated_fixed_32", "isolated_fraction_996"):
        row = data[key]
        check_ratio(row, "n5")
        check_ratio(row, "n10")
        if row["representations_completed"] != row["representations_attempted"]:
            raise SystemExit(f"FAIL: completion mismatch: {key}")
        if row["exact_reconstructions"] != row["attempted_reconstructions"]:
            raise SystemExit(f"FAIL: exactness mismatch: {key}")
    pass_structure = data["isolated_fraction_996"]["pass_structure"]
    if pass_structure["description"] != "primary pass plus frozen completion pass":
        raise SystemExit("FAIL: fractional pass structure changed")
    if pass_structure["single_uninterrupted_combined_pass"]:
        raise SystemExit("FAIL: fractional result overstated as one uninterrupted pass")
    if not pass_structure["same_frozen_campaign_boundaries"]:
        raise SystemExit("FAIL: frozen campaign-boundary qualifier changed")
    if data["execution_scope"] != "representation-isolated workers":
        raise SystemExit("FAIL: representation-isolation boundary changed")
    if data["maximum_tested_estate_rows"] != 1000000 or data["combined_production_qualification"]:
        raise SystemExit("FAIL: scaling scope overstated")
    print("PASS ER-06: receipt hashes, isolated byte ratios, completions, and exactness counts")
    print("SCOPE: receipt verification only; no scaling campaign was rerun")


if __name__ == "__main__":
    main()

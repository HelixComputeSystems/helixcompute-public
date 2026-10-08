#!/usr/bin/env python3
"""Verify ER-04 receipt integrity and recorded byte ratios; do not run Helix."""

from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def verify_manifest() -> None:
    for line in (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        if sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise SystemExit(f"FAIL: SHA-256 mismatch: {name}")


def main() -> None:
    verify_manifest()
    data = json.loads((ROOT / "result.json").read_text(encoding="utf-8"))
    for policy in ("n5", "n10"):
        ratios = []
        for row in data[policy]:
            calculated = (Decimal(row["expanded_full_bytes"]) / Decimal(row["helix_bytes"])).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
            recorded = Decimal(row["expanded_full_div_helix"])
            if calculated != recorded:
                raise SystemExit(f"FAIL: {policy} campaign {row['campaign']} ratio mismatch")
            ratios.append(recorded)
        expected_range = data["ranges"][policy]
        if min(ratios) != Decimal(expected_range["minimum"]) or max(ratios) != Decimal(expected_range["maximum"]):
            raise SystemExit(f"FAIL: {policy} range mismatch")
    exact = data["exactness"]
    if exact["helix_transitions_exact"] != exact["helix_transitions_attempted"] or exact["expanded_full_transitions_exact"] != exact["expanded_full_transitions_attempted"]:
        raise SystemExit("FAIL: exactness count mismatch")
    print("PASS ER-04: receipt hashes, byte ratios, range, and exactness counts")
    print("SCOPE: receipt verification only; the transport campaign was not rerun")


if __name__ == "__main__":
    main()

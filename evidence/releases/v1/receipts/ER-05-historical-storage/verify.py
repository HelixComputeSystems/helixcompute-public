#!/usr/bin/env python3
"""Verify ER-05 receipt integrity and arithmetic; do not run Helix."""

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


def close(left: Decimal, right: Decimal) -> bool:
    return abs(left - right) <= TOLERANCE


def main() -> None:
    verify_manifest()
    data = json.loads((ROOT / "result.json").read_text(encoding="utf-8"))
    n5 = []
    n10 = []
    for row in data["comparisons"]:
        expanded = Decimal(row["expanded_bytes"])
        helix = Decimal(row["helix_bytes"])
        if not close(expanded / helix, Decimal(row["expanded_div_helix"])):
            raise SystemExit(f"FAIL: expanded/Helix mismatch in campaign {row['campaign']} N={row['interval']}")
        if row["interval"] == 5:
            n5.append(Decimal(row["expanded_div_helix"]))
        elif row["interval"] == 10:
            n10.append(Decimal(row["expanded_div_helix"]))
    if min(n5) != Decimal(data["er05_n5_range"]["minimum"]) or max(n5) != Decimal(data["er05_n5_range"]["maximum"]):
        raise SystemExit("FAIL: ER-05 N=5 range mismatch")
    if min(n10) != Decimal(data["er05_n10_range"]["minimum"]) or max(n10) != Decimal(data["er05_n10_range"]["maximum"]):
        raise SystemExit("FAIL: ER-05 N=10 range mismatch")
    exact = data["exactness"]
    if exact["requested_reconstructions"] != exact["exact_reconstructions"] or exact["helix_requested"] != exact["helix_exact"]:
        raise SystemExit("FAIL: exactness count mismatch")
    print("PASS ER-05: receipt hashes, expanded-history byte ratios, and exactness counts")
    print("SCOPE: receipt verification only; no history was reconstructed")


if __name__ == "__main__":
    main()

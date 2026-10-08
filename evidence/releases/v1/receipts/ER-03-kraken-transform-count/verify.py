#!/usr/bin/env python3
"""Verify ER-03 receipt integrity and recorded arithmetic; do not run Helix."""

from decimal import Decimal, getcontext
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
getcontext().prec = 80


def verify_manifest() -> None:
    for line in (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        actual = sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"FAIL: SHA-256 mismatch: {name}")


def main() -> None:
    verify_manifest()
    result = json.loads((ROOT / "result.json").read_text(encoding="utf-8"))
    counter = result["counter"]
    full = Decimal(counter["full"])
    helix = Decimal(counter["helix"])
    if abs(full / helix - Decimal(counter["full_div_helix"])) > Decimal("1e-46"):
        raise SystemExit("FAIL: transform ratio mismatch")
    reduction = (Decimal(1) - helix / full) * Decimal(100)
    if abs(reduction - Decimal(counter["reduction_percent"])) > Decimal("1e-47"):
        raise SystemExit("FAIL: transform reduction mismatch")
    exact = result["exactness"]
    if exact["equivalence_gate"] != "PASS":
        raise SystemExit("FAIL: equivalence gate is not PASS")
    if exact["full_digest_sha256"] != exact["helix_digest_sha256"]:
        raise SystemExit("FAIL: recorded output digests differ")
    print("PASS ER-03: receipt hashes, counter arithmetic, and recorded digest equality")
    print("SCOPE: receipt verification only; the frozen workload was not rerun")


if __name__ == "__main__":
    main()

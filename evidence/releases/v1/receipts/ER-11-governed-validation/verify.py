#!/usr/bin/env python3
"""Verify the sanitized ER-11 receipt without executing Helix."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
getcontext().prec = 60
MEAN_TOLERANCE = Decimal("1e-9")
RATIO_TOLERANCE = Decimal("1e-15")
DENSITY_TOLERANCE = Decimal("1e-17")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def close(actual: Decimal, recorded: str, tolerance: Decimal, label: str) -> None:
    if abs(actual - Decimal(recorded)) > tolerance:
        fail(f"{label} mismatch: computed {actual}, recorded {recorded}")


def verify_manifest() -> None:
    seen = set()
    manifest = ROOT / "MANIFEST.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        if relative in seen:
            fail(f"duplicate manifest path: {relative}")
        seen.add(relative)
        target = (ROOT / relative).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"manifest target escapes receipt: {relative}")
        if not target.is_file():
            fail(f"manifest target missing: {relative}")
        if sha256(target.read_bytes()).hexdigest() != expected:
            fail(f"SHA-256 mismatch: {relative}")


def rounded(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def main() -> None:
    verify_manifest()
    data = json.loads((ROOT / "result.json").read_text(encoding="utf-8"))
    claim = json.loads((ROOT / "claim.json").read_text(encoding="utf-8"))
    binding = json.loads((ROOT / "source-binding.json").read_text(encoding="utf-8"))

    if claim["release_status"] != "PUBLIC_RELEASE" or claim["publication_approved"] is not True:
        fail("public-release publication control drift")
    if claim["reproduction_level"] != "RECEIPT_VERIFICATION":
        fail("reproduction level drift")
    if data["evidence_class"] != "MEASURED" or data["frozen_verdict"] != "MIXED":
        fail("evidence class or MIXED verdict drift")

    protocol = data["protocol"]
    if protocol != {
        "timer": "perf_counter_ns",
        "published_timing_cells": 3,
        "target_affected_fraction": "0.001",
        "warmups_per_cell": 1,
        "sequential_measured_transitions_per_cell": 3,
        "route_workers": "fresh and non-overlapping for FULL and Helix",
        "state_condition": "retained prepared state",
        "comparison_statistic": "arithmetic mean of three governed-validation wall-time samples per route and cell",
        "host_scope": "one host",
    }:
        fail("measurement protocol drift")

    expected_affected = {44224: 44, 250000: 250, 1000000: 1000}
    if len(data["cells"]) != 3:
        fail("expected three published approximately-0.1% cells")
    validation_ratios = []
    route_ratios = []
    seen_estates = set()
    for cell in data["cells"]:
        estate = cell["estate_rows"]
        if estate in seen_estates or estate not in expected_affected:
            fail(f"unexpected or duplicate estate: {estate}")
        seen_estates.add(estate)
        if cell["affected_rows"] != expected_affected[estate]:
            fail(f"affected-row count drift: {estate}")
        density = Decimal(cell["affected_rows"]) / Decimal(estate)
        if abs(density - Decimal(cell["actual_affected_fraction"])) > DENSITY_TOLERANCE:
            fail(f"affected fraction drift: {estate}")

        helix_samples = cell["helix_governed_validation_wall_ns"]
        full_samples = cell["full_governed_validation_wall_ns"]
        if len(helix_samples) != 3 or len(full_samples) != 3:
            fail(f"sample count drift: {estate}")
        helix_total = sum(helix_samples)
        full_total = sum(full_samples)
        helix_mean = Decimal(helix_total) / Decimal(3)
        full_mean = Decimal(full_total) / Decimal(3)
        close(helix_mean, cell["helix_arithmetic_mean_ns"], MEAN_TOLERANCE, f"Helix mean {estate}")
        close(full_mean, cell["full_arithmetic_mean_ns"], MEAN_TOLERANCE, f"FULL mean {estate}")

        validation_ratio = Decimal(full_total) / Decimal(helix_total)
        route_ratio = Decimal(cell["full_route_total_ns"]) / Decimal(cell["helix_route_total_ns"])
        close(validation_ratio, cell["full_over_helix"], RATIO_TOLERANCE, f"validation ratio {estate}")
        close(route_ratio, cell["full_over_helix_route_total"], RATIO_TOLERANCE, f"route ratio {estate}")
        validation_ratios.append(validation_ratio)
        route_ratios.append(route_ratio)

    for key, values in (
        ("full_over_helix_validation_range", validation_ratios),
        ("full_over_helix_route_total_range", route_ratios),
    ):
        recorded = data[key]
        computed = [min(values), max(values)]
        for index in (0, 1):
            close(computed[index], recorded["exact"][index], RATIO_TOLERANCE, f"{key} bound")
        if [rounded(value) for value in computed] != recorded["rounded_for_claim"]:
            fail(f"rounded range drift: {key}")

    correctness = data["correctness"]
    expected_correctness = {
        "unique_measured_transition_instances": 36,
        "helix_exact_and_validated": 36,
        "full_exact_and_validated": 36,
        "separate_mediated_residual_units": 333,
        "residual_units_exactly_localized": 333,
        "residual_units_exactly_repaired": 333,
        "published_output_pairs_for_independent_exactness_recomputation": False,
    }
    if correctness != expected_correctness:
        fail("correctness or residual aggregate drift")

    threat = data["threat_boundary"]
    if threat != {
        "supported_update_model": "mediated authenticated updates",
        "out_of_model_state_mutation_requires_independent_detection": True,
        "private_counterexample_published": False,
        "attack_construction_published": False,
    }:
        fail("threat or disclosure boundary drift")

    memory = data["memory_gate"]
    if Decimal(memory["median_helix_over_full_incremental_rss"]) != Decimal("1.5065586419753085"):
        fail("RSS median drift")
    if not Decimal(memory["median_helix_over_full_incremental_rss"]) > Decimal(memory["ceiling"]):
        fail("RSS failure no longer holds")
    if memory["result"] != "FAIL" or memory["causal_rss_attribution_established"] is not False:
        fail("RSS verdict or attribution drift")

    expected_qualification = {
        "governed_validation_wall_gate": "PASS",
        "correctness_gate": "PASS",
        "residual_localization_and_repair_gate": "PASS",
        "incremental_rss_gate": "FAIL",
        "overall_qualification": "FAIL",
        "experiment": "MIXED",
        "final_campaign": "NOT_RUN_QUALIFICATION_GATE",
    }
    if data["qualification"] != expected_qualification:
        fail("frozen qualification drift")

    provenance = binding["execution_provenance"]
    if provenance != {
        "tracked_source_changes_at_execution": 0,
        "experiment_directory_untracked_at_execution": True,
        "execution_commit_alone_binds_experiment": False,
        "content_hash_bundle_binds_executed_materials": True,
    }:
        fail("execution provenance drift")
    if binding["private_mapping_published"] is not False or binding["private_source_identities_published"] is not False:
        fail("private authority mapping disclosure drift")
    if binding["commitments_publicly_dereferenceable"] is not False or binding["commitments_rehashed_by_public_verifier"] is not False:
        fail("opaque commitment scope drift")

    print("PASS ER-11: three-cell validation and route ratios, exactness aggregates, RSS failure, and MIXED verdict")
    print("SCOPE: receipt verification only; no workload ran and output equality was not independently recomputed")


if __name__ == "__main__":
    main()

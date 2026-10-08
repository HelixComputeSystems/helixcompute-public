import copy
from base64 import b64decode
from decimal import Decimal
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
V1 = EVIDENCE / "releases" / "v1"
PUBLIC_STATUS = "PUBLIC_RELEASE"
EXPECTED_CLAIMS = {
    "ER-03": "ER-03-kraken-transform-count",
    "ER-04": "ER-04-transport",
    "ER-05": "ER-05-historical-storage",
    "ER-06": "ER-06-scaling",
    "ER-11": "ER-11-governed-validation",
}
EXPECTED_RECEIPT_FILES = {
    "README.md",
    "claim.json",
    "environment.json",
    "methodology.md",
    "result.json",
    "source-binding.json",
    "verify.py",
}
EXPECTED_BSD_FILES = {
    "evidence/verify.py",
    "evidence/releases/v1/receipts/ER-03-kraken-transform-count/verify.py",
    "evidence/releases/v1/receipts/ER-04-transport/verify.py",
    "evidence/releases/v1/receipts/ER-05-historical-storage/verify.py",
    "evidence/releases/v1/receipts/ER-06-scaling/verify.py",
    "evidence/releases/v1/receipts/ER-11-governed-validation/verify.py",
    "tests/test_evidence_release.py",
}
EXPECTED_RELEASE_MANIFEST_PATHS = {
    "README.md",
    "APPROVAL.md",
    "../../README.md",
    "../../transport.md",
    "../../historical-storage.md",
    "../../scaling.md",
    "../../validation.md",
    "../../boundaries.md",
    "../../claims-v1.json",
    "../../claim.schema.json",
    "../../claim.public.schema.json",
    "../../methodology.md",
    "../../reproduction-levels.md",
    "../../limitations.md",
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
    *{
        f"receipts/{receipt}/MANIFEST.sha256"
        for receipt in EXPECTED_CLAIMS.values()
    },
}
TEXT_SUFFIXES = {".md", ".json", ".py", ".sha256", ".txt", ".yml", ".yaml"}
CACHE_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache"}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_entries(manifest):
    return [
        line.split("  ", 1)[1]
        for line in manifest.read_text(encoding="utf-8").splitlines()
    ]


def manifest_paths(manifest):
    return set(manifest_entries(manifest))


def release_files():
    return {
        path.resolve()
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and CACHE_PARTS.isdisjoint(path.parts)
    }


class EvidenceReleaseTests(unittest.TestCase):
    @staticmethod
    def load_verifier_module():
        spec = importlib.util.spec_from_file_location(
            "evidence_verify", EVIDENCE / "verify.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_root_verifier(self):
        completed = subprocess.run(
            [sys.executable, str(EVIDENCE / "verify.py")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn(f"STATUS: {PUBLIC_STATUS}", completed.stdout)

    def test_release_is_exactly_the_five_claim_public_release(self):
        index = load_json(EVIDENCE / "claims-v1.json")
        self.assertEqual(index["release_status"], PUBLIC_STATUS)
        self.assertTrue(index["publication_approved"])
        self.assertEqual(index["reproduction_level"], "RECEIPT_VERIFICATION")

        claims = {claim["claim_id"]: claim for claim in index["claims"]}
        self.assertEqual(set(claims), set(EXPECTED_CLAIMS))
        for claim_id, receipt_name in EXPECTED_CLAIMS.items():
            claim = claims[claim_id]
            self.assertEqual(claim["release_status"], PUBLIC_STATUS)
            self.assertTrue(claim["publication_approved"])
            self.assertEqual(claim["reproduction_level"], "RECEIPT_VERIFICATION")
            self.assertEqual(
                claim["receipt_path"], f"releases/v1/receipts/{receipt_name}"
            )

    def test_active_and_mirror_schemas_require_public_state(self):
        module = self.load_verifier_module()
        active_schema = load_json(EVIDENCE / "claim.schema.json")
        public_schema = load_json(EVIDENCE / "claim.public.schema.json")
        index = load_json(EVIDENCE / "claims-v1.json")

        module.validate_schema(index, active_schema, active_schema)
        module.validate_schema(index, public_schema, public_schema)

        review_projection = copy.deepcopy(index)
        review_projection["release_status"] = "REVIEW_CANDIDATE_NOT_APPROVED"
        review_projection["publication_approved"] = False
        for claim in review_projection["claims"]:
            claim["release_status"] = "REVIEW_CANDIDATE_NOT_APPROVED"
            claim["publication_approved"] = False

        with self.assertRaises(SystemExit):
            module.validate_schema(review_projection, active_schema, active_schema)
        with self.assertRaises(SystemExit):
            module.validate_schema(review_projection, public_schema, public_schema)

    def test_public_schema_rejects_claim_approval_drift(self):
        module = self.load_verifier_module()
        schema = load_json(EVIDENCE / "claim.schema.json")
        index = load_json(EVIDENCE / "claims-v1.json")
        index["claims"][0]["publication_approved"] = False
        with self.assertRaises(SystemExit):
            module.validate_schema(index, schema, schema)

    def test_manifest_targets_cannot_escape_allowed_root(self):
        module = self.load_verifier_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "package"
            package.mkdir()
            outside = root / "outside.txt"
            outside.write_text("not package evidence\n", encoding="utf-8", newline="\n")
            digest = module.sha256(outside.read_bytes()).hexdigest()
            manifest = package / "MANIFEST.sha256"
            manifest.write_text(
                f"{digest}  ../outside.txt\n", encoding="utf-8", newline="\n"
            )
            with self.assertRaises(SystemExit):
                module.verify_manifest(manifest, package, package)

    def test_release_and_receipt_manifests_are_closed_world(self):
        receipts_root = V1 / "receipts"
        receipt_dirs = {
            path.name for path in receipts_root.iterdir() if path.is_dir()
        }
        self.assertEqual(receipt_dirs, set(EXPECTED_CLAIMS.values()))

        release_manifest = V1 / "MANIFEST.sha256"
        self.assertEqual(
            len(manifest_entries(release_manifest)),
            len(manifest_paths(release_manifest)),
            "duplicate release manifest path",
        )
        self.assertEqual(
            manifest_paths(release_manifest), EXPECTED_RELEASE_MANIFEST_PATHS
        )
        covered_files = {release_manifest.resolve()}
        for relative in manifest_paths(release_manifest):
            covered_files.add((V1 / relative).resolve())

        for receipt_name in EXPECTED_CLAIMS.values():
            receipt = receipts_root / receipt_name
            manifest = receipt / "MANIFEST.sha256"
            actual = {
                path.relative_to(receipt).as_posix()
                for path in receipt.rglob("*")
                if path.is_file()
                and path.name != "MANIFEST.sha256"
                and CACHE_PARTS.isdisjoint(path.parts)
            }
            self.assertEqual(actual, EXPECTED_RECEIPT_FILES, receipt_name)
            self.assertEqual(
                len(manifest_entries(manifest)),
                len(manifest_paths(manifest)),
                f"duplicate receipt manifest path: {receipt_name}",
            )
            self.assertEqual(
                manifest_paths(manifest), EXPECTED_RECEIPT_FILES, receipt_name
            )
            covered_files.update((receipt / relative).resolve() for relative in actual)

        self.assertEqual(release_files(), covered_files)

    def test_license_scope_is_exact_and_closed_world(self):
        scope = load_json(ROOT / "LICENSES" / "scope.json")
        self.assertEqual(scope["release_id"], "helix-evidence-v1")
        self.assertEqual(scope["effective_for_tag"], "evidence-v1.0.0")
        assignments = {
            assignment["license"]: assignment
            for assignment in scope["assignments"]
        }
        self.assertEqual(set(assignments), {"BSD-2-Clause", "CC-BY-ND-4.0"})
        self.assertEqual(
            set(assignments["BSD-2-Clause"]["files"]), EXPECTED_BSD_FILES
        )

        scopes = [
            set(assignments["BSD-2-Clause"]["files"]),
            set(assignments["CC-BY-ND-4.0"]["files"]),
            set(scope["all_rights_reserved_files"]),
            set(scope["license_texts_governed_by_their_own_terms"]),
        ]
        for index, paths in enumerate(scopes):
            for other in scopes[index + 1:]:
                self.assertEqual(paths & other, set())
        scoped = set().union(*scopes)
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in release_files()
        }
        self.assertEqual(scoped, actual)

        self.assertEqual(
            sha256((ROOT / "LICENSES" / "CC-BY-ND-4.0.txt").read_bytes()).hexdigest(),
            "9cc97638cf0185884ac800144b6246c7772f94ff2cc70686afa9574aaea4fa2b",
        )
        self.assertEqual(
            sha256((ROOT / "LICENSES" / "BSD-2-Clause.txt").read_bytes()).hexdigest(),
            "e547dcb8d849a1f354db7c171b8677ccd407a30b1576cc8cdf133e86f416413d",
        )

    def test_receipt_claims_match_index_statements_and_public_state(self):
        index = load_json(EVIDENCE / "claims-v1.json")
        claims = {claim["claim_id"]: claim for claim in index["claims"]}

        for claim_id, receipt_name in EXPECTED_CLAIMS.items():
            receipt_claim = load_json(
                V1 / "receipts" / receipt_name / "claim.json"
            )
            self.assertEqual(receipt_claim["claim_ids"], [claim_id])
            self.assertEqual(
                set(receipt_claim["exact_permitted_statements"]), {claim_id}
            )
            self.assertEqual(
                receipt_claim["exact_permitted_statements"][claim_id],
                claims[claim_id]["exact_permitted_statement"],
            )
            self.assertEqual(receipt_claim["release_status"], PUBLIC_STATUS)
            self.assertTrue(receipt_claim["publication_approved"])
            self.assertEqual(
                receipt_claim["reproduction_level"], "RECEIPT_VERIFICATION"
            )

    def test_er11_mixed_memory_and_threat_boundaries_are_indivisible(self):
        receipt = V1 / "receipts" / EXPECTED_CLAIMS["ER-11"]
        result = load_json(receipt / "result.json")
        self.assertEqual(result["evidence_class"], "MEASURED")
        self.assertEqual(result["frozen_verdict"], "MIXED")

        memory = result["memory_gate"]
        self.assertEqual(
            memory["median_helix_over_full_incremental_rss"],
            "1.5065586419753085",
        )
        self.assertEqual(memory["ceiling"], "1.50")
        self.assertGreater(
            Decimal(memory["median_helix_over_full_incremental_rss"]),
            Decimal(memory["ceiling"]),
        )
        self.assertEqual(memory["result"], "FAIL")
        self.assertFalse(memory["causal_rss_attribution_established"])

        self.assertEqual(
            result["threat_boundary"],
            {
                "supported_update_model": "mediated authenticated updates",
                "out_of_model_state_mutation_requires_independent_detection": True,
                "private_counterexample_published": False,
                "attack_construction_published": False,
            },
        )
        self.assertEqual(
            result["qualification"],
            {
                "governed_validation_wall_gate": "PASS",
                "correctness_gate": "PASS",
                "residual_localization_and_repair_gate": "PASS",
                "incremental_rss_gate": "FAIL",
                "overall_qualification": "FAIL",
                "experiment": "MIXED",
                "final_campaign": "NOT_RUN_QUALIFICATION_GATE",
            },
        )

        claims = {
            claim["claim_id"]: claim
            for claim in load_json(EVIDENCE / "claims-v1.json")["claims"]
        }
        statement = claims["ER-11"]["exact_permitted_statement"]
        for required in (
            "MIXED",
            "1.5065586419753085",
            "1.50 ceiling",
            "final campaign was not run",
        ):
            self.assertIn(required, statement)

    def test_no_ambiguous_times_less_wording(self):
        pattern = re.compile(r"\b\d+(?:\.\d+)?\s*[x×]\s+less\b", re.IGNORECASE)
        offenders = []
        for path in ROOT.rglob("*.md"):
            if ".git" not in path.parts and pattern.search(
                path.read_text(encoding="utf-8")
            ):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_no_private_paths_or_repository_names_in_release(self):
        forbidden_literals = tuple(
            b64decode(encoded).decode("utf-8")
            for encoded in (
                "YzpcdXNlcnNc",
                "YzovdXNlcnMv",
                "L2hvbWUv",
                "L3VzZXJzLw==",
                "cHJpdmF0ZV9wcm92ZW5hbmNlX21hcA==",
                "aGVsaXhjb21wdXRlX2NvcmU=",
            )
        )
        absolute_path_patterns = (
            re.compile(r"(?<![a-z0-9])[a-z]:[\\/]", re.IGNORECASE),
            re.compile(r"(?<![a-z0-9])/(?:home|users)/[^\s\"'`]+", re.IGNORECASE),
        )
        offenders = []
        for path in ROOT.rglob("*"):
            if (
                ".git" in path.parts
                or not path.is_file()
                or path.suffix not in TEXT_SUFFIXES
            ):
                continue
            text = path.read_text(encoding="utf-8").lower()
            if any(token in text for token in forbidden_literals) or any(
                pattern.search(text) for pattern in absolute_path_patterns
            ):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_manifested_files_are_lf_stable(self):
        manifests = [V1 / "MANIFEST.sha256", *V1.glob("receipts/*/MANIFEST.sha256")]
        for manifest in manifests:
            self.assertNotIn(b"\r\n", manifest.read_bytes(), str(manifest))
            for relative in manifest_paths(manifest):
                target = (manifest.parent / relative).resolve()
                self.assertTrue(target.is_file(), relative)
                if target.suffix in TEXT_SUFFIXES or target.name in {
                    ".gitattributes",
                    ".gitignore",
                }:
                    self.assertNotIn(b"\r\n", target.read_bytes(), str(target))


if __name__ == "__main__":
    unittest.main()

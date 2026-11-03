import json
import shutil
import tempfile
import unittest
from pathlib import Path

import validate_registry


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidateRegistryTests(unittest.TestCase):
    def test_checked_in_candidate_registry_is_valid(self):
        self.assertEqual(validate_registry.validate_registry(REPO_ROOT), [])

    def test_unknown_manifest_system_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(REPO_ROOT / "registry", root / "registry")
            unknown = root / "registry" / "system-manifests" / "unknown.yaml"
            unknown.write_text(
                json.dumps({"system_id": "UNKNOWN", "lifecycle_state": "CANDIDATE"}),
                encoding="utf-8",
            )

            errors = validate_registry.validate_registry(root)

            self.assertTrue(any("unknown system" in error for error in errors))

    def test_ready_manifest_requires_owner_signoff(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(REPO_ROOT / "registry", root / "registry")
            manifest = root / "registry" / "system-manifests" / "M03-EBMS.yaml"
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["lifecycle_state"] = "READY"
            data["sign_off"] = {"owner": "PENDING", "environment": "PENDING"}
            manifest.write_text(json.dumps(data), encoding="utf-8")

            errors = validate_registry.validate_registry(root)

            self.assertTrue(any("owner sign-off" in error for error in errors))

    def test_person_lifecycle_scope_has_twelve_runtime_targets_and_three_gates(self):
        systems = json.loads((REPO_ROOT / "registry" / "systems.yaml").read_text(encoding="utf-8"))["systems"]
        runtime = [item for item in systems if item.get("system_id") != "M00_AEOS"]
        gates = json.loads((REPO_ROOT / "registry" / "capability-gates.yaml").read_text(encoding="utf-8"))["gates"]

        self.assertEqual(len(systems), 13)
        self.assertEqual(len(runtime), 12)
        self.assertEqual({item["system_id"] for item in gates}, {"M08_QUALITY", "M11_INTEGRATION", "M12_DEVSECOPS"})
        self.assertTrue(all(item["deployment_state"] == "NOT_DEPLOYED" for item in gates))

    def test_runtime_manifest_requires_person_lifecycle_endpoint(self):
        data = json.loads((REPO_ROOT / "registry" / "system-manifests" / "M03-EBMS.yaml").read_text(encoding="utf-8"))
        self.assertEqual(data["person_lifecycle_role"], "adapter")
        self.assertEqual(data["deployment_state"], "CANDIDATE")
        self.assertTrue(data["person_lifecycle_endpoint"].endswith("/internal/aeos/person-lifecycle"))


if __name__ == "__main__":
    unittest.main()

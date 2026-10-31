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


if __name__ == "__main__":
    unittest.main()

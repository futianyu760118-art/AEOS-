import json
import shutil
import tempfile
import unittest
from pathlib import Path

import validate_contracts


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SCHEMAS = {
    "principal-context-v1.schema.json",
    "system-manifest-v1.schema.json",
    "audit-event-v1.schema.json",
    "business-event-v1.schema.json",
    "finance-result-v1.schema.json",
    "lead-intake-v1.schema.json",
}


class ValidateContractsTests(unittest.TestCase):
    def test_all_phase_one_schemas_are_valid_and_registered(self):
        errors = validate_contracts.validate_contracts(REPO_ROOT)

        self.assertEqual(errors, [])
        schema_names = {
            path.name for path in (REPO_ROOT / "contracts" / "v1").glob("*.schema.json")
        }
        self.assertEqual(schema_names, EXPECTED_SCHEMAS)

    def test_schema_metadata_has_unique_ids_and_versions(self):
        schemas = validate_contracts.load_schemas(REPO_ROOT)

        self.assertEqual(len(schemas), 6)
        self.assertEqual(len({schema["$id"] for schema in schemas.values()}), 6)
        self.assertEqual(len({schema["schema_version"] for schema in schemas.values()}), 6)
        for schema in schemas.values():
            self.assertIsInstance(schema["title"], str)
            self.assertEqual(schema["type"], "object")
            self.assertFalse(schema["additionalProperties"])
            self.assertTrue(schema["required"])

    def test_manifest_fingerprint_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(REPO_ROOT / "contracts", root / "contracts")
            manifest_path = root / "contracts" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["schemas"][0]["sha256"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            errors = validate_contracts.validate_contracts(root)

            self.assertTrue(any("fingerprint mismatch" in error for error in errors))

    def test_missing_required_field_in_schema_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(REPO_ROOT / "contracts", root / "contracts")
            schema_path = root / "contracts" / "v1" / "audit-event-v1.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["required"].remove("event_id")
            schema_path.write_text(json.dumps(schema), encoding="utf-8")

            errors = validate_contracts.validate_contracts(root)

            self.assertTrue(any("required metadata" in error for error in errors))

    def test_schema_files_are_json_and_contain_no_credentials(self):
        for path in (REPO_ROOT / "contracts" / "v1").glob("*.schema.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            serialized = json.dumps(data).lower()
            self.assertNotRegex(serialized, r'"(?:password|secret|api[_-]?key)"\s*:')


if __name__ == "__main__":
    unittest.main()

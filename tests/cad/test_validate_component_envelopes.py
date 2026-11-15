"""Unit tests for tools/cad/validate_component_envelopes.py."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.cad.validate_component_envelopes import semantic_errors, validate_records


SCHEMA = Path("schemas/cad/component-envelope-record.schema.json")


def base_record() -> dict:
    return {
        "schema_version": "1.0.0",
        "record_id": "TEST.COMPONENT.001",
        "identity": {
            "manufacturer": "Example Manufacturer",
            "designation": "Test device",
            "manufacturer_part_number": "TEST-001",
        },
        "lifecycle": "current",
        "model_provenance": "manufacturer_original",
        "sources": [{
            "source_id": "SRC.DRAWING",
            "class": "A_manufacturer_controlled_drawing",
            "publisher": "Example Manufacturer",
            "title": "Controlled outline drawing",
            "document_revision": "A",
            "retrieved_on": "2026-11-15",
        }],
        "dimensions": [{
            "dimension_id": "DIM.WIDTH",
            "name": "Body width",
            "value": 100.0,
            "unit": "mm",
            "definition": "Maximum external body width",
            "axis_or_datum": "X axis",
            "evidence_class": "A_manufacturer_controlled_drawing",
            "source_ids": ["SRC.DRAWING"],
        }],
        "review": {"state": "provisional", "open_issues": ["Test fixture only"]},
    }


class ComponentEnvelopeValidatorTests(unittest.TestCase):
    def test_valid_provisional_record_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = root / "records"
            records.mkdir()
            (records / "test.json").write_text(json.dumps(base_record()), encoding="utf-8")
            checked, errors = validate_records(records, SCHEMA, root)
            self.assertEqual(checked, 1)
            self.assertEqual(errors, [])

    def test_missing_source_reference_is_rejected(self):
        record = base_record()
        record["dimensions"][0]["source_ids"] = ["SRC.MISSING"]
        errors = semantic_errors(record, Path("."))
        self.assertTrue(any("unknown source_id SRC.MISSING" in item for item in errors))

    def test_dimension_source_class_mismatch_is_rejected(self):
        record = base_record()
        record["dimensions"][0]["evidence_class"] = "C_manufacturer_datasheet"
        errors = semantic_errors(record, Path("."))
        self.assertTrue(any("evidence_class does not match" in item for item in errors))

    def test_release_without_second_person_review_is_rejected(self):
        record = base_record()
        record["review"] = {
            "state": "released_for_design",
            "reviewer_role": "Mechanical reviewer",
            "reviewed_on": "2026-11-15",
            "approval_scope": "Envelope layout only",
            "second_person_review": False,
        }
        errors = semantic_errors(record, Path("."))
        self.assertTrue(any("second-person review" in item for item in errors))

    def test_third_party_model_cannot_be_released(self):
        record = base_record()
        record["model_provenance"] = "third_party_unverified"
        record["review"] = {
            "state": "released_for_design",
            "reviewer_role": "Reviewer",
            "reviewed_on": "2026-11-15",
            "approval_scope": "Layout",
            "second_person_review": True,
        }
        errors = semantic_errors(record, Path("."))
        self.assertTrue(any("cannot be released" in item for item in errors))

    def test_stored_source_hash_is_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "drawing.pdf"
            evidence.write_bytes(b"controlled drawing fixture")
            record = base_record()
            record["sources"][0]["controlled_path"] = "drawing.pdf"
            record["sources"][0]["sha256"] = hashlib.sha256(b"wrong").hexdigest()
            errors = semantic_errors(record, root)
            self.assertTrue(any("SHA-256 mismatch" in item for item in errors))

    def test_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = base_record()
            record["sources"][0]["controlled_path"] = "../outside.pdf"
            record["sources"][0]["sha256"] = "0" * 64
            errors = semantic_errors(record, root)
            self.assertTrue(any("escapes repository root" in item for item in errors))


if __name__ == "__main__":
    unittest.main()

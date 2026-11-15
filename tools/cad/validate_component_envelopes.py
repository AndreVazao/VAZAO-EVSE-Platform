#!/usr/bin/env python3
"""Validate VAZAO EVSE component-envelope records and their local evidence.

This tool is intentionally offline: it does not fetch URLs or trust remote content.
It validates JSON Schema structure, cross-references, repository-contained paths,
and SHA-256 hashes for evidence files that are present in the repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - exercised by CLI users
    raise SystemExit(
        "Missing dependency. Install with: "
        "python -m pip install -r requirements-cad-validation.txt"
    ) from exc


RELEASE_EVIDENCE_CLASSES = {
    "A_manufacturer_controlled_drawing",
    "B_manufacturer_CAD",
    "C_manufacturer_datasheet",
    "D_verified_physical_measurement",
}
ALL_EVIDENCE_CLASSES = RELEASE_EVIDENCE_CLASSES | {
    "E_derived_engineering",
    "F_visual_or_unverified",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contained_path(root: Path, raw_path: str, label: str, errors: list[str]) -> Path | None:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        errors.append(f"{label}: absolute paths are not allowed: {raw_path}")
        return None
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        errors.append(f"{label}: path escapes repository root: {raw_path}")
        return None
    return resolved


def check_file_hash(
    root: Path, raw_path: str, expected_hash: str | None, label: str,
    errors: list[str], *, required_hash: bool,
) -> None:
    file_path = contained_path(root, raw_path, label, errors)
    if file_path is None:
        return
    if not file_path.is_file():
        errors.append(f"{label}: file does not exist: {raw_path}")
        return
    if not expected_hash:
        if required_hash:
            errors.append(f"{label}: SHA-256 is required for a stored file")
        return
    actual = sha256_file(file_path)
    if actual.lower() != expected_hash.lower():
        errors.append(
            f"{label}: SHA-256 mismatch for {raw_path}; "
            f"expected {expected_hash.lower()}, got {actual}"
        )


def semantic_errors(record: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    record_id = str(record.get("record_id", "<unknown>"))
    sources = record.get("sources", [])
    source_by_id: dict[str, dict[str, Any]] = {}

    for source in sources:
        source_id = source.get("source_id")
        if not source_id:
            continue
        if source_id in source_by_id:
            errors.append(f"{record_id}: duplicate source_id {source_id}")
        source_by_id[source_id] = source
        controlled_path = source.get("controlled_path")
        if controlled_path:
            check_file_hash(
                root, controlled_path, source.get("sha256"),
                f"{record_id}/source/{source_id}", errors, required_hash=True,
            )

    for dimension in record.get("dimensions", []):
        dimension_id = dimension.get("dimension_id", "<unnamed>")
        linked_ids = dimension.get("source_ids", [])
        for source_id in linked_ids:
            source = source_by_id.get(source_id)
            if source is None:
                errors.append(
                    f"{record_id}/dimension/{dimension_id}: "
                    f"unknown source_id {source_id}"
                )
                continue
            if source.get("class") != dimension.get("evidence_class"):
                errors.append(
                    f"{record_id}/dimension/{dimension_id}: evidence_class "
                    f"does not match source {source_id}"
                )

    model = record.get("model_file")
    if model:
        check_file_hash(
            root, model.get("path", ""), model.get("sha256"),
            f"{record_id}/model_file", errors, required_hash=True,
        )
        if model.get("original_source_immutable") is False and (
            record.get("model_provenance") == "manufacturer_original"
        ):
            errors.append(
                f"{record_id}: manufacturer_original model must preserve "
                "the source file as immutable"
            )

    review = record.get("review", {})
    if review.get("state") == "released_for_design":
        if not review.get("reviewer_role"):
            errors.append(f"{record_id}: released record requires reviewer_role")
        if not review.get("reviewed_on"):
            errors.append(f"{record_id}: released record requires reviewed_on")
        if not review.get("approval_scope"):
            errors.append(f"{record_id}: released record requires approval_scope")
        if review.get("second_person_review") is not True:
            errors.append(f"{record_id}: released record requires second-person review")
        if record.get("model_provenance") == "third_party_unverified":
            errors.append(f"{record_id}: unverified third-party model cannot be released")
        if not any(source.get("class") in RELEASE_EVIDENCE_CLASSES for source in sources):
            errors.append(
                f"{record_id}: released record requires at least one A/B/C/D source"
            )
        for dimension in record.get("dimensions", []):
            if dimension.get("evidence_class") == "F_visual_or_unverified":
                errors.append(
                    f"{record_id}: released record contains an unverified dimension "
                    f"({dimension.get('dimension_id', '<unnamed>')})"
                )

    if record.get("model_provenance") == "third_party_unverified" and (
        review.get("state") in {"verified_reference", "released_for_design"}
    ):
        errors.append(
            f"{record_id}: third_party_unverified provenance cannot be "
            f"{review.get('state')}"
        )

    return errors


def load_schema(schema_path: Path) -> dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_records(records_dir: Path, schema_path: Path, repo_root: Path) -> tuple[int, list[str]]:
    schema = load_schema(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    files = sorted(records_dir.rglob("*.json")) if records_dir.exists() else []
    errors: list[str] = []
    seen_record_ids: set[str] = set()
    seen_parts: dict[tuple[str, str], str] = {}
    checked = 0

    for record_path in files:
        if record_path.resolve() == schema_path.resolve():
            continue
        checked += 1
        try:
            record = json.loads(record_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"{record_path}: cannot read JSON: {exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{record_path}: record root must be a JSON object")
            continue

        for issue in validator.iter_errors(record):
            location = ".".join(str(part) for part in issue.absolute_path) or "$"
            errors.append(f"{record_path}:{location}: {issue.message}")

        record_id = record.get("record_id")
        if record_id:
            if record_id in seen_record_ids:
                errors.append(f"{record_path}: duplicate record_id {record_id}")
            seen_record_ids.add(record_id)

        identity = record.get("identity", {})
        manufacturer = identity.get("manufacturer")
        part_number = identity.get("manufacturer_part_number")
        if manufacturer and part_number:
            key = (manufacturer.casefold(), part_number.casefold())
            previous = seen_parts.get(key)
            if previous:
                errors.append(
                    f"{record_path}: duplicate manufacturer/part number also in {previous}; "
                    "represent a distinct variant explicitly"
                )
            else:
                seen_parts[key] = str(record_path)

        errors.extend(semantic_errors(record, repo_root))

    if checked == 0:
        errors.append(f"No component record JSON files found under {records_dir}")
    return checked, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--records", type=Path, default=Path("hardware/library/components"),
        help="directory containing component record.json files",
    )
    parser.add_argument(
        "--schema", type=Path,
        default=Path("schemas/cad/component-envelope-record.schema.json"),
        help="JSON Schema file",
    )
    parser.add_argument(
        "--repo-root", type=Path, default=Path("."),
        help="repository root used to resolve and constrain evidence paths",
    )
    args = parser.parse_args()

    try:
        count, errors = validate_records(args.records, args.schema, args.repo_root)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2

    if errors:
        print(f"FAIL: checked {count} record(s); found {len(errors)} issue(s).")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"PASS: schema and semantic checks passed for {count} record(s).")
    print("Note: this does not prove source authenticity, dimensional accuracy or design approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

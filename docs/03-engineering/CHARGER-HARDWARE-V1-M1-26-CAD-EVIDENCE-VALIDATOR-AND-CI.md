# VAZÃO EVSE — Charger Hardware V1
## M1.26 — CAD evidence validator and continuous integration

**Status:** IMPLEMENTED IN REPOSITORY; AUTOMATED EXECUTION PENDING GITHUB ACTIONS RESULT  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.25 provenance record and JSON Schema  
**Scope:** validate record structure and local evidence integrity without inventing or approving component data.

---

## 1. Deliverables

- `tools/cad/validate_component_envelopes.py` — offline command-line validator.
- `tests/cad/test_validate_component_envelopes.py` — negative and positive unit tests.
- `tools/cad/__init__.py` — Python package marker.
- `requirements-cad-validation.txt` — isolated dependency declaration (`jsonschema>=4.23,<5`).
- `.github/workflows/cad-envelope-validation.yml` — pull-request CI for schema validation and unit tests.

The validator uses JSON Schema Draft 2020-12 and an additional semantic validation pass. It does not fetch URLs, call external services, alter files or infer component dimensions.

## 2. Checks implemented

1. Validate each JSON record against `schemas/cad/component-envelope-record.schema.json`, including date/URI formats.
2. Reject malformed JSON and non-object record roots.
3. Detect duplicate record IDs and duplicate manufacturer/part-number identities within the scanned record set.
4. Detect duplicate source IDs inside a record.
5. Ensure each dimension's source IDs exist and the declared evidence class is represented by its linked source evidence.
6. Constrain stored evidence/model paths to the repository root; reject absolute paths and path traversal.
7. Require a SHA-256 for stored source/model files and compare it with the actual file bytes.
8. Require a design-release record to carry reviewer role, review date, approval scope, second-person review, at least one A/B/C/D source, and no unverified F-class dimensions.
9. Prevent a `third_party_unverified` model from reaching `verified_reference` or `released_for_design`.

The validator is deliberately offline. A URL is metadata, not proof that a source is genuine. SHA-256 proves byte identity against the recorded digest, not that a drawing is correct or belongs to the intended SKU.

## 3. Run locally

From the repository root:

```powershell
python -m pip install -r requirements-cad-validation.txt
python -m unittest discover -s tests/cad -v
python tools/cad/validate_component_envelopes.py --records hardware/library/components --repo-root .
```

The CLI expects actual component record JSON files under the records directory. Until the first evidence-backed record is added, it reports that no records were found; this is an intentional fail-closed result, not a passing empty inventory.

To validate a different record directory or schema:

```powershell
python tools/cad/validate_component_envelopes.py --records <records-directory> --schema schemas/cad/component-envelope-record.schema.json --repo-root .
```

## 4. CI behaviour

The workflow runs on pull requests touching CAD schema/tool/tests/dependency/workflow paths and on matching pushes to `main`. It installs the isolated dependency, checks the Draft 2020-12 schema itself, then runs the unit tests on Python 3.12.

CI does not currently run the CLI against product records because no approved component records exist. When the first evidence-backed record is committed, add a separate CI step for the record directory. Do not add synthetic/example components to the production library merely to make the command green.

## 5. Test coverage authored

The unit suite covers:
- a valid provisional test record;
- missing source reference;
- source/evidence-class mismatch;
- design release without second-person review;
- prohibited release of third-party unverified model;
- stored evidence SHA-256 mismatch;
- path traversal outside the repository root.

These tests have been committed, but their execution is **PENDING** until the GitHub Actions run is observed. Do not report them as passed before the run completes successfully.

## 6. Known limits / next hardening

- No actual manufacturer component record has been populated.
- No file authenticity, URL availability, licensing or manufacturer lifecycle check is performed.
- No CAD geometry is opened or measured by this validator.
- No thermal, electrical, structural, IP/IK, metrology or regulatory approval is inferred.
- The current validator checks source references and local hashes; a later hardening pass should add a reviewable manifest for external evidence and stricter variant/revision conflict handling.
- No component record can be released without competent engineering review, regardless of CI status.

## 7. Acceptance status

| Gate | Acceptance evidence | Status |
|---|---|---|
| V1 | Validator and tests committed | COMPLETE |
| V2 | CI workflow committed | COMPLETE |
| V3 | JSON Schema check in GitHub Actions | PENDING |
| V4 | Unit suite in GitHub Actions | PENDING |
| V5 | Real manufacturer-backed component record | OPEN |
| V6 | Actual stored source/model hash verification against controlled files | OPEN |
| V7 | Independent review of a populated record | OPEN |
| V8 | CAD-native geometry verification on workstation | OPEN (M1.24 W-gates) |

**Current result:** validator, unit tests and CI workflow are committed. Automated execution has not yet been observed. No physical component data, approved envelope, product CAD or manufacturing release is claimed. PR remains Draft.

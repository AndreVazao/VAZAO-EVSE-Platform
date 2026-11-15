# VAZÃO EVSE — Charger Hardware V1
## M1.25 — CAD model provenance and dimensional evidence control

**Status:** CONTROL SPECIFICATION / NOT YET POPULATED WITH APPROVED COMPONENT RECORDS  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.21 enclosure requirements; M1.22 dimensioning/CAD input matrix; M1.23 native CAD architecture/model control; M1.24 workstation inventory/pilot  
**Purpose:** establish a machine-readable, reviewable chain from a physical component and its manufacturer evidence to any CAD envelope used in VAZÃO EVSE design.

---

## 1. Decision and scope

M1.25 defines the minimum provenance record for every component envelope admitted into mechanical CAD. The objective is to prevent an attractive STEP model, an approximate drawing, a catalogue dimension or a derived model from silently becoming an authoritative manufacturing input.

The record schema is provided at:

`schemas/cad/component-envelope-record.schema.json`

This milestone defines data governance and validation rules only. It does not populate or approve any component envelope, select an enclosure, generate product geometry or close M1.21/M1.22/M1.23 gates.

## 2. Evidence classes and authority

Each dimension or geometric claim must be traceable to a source and classified by authority:

| Class | Meaning | Permitted use |
|---|---|---|
| A — controlled manufacturer drawing | Exact part/revision drawing published or supplied by manufacturer | Primary dimensional authority, subject to revision and interpretation review |
| B — manufacturer CAD model | Exact manufacturer-supplied native/STEP model with identifiable part and revision | Shape/envelope reference; not automatically proof of hidden tolerances or service clearances |
| C — manufacturer datasheet/catalogue | Published dimensional data for the exact product/variant | Supporting evidence; confirm which dimensions are overall, mounting or accessory-related |
| D — verified physical measurement | Recorded measurement of the exact physical item with method, instrument and uncertainty | Corroboration or controlled substitute where manufacturer evidence is unavailable; independent review required |
| E — derived engineering value | Calculated or inferred from A–D sources with method and inputs recorded | Engineering estimate only; must not be represented as manufacturer data |
| F — visual estimate / third-party model | Photograph, marketplace image, community model or unverified source | Discovery only; prohibited as dimensional authority for released CAD |

A source class is not a product approval. Exact SKU, suffix, revision, accessory state and regional variant must match the intended component. Where sources conflict, record the conflict; do not average dimensions or choose the most convenient value.

## 3. Required record contents

Every component envelope record must contain:

- stable record ID and schema version;
- manufacturer, exact product designation and complete manufacturer part number;
- lifecycle state and evidence date;
- model provenance: manufacturer original, supplier-provided, measured, derived or community/unknown;
- one or more source records with publisher, document title, revision/date, URL or controlled local path, retrieval date and SHA-256 where a file is retained;
- dimensions with explicit units (millimetres for this project), axis/measurement definition, evidence class and source reference;
- model file path, format, file hash, units, coordinate convention and orientation where a model is retained;
- known exclusions: connectors, cable bend radius, mating space, tool access, ventilation, terminal access, door swing and service clearance are not assumed to be included in the body envelope;
- review state, reviewer identity/role and review date;
- explicit limitations and unresolved conflicts.

The schema intentionally does not require personal names. Use role/team identifiers in public records where possible.

## 4. Model provenance states

Use one of the following controlled values:

- `manufacturer_original`: file downloaded from or supplied directly by the manufacturer for the exact part.
- `supplier_provided`: file supplied by a distributor/integrator; manufacturer origin not independently confirmed.
- `measured_reference`: geometry created from a physical sample using a documented measurement method.
- `derived_engineering`: geometry created or simplified from controlled evidence; transformation and source links must be retained.
- `third_party_unverified`: community/marketplace/unknown model; discovery only, never release authority.

A model may be visually correct and still be dimensionally unsuitable. Simplification, missing accessories, suppressed features, imported scale, tessellation and coordinate transformations must be declared.

## 5. Dimensional and CAD acceptance rules

1. Use millimetres in the VAZÃO EVSE mechanical master model. Imported source units must be checked, not assumed.
2. Keep the original source file immutable. Work on a derived copy and record both hashes.
3. Verify at least three non-collinear, manufacturer-dimensioned references where the drawing provides them; include overall envelope and mounting interface where applicable.
4. Record orientation and origin transformation explicitly. Never silently rotate, scale or translate an imported supplier model.
5. Compare model geometry against the exact drawing revision. A visual fit is not dimensional verification.
6. Do not infer tolerances from nominal dimensions. Record tolerance only when explicitly specified or independently justified.
7. Do not treat a component body envelope as a complete installation envelope. Add cable, mating, ventilation, heat, access and service envelopes as separate, traceable design objects.
8. Preserve source units and original model in an immutable evidence location; derived CAD files must link back to source record ID.
9. Any change of SKU, suffix, revision, accessory, terminal orientation or mounting kit invalidates the previous envelope review until assessed.
10. A failed or incomplete validation leaves the record `provisional` or `rejected`; it must not enter a released assembly.

## 6. Review states

- `unreviewed`: record exists but no engineering review has occurred.
- `provisional`: useful for layout exploration only; open evidence or dimensional checks remain.
- `verified_reference`: provenance and dimensional checks reviewed for engineering layout; not a manufacturing approval.
- `released_for_design`: approved for the explicitly named design purpose and configuration, with reviewer and evidence retained.
- `rejected`: known mismatch, insufficient provenance or failed dimensional validation.

No record can become `released_for_design` solely because a STEP file imports successfully. A second-person review is required for release. The approval scope must state whether the model may be used for envelope layout, mounting design, thermal analysis or manufacturing; these are not interchangeable permissions.

## 7. Repository and change control

Recommended structure:

```text
hardware/
  library/
    components/
      <manufacturer>/
        <part-number>/
          source/       # immutable manufacturer/supplier originals
          derived/      # simplified/converted models with provenance
          evidence/     # drawings, datasheets, verification notes
          record.json   # conforms to the M1.25 schema
```

Do not commit licensed or confidential supplier files unless redistribution rights are confirmed. If the original cannot be stored in Git, retain a controlled source URL/reference, retrieval date, hash and access location. Large binary models should follow the repository's approved large-file policy; do not introduce Git LFS or a new storage service without checking current repository policy.

Every change to source file, dimensions, model transformation, SKU or review state must update the record and trigger re-review. Keep previous source hashes and review decisions in Git history; do not rewrite history to hide a superseded model.

## 8. Automated checks

A future validator should reject or flag:

- missing required identity, SKU, units, source or provenance;
- duplicate record IDs or duplicate manufacturer/part-number records without an explicit variant distinction;
- source references without retrieval date or revision where one exists;
- local source/model paths that do not resolve;
- file hash mismatch;
- unsupported units or implicit unit conversion;
- model path with no format or hash;
- `released_for_design` without reviewer, review date, approval scope and at least one A/B/C/D evidence source;
- third-party/unverified geometry marked released;
- dimensions with no source reference or evidence class;
- stale review after a SKU/revision/accessory change.

This milestone does not claim that such a validator has been implemented or run. The JSON Schema validates record shape; it cannot prove that a URL is authentic, a file hash matches the actual file, or a dimension is correct. Those checks require external source review and human review; M1.26 adds local structural, reference and file-integrity checks but does not authenticate remote sources.

## 9. Relationship to existing gates

M1.25 supports, but does not close:

- M1.21 E-gates: enclosure, environment, thermal and structural inputs;
- M1.22 D-gates: exact component envelopes, capacity and service spaces;
- M1.23 C-gates: native CAD workflow, units, model provenance and exchange;
- M1.24 W-gates: actual workstation inventory and native/STEP/DXF pilot.

Until exact component records are populated and reviewed, enclosure sizing, component coordinates, mounting holes, clearances, thermal/structural conclusions and fabrication drawings remain blocked.

## 10. Acceptance checklist

| Gate | Acceptance evidence | Status |
|---|---|---|
| P1 | Schema reviewed against actual CAD/library workflow | OPEN |
| P2 | JSON Schema syntax validated by a standards-compliant validator | OPEN |
| P3 | At least one exact component record populated from manufacturer evidence | OPEN |
| P4 | Source file hash and immutable original handling demonstrated | OPEN |
| P5 | Model units/orientation and drawing comparison recorded | OPEN |
| P6 | Independent second-person review demonstrated | OPEN |
| P7 | Repository/licensing and large-file handling approved | OPEN |
| P8 | Validator implemented; negative-case execution confirmed in CI | PENDING (M1.26 CI not yet observed) |
| P9 | AndreOS Memory checkpoint updated | OPEN until verified |
| P10 | PR summary and evidence links verified | OPEN until verified |

**Current result:** provenance and dimensional-evidence rules prepared. No component envelope is populated or approved; no CAD geometry, manufacturing dimension or test result is claimed. PR remains Draft. No fabrication, installation or mains energisation is authorised.

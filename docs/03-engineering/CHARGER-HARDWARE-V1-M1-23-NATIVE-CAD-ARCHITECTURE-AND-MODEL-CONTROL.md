# VAZÃO EVSE — Charger Hardware V1
## M1.23 — Native CAD architecture and model control

**Status:** CAD ARCHITECTURE / TOOLCHAIN DECISION FRAMEWORK — OPEN  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.19 electrical boundaries, M1.20 physical zoning, M1.21 enclosure requirements, M1.22 dimensioning/CAD input matrix  
**Purpose:** define a reproducible, editable, evidence-linked mechanical CAD workflow without implying that the local CAD software has been inventoried or that dimensioned/manufacturing models exist.

---

## 1. Executive decision

Adopt a **native-source-first, neutral-exchange-second** CAD policy.

- Native editable source is the authoritative design record.
- STEP is the preferred neutral 3D exchange format for verified component geometry.
- DXF may be used for 2D exchange where the receiving process requires it.
- PDF and SVG are review/publication derivatives only; they are never the authoritative editable model.
- Every imported component model must be tied to an exact manufacturer SKU, document revision, source URL/file and retrieval date.
- Missing or unverified dimensions must remain explicitly marked as unknown; placeholder envelopes must be visibly labelled as non-dimensional.
- No CAD geometry may silently convert an assumption into a released manufacturing dimension.

**Provisional native-tool direction:** evaluate FreeCAD as the preferred open-source native authoring environment, using its native project format (`.FCStd`) and parametric features. This is a recommendation for evaluation, **not a claim that FreeCAD is installed, available on the user's PC, or already validated for this project**. The local tool inventory remains OPEN until the workstation is inspected or the user supplies an inventory.

The model structure must remain portable enough to migrate to another capable CAD system if FreeCAD is unavailable or unsuitable.

## 2. Toolchain inventory — not yet performed

The following must be recorded on the actual engineering workstation before toolchain approval:

| Item | Required evidence | Status |
|---|---|---|
| Operating system and architecture | System inventory | OPEN |
| CAD application and exact version | Application/version evidence | OPEN |
| Native file compatibility | Open/save/reopen test on a controlled sample | OPEN |
| STEP import/export | Round-trip test and geometry inspection | OPEN |
| DXF import/export | Units/layers/text test where needed | OPEN |
| Parametric assembly capability | Small repeatable assembly test | OPEN |
| 2D drawing and dimensioning | Drawing-sheet/export test | OPEN |
| Scripting/API support | Version-matched official documentation and test | OPEN |
| Batch/headless operation | Actual application test, if required | OPEN |
| Git-friendly storage | Save/reopen and diff/large-file strategy | OPEN |

Do not report a CAD application as installed or tested based solely on a planned workflow. If the workstation is inaccessible, retain this inventory as OPEN and continue with format-neutral documentation.

## 3. File-format policy

| Purpose | Preferred format | Rule |
|---|---|---|
| Authoritative parametric mechanical model | Native CAD project (provisionally `.FCStd`) | Editable source, versioned and backed up |
| Manufacturer component geometry | STEP (`.step` / `.stp`) | Exact SKU and source provenance required |
| 2D exchange | DXF | Units, layers and revision documented |
| Review drawing | PDF | Derived from native source |
| Lightweight web/review diagram | SVG | Not manufacturing authority |
| Mesh/visualisation | STL/3MF only when justified | Not suitable as dimensional source of truth |

Never replace a parametric/native source with a rendered image or mesh. Avoid repeated STEP/DXF round-trips as a substitute for native feature history.

## 4. Repository structure proposal

Use a predictable source tree under `hardware/charger/V1/CAD/`:

```text
hardware/charger/V1/CAD/
├── README.md
├── standards/
│   ├── CAD-MODELLING-STANDARD.md
│   ├── DATUM-AND-COORDINATE-SYSTEM.md
│   └── LAYER-AND-NAMING-REGISTER.md
├── source/
│   ├── common/
│   ├── wallbox-1/
│   ├── wallbox-2/
│   ├── pedestal-1/
│   ├── pedestal-2/
│   ├── pedestal-4/
│   ├── pedestal-4-cross/
│   └── multistation/
├── components/
│   ├── manufacturer/
│   ├── envelope-only/
│   └── provenance/
├── exchange/
│   ├── step/
│   └── dxf/
├── drawings/
│   ├── review/
│   └── released/
├── configurations/
│   ├── base-public/
│   ├── rfid/
│   ├── ethernet/
│   ├── lte/
│   ├── hmi/
│   └── payment/
├── validation/
│   ├── collision/
│   ├── service-access/
│   ├── cable-routing/
│   └── reports/
└── archive/
```

This is a proposed logical structure, not a statement that all directories or CAD files have already been created. Create directories/files incrementally when the first evidence-backed model is ready.

## 5. Naming, units and revision rules

### 5.1 Naming

Use stable, descriptive identifiers:
- `VZ-EVSE-V1-<VARIANT>-<ASSEMBLY>-R<NN>` for assemblies.
- `VZ-EVSE-V1-COMP-<FUNCTION>-<SKU>` for verified component models.
- `VZ-EVSE-V1-ENV-<FUNCTION>-UNVERIFIED` for explicitly non-dimensional placeholder envelopes.
- `VZ-EVSE-V1-DRW-<VARIANT>-<SUBJECT>-R<NN>` for drawing derivatives.

Do not put a guessed SKU in a filename. Do not label a placeholder as a manufacturer model.

### 5.2 Units and coordinate system

- Use millimetres for mechanical dimensions.
- Use degrees for angular dimensions.
- Define one assembly datum and coordinate orientation per top-level variant.
- Record the datum origin, positive axes, mounting plane and front/service direction in the model README.
- Imported components must preserve manufacturer orientation metadata where available; otherwise record the transformation applied.
- Never infer a mounting datum from an illustrative product photograph.

### 5.3 Revisions

Every model change must record:
- model identifier and revision;
- author/change description;
- affected variant/configuration;
- source evidence added or changed;
- review status;
- compatibility impact on related assemblies/drawings.

Use Git commits for traceability. Binary CAD files may not produce useful textual diffs; therefore include a short companion change log and, where practical, neutral-format exports for review. Do not use generated exports as a substitute for source control.

## 6. Model decomposition and parametric strategy

Build reusable assemblies from controlled subassemblies:

1. **Common enclosure framework:** shared design references and interface datums.
2. **Variant-specific structure:** wallbox, conventional pedestal, cross-quad and future MultiStation structures remain separate.
3. **Electrical panel and DIN support:** geometry only after exact component and mounting data exist.
4. **Per-output cell:** repeatable module for protection, switching, meter, local controller and Type 2 interface; no unverified part placement.
5. **Shared service core:** cluster controller, auxiliary supplies, communications and service access, subject to electrical/thermal evidence.
6. **Optional interface modules:** RFID, HMI, payment, Ethernet, LTE and antenna configurations.
7. **Cable and service envelopes:** separate keep-out/clearance bodies, not physical conductors unless the routing data is known.
8. **Door, cover and blanking assemblies:** include opening/removal motion and sealing interfaces once evidenced.

Prefer named parameters and expressions over duplicated independent dimensions. A parameter must identify its source or be marked as a design variable awaiting approval. Do not create a parametric value that appears exact when it is only a placeholder.

## 7. Configuration strategy

Represent product options as controlled configurations, not ad-hoc copies:

- BASE-PUBLIC (no RFID dependency);
- RFID;
- Ethernet;
- LTE;
- HMI;
- payment terminal/device;
- supported combinations of communications and commercial modules;
- service/maintenance state with access panels open.

Each configuration must demonstrate:
- optional bays are closed with suitable blanking when unused;
- no opening exposes hazardous or ingress-sensitive internals;
- local safety/control is unchanged by optional modules;
- thermal, power and EMC impacts are recorded;
- metrology seals and service access are not obstructed;
- the correct cable, antenna and connector envelopes are present.

A configuration is not supported merely because the CAD software can display its parts.

## 8. Evidence and provenance for component models

For every manufacturer component model, retain a provenance record with:

| Field | Required content |
|---|---|
| Manufacturer | Exact legal/manufacturer name |
| Product | Product family and exact SKU |
| Source | Manufacturer URL or supplied file |
| Source revision/date | Drawing/model revision and publication date if available |
| Retrieved | Retrieval date |
| Geometry type | STEP/native drawing/dimensioned PDF |
| Units | Confirmed units |
| Accuracy | Manufacturer model, simplified model or envelope-only |
| Verification | Critical dimensions cross-checked against datasheet |
| Restrictions | Missing details, excluded accessories or simplifications |

A third-party model repository is not authoritative evidence. It may be used only as a provisional visual aid, clearly labelled and replaced or verified against manufacturer documentation before dimensional design.

If a component lacks a STEP model, create a dimensioned envelope only from its official drawing. If that drawing is unavailable, use a visibly unverified placeholder and keep the relevant CAD gate OPEN.

## 9. CAD validation checks

Before each review snapshot, check:

- missing or unverified component geometry is listed;
- units and assembly datums are consistent;
- no unintended solid intersections exist;
- required clearances are sourced, not guessed;
- door/cover opening and component removal paths are represented;
- cable bend-radius envelopes come from actual cable data;
- cable entries, glands and connectors are included only when evidenced;
- electrical segregation and safety-zone keep-outs follow approved electrical design;
- thermal keep-outs and airflow assumptions are traceable to M1.21;
- wall/base/arm interfaces have structural inputs;
- optional configurations and blanking states are covered;
- model can be reopened in the declared CAD version;
- drawing/export derivatives match the native source revision.

Collision-free geometry alone does not prove electrical safety, thermal adequacy, ingress protection, structural integrity or manufacturability.

## 10. Git and large-file handling

- Keep text standards, provenance records, configuration definitions and review reports in ordinary Git.
- Track native CAD and STEP files only when they are genuine project sources and their size/licensing permits repository storage.
- Avoid committing duplicate exports, caches, autosaves, temporary meshes or application lock files.
- Define a repository size policy before importing large manufacturer libraries.
- Consider Git LFS only after confirming repository/account limits, contributor workflow and backup strategy; do not assume it is enabled.
- Never rewrite history or remove an existing model without preserving the prior revision and documenting the reason.
- Each review snapshot should identify the exact native source revision and generated derivative hashes where practical.

## 11. First controlled CAD pilot

The first pilot should be deliberately small and non-electrical:

1. Confirm the CAD application/version on the workstation.
2. Create a blank native project and verify save/reopen.
3. Establish units, axes, datum and naming standard.
4. Model a simple non-safety-critical enclosure reference block with explicitly declared test dimensions, clearly marked as a software workflow test—not product geometry.
5. Import one manufacturer STEP file only after its exact SKU and source are verified.
6. Compare critical dimensions with its official drawing.
7. Generate one review PDF/STEP derivative and confirm revision linkage.
8. Record the result, application version, test file path and limitations.

Do not use the pilot block as the basis for enclosure dimensions or production geometry.

## 12. M1.23 release gates

| Gate | Acceptance evidence | Status |
|---|---|---|
| C1 — workstation inventory | Actual CAD tool/version recorded | OPEN |
| C2 — native format | Save/reopen test passed | OPEN |
| C3 — exchange formats | STEP/DXF tests passed where applicable | OPEN |
| C4 — modelling standard | Units, datums, naming and revisions approved | OPEN |
| C5 — repository structure | Source tree and large-file policy established | OPEN |
| C6 — provenance | Exact-SKU manufacturer geometry linked to evidence | OPEN |
| C7 — parametric variants | Controlled variant/configuration strategy reviewed | OPEN |
| C8 — validation checks | Collision/service/configuration checks demonstrated | OPEN |
| C9 — review derivatives | Native source and exported review files revision-linked | OPEN |
| C10 — independent review | Mechanical/electrical/thermal review completed | OPEN |

## 13. Inputs still required

- Actual workstation CAD inventory and application versions.
- Exact component SKUs and manufacturer STEP/dimensioned drawings.
- Approved mechanical datums and installation interfaces.
- Cable, gland, connector and bend-radius data.
- Electrical segregation and service-access criteria.
- M1.21 thermal losses and environmental targets.
- Structural loads and wall/foundation details.
- Agreed repository policy for binary CAD and large files.
- Named reviewer and review process.

## 14. Explicit exclusions and status

M1.23 does not:
- assert that FreeCAD or another CAD application is installed;
- create or approve dimensioned enclosure geometry;
- invent component dimensions, mounting holes, cable routes or clearances;
- select final materials, IP/IK ratings or thermal solutions;
- approve electrical layout, protection, wiring or structural calculations;
- release manufacturing drawings, fabrication files or assembly instructions;
- claim collision, thermal, environmental or physical tests have passed.

**Status: CAD TOOLCHAIN AND MODEL-CONTROL FRAMEWORK / OPEN.** This milestone establishes how editable CAD will be controlled. The local application inventory and native-format pilot remain unverified until performed on the workstation. Dimensioned CAD and fabrication remain blocked by M1.21 E1–E10, M1.22 D1–D10 and M1.23 C1–C10 evidence. No mains energisation, fabrication, installation, billing or commercial deployment is authorised.

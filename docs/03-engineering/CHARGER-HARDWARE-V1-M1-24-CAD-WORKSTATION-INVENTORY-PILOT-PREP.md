# VAZÃO EVSE — Charger Hardware V1
## M1.24 — CAD workstation inventory and pilot preparation

**Status:** PREPARED / NOT EXECUTED — WORKSTATION OFFLINE  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.21 enclosure requirements, M1.22 dimensioning/CAD inputs, M1.23 native CAD architecture/model control  
**Purpose:** prepare a safe, reproducible first action on the engineering workstation without claiming access, software presence or test results that have not been observed.

---

## 1. Current execution status

The Desktop Commander device `PC-Vazao-Anjos` was reported OFFLINE at the last access attempt. Therefore:

- the current CAD application inventory is unknown;
- no CAD application/version is confirmed installed;
- no native project was created or reopened;
- no STEP or DXF import/export test was run;
- no mechanical geometry or product dimensions were created;
- M1.24 remains PREPARED / NOT EXECUTED.

This document and the inventory script prepare the next workstation session. They do not close M1.23 C1–C3 or authorise dimensioned CAD.

## 2. Read-only inventory utility

Script:

`tools/cad/Invoke-VazaoCadInventory.ps1`

The script collects:
- computer manufacturer/model and Windows version/build/architecture;
- PowerShell version;
- installed-application records from standard 64-bit, 32-bit and current-user uninstall registry locations;
- known CAD command and executable-path evidence for FreeCAD, AutoCAD, Inventor, Fusion, SOLIDWORKS, BricsCAD, DraftSight, QCAD, LibreCAD and KiCad;
- a clear classification note that KiCad is ECAD, not mechanical CAD.

It writes timestamped JSON and Markdown reports beneath `reports/cad-inventory/` by default.

### Safety properties

- No installation, removal, update, configuration change or application launch.
- No administrator elevation is requested.
- No project files or CAD documents are opened or modified.
- Registry and path matches are evidence of presence only, not proof that an application launches or works.
- Portable installations, custom folders, Store applications and browser-based CAD may be missed.
- The script does not validate licensing, STEP/DXF compatibility, parametric features or native save/reopen.

### Execution command

From the repository root in Windows PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\cad\Invoke-VazaoCadInventory.ps1
```

If the repository is not the current directory, use the full path to the script. The command only bypasses the process execution-policy setting for this invocation; it does not change the machine policy. Review the script before execution. A custom report destination can be supplied with `-OutputDirectory`.

Optional reduced scan:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\cad\Invoke-VazaoCadInventory.ps1 -SkipKnownPathScan
```

The reduced scan still reads uninstall registry entries and command resolution but skips recursive known-path detection.

## 3. First session sequence

1. Confirm the intended workstation is online and identify its device/host name.
2. Confirm repository checkout and branch; do not run against an unrelated working copy.
3. Review the PowerShell script and run the read-only inventory.
4. Preserve both JSON and Markdown reports in the project evidence folder.
5. Review detected product names, versions, executable paths and installation records.
6. Resolve ambiguous or duplicate installations manually; do not infer the active version from a stale registry record.
7. Select the CAD candidate only after considering native parametric assemblies, STEP fidelity, DXF needs, drawing output, scripting, hardware constraints, licensing and repository workflow.
8. Perform a separate controlled native save/reopen test.
9. Perform a separate STEP import/export test with a verified manufacturer model and compare critical dimensions against the official drawing.
10. Record exact application version, test file hashes, results and limitations.

## 4. Native-format pilot — separate test, not part of inventory

The pilot must use a disposable test folder and a deliberately artificial reference object. It must not be mistaken for VAZÃO EVSE product geometry.

Acceptance evidence:
- application starts and exact version is recorded;
- blank native project saves, closes and reopens;
- units are explicitly millimetres;
- origin and X/Y/Z axes are documented;
- a simple non-electrical test solid uses clearly labelled test-only dimensions;
- a verified manufacturer STEP model imports without unexplained scale/orientation changes;
- selected critical dimensions match the official manufacturer drawing within a documented tolerance;
- native source and exported review derivative are linked to the same revision;
- the test can be repeated by another reviewer.

Do not import random third-party models as authoritative component geometry. Do not create mounting holes, clearances, cable paths or enclosure dimensions from photographs.

## 5. Report handling and privacy

The inventory report may contain computer name, manufacturer/model, installed software, installation paths and domain information. Treat it as project-internal technical evidence. Review it before publishing to a public repository. If the repository is public, redact workstation identifiers and unrelated installed-application records while preserving the engineering-relevant CAD evidence in a controlled report.

The script defaults to a report directory inside the repository. Before committing generated reports, review for personal, organisation or licensing information. The script itself is safe to version; generated workstation inventories should be reviewed individually.

## 6. M1.24 acceptance gates

| Gate | Evidence | Status |
|---|---|---|
| W1 — workstation reachable | Device online and host identity confirmed | OPEN |
| W2 — inventory executed | JSON and Markdown reports generated | OPEN |
| W3 — CAD candidates reconciled | Exact product/version/path confirmed | OPEN |
| W4 — toolchain decision | Candidate selected with licensing/hardware rationale | OPEN |
| W5 — native save/reopen | Repeatable test evidence | OPEN |
| W6 — STEP exchange | Verified manufacturer model round-trip/inspection | OPEN |
| W7 — DXF exchange | Units/layers/text test if required | OPEN |
| W8 — repository handling | Native source and review derivative versioned safely | OPEN |
| W9 — independent review | Results and limitations reviewed | OPEN |
| W10 — memory checkpoint | Reports, decision and open issues recorded in AndreOS Memory | OPEN |

## 7. Explicit exclusions

M1.24 preparation does not claim:
- that the workstation is online now;
- that FreeCAD or another CAD application is installed;
- that the inventory script has executed;
- that any CAD application is operational;
- that native save/reopen or STEP/DXF tests passed;
- that any product dimensions, component placement or manufacturing geometry exist;
- that M1.21, M1.22 or M1.23 release gates are closed.

**Current result: preparation complete; execution blocked by workstation availability.** No fabrication release, installation or mains energisation is authorised.

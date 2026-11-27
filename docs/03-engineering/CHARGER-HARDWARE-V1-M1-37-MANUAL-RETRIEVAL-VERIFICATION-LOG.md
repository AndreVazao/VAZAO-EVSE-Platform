# VAZÃO EVSE Charger Hardware V1 — Manual Retrieval and Verification Log (M1.37)

**Status:** OFFICIAL SOURCE LOCATED / ORIGINAL BINARY CUSTODY NOT VERIFIED  
**Date:** 2026-11-27  
**Scope:** Reproducible retrieval and verification of Phoenix Contact CHARX SEC-1000 controlled documentation (item 1139034)  
**Parent:** M1.34 document intake; M1.35 catalog claims review; M1.36 evidence request matrix

## 1. Purpose

This milestone records official retrieval locations and the verification procedure for the exact controller documentation. It closes no technical evidence gate: the original PDF has not been downloaded into project custody, checked for completeness, or SHA-256 hashed.

## 2. Official source locations identified

| Source ID | Location | Intended evidence | Status |
|---|---|---|---|
| SRC-SEC1000-01 | https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034 | Product identity and dynamic catalog claims | Official page identified; capture date recorded in M1.30/M1.34; not controlled manual |
| SRC-SEC1000-02 | https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm | Official manual portal / document revision and applicability | Portal identified; exact SEC-1000 manual binary not archived |
| SRC-SEC1000-03 | https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Ordering_data.htm | Family ordering/compatibility context | Official source identified; not substitute for product manual |
| SRC-SEC1000-04 | https://www.phoenixcontact.com/en-dk/products/ac-charging-controller-charx-sec-1000-1139034 | Cross-locale product data and download area | Official product page inspected; catalog claims only |

## 3. Revision/applicability discovery

An official manual-portal search result identified a manual described as **UM EN CHARX SEC, Revision 06**, with firmware applicability noted as **1.9.1** and date **2026-06-29**. This is discovery metadata only: it is not proof that this is the exact manual applicable to item 1139034 / SEC-1000, nor that the full PDF was retrieved.

Before accepting the revision:
- Verify the title page, document number, revision, publication date, product models and firmware applicability directly in the downloaded PDF.
- Confirm whether the manual applies to SEC-1000 item 1139034 specifically, and whether restrictions differ from SEC-3xxx models.
- Check page count, completeness, appendices, terminal diagrams and revision history.
- Do not extrapolate SEC-3xxx firmware, features, security statements or operating modes to SEC-1000.

## 4. Controlled intake checklist

| Gate | Action | Acceptance evidence | Status |
|---|---|---|---|
| M37-01 | Retrieve manual from official Phoenix Contact source | Original downloaded PDF and source URL | OPEN |
| M37-02 | Record document metadata | Document number, title, revision, date, product/model and firmware applicability from PDF itself | OPEN |
| M37-03 | Preserve original binary | Repository-controlled evidence location or approved project archive; original filename retained | OPEN |
| M37-04 | Compute SHA-256 | Hash computed from archived original file, command/tool and date recorded | OPEN |
| M37-05 | Verify binary integrity/completeness | PDF opens, page count, no truncation/corruption; metadata and revision pages retained | OPEN |
| M37-06 | Review applicability | Reviewer records SEC-1000/item 1139034 applicability and any model/firmware exclusions | OPEN |
| M37-07 | Extract engineering claims | Each claim maps to page/section and exact condition; catalog/manual conflicts tracked | OPEN |
| M37-08 | Independent review | Reviewer and review date recorded; unresolved issues remain explicitly OPEN | OPEN |

## 5. Required archive record

The intake record must contain:

- Original filename (no renaming before custody intake).
- Official source URL and retrieval date/time (UTC).
- Manufacturer document number, title, revision, publication date.
- Exact products/models and firmware applicability.
- File size in bytes and page count.
- SHA-256 digest calculated from the original downloaded file.
- Tool/command and environment used to calculate the digest.
- Archive path and access/backup policy.
- Reviewer, review date and applicability disposition.
- Notes for superseded versions; do not overwrite prior evidence silently.

**Integrity example (run against the actual archived PDF; no hash value is supplied here):**

Windows PowerShell:
```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath ".\ORIGINAL_MANUAL.pdf"
```

Linux/macOS:
```sh
sha256sum ORIGINAL_MANUAL.pdf
```

These examples are procedure only. No file named `ORIGINAL_MANUAL.pdf` is claimed to exist and no hash is claimed.

## 6. Claims that remain unverified pending manual custody

- Complete pin/terminal map and wiring constraints.
- CP/PP state handling, measurement/generation tolerances and fault behavior.
- Contactor interface behavior and permitted external circuit.
- RCM peripheral compatibility, configuration, diagnostic behavior and response timing.
- Meter and RFID interface topology and exact compatible devices.
- Digital output load limitations, simultaneity, thermal/derating conditions and whether external loads affect controller supply figures.
- System bus limits, client/stand-alone restrictions and multi-controller architecture.
- Startup, steady, transient and no-load current conditions.
- Reset, watchdog, brownout, offline and recovery behavior.
- Firmware lifecycle, security support and product-specific CRA/RED documentation.

## 7. Disposition

M1.37 establishes source locations, revision-discovery metadata and a repeatable intake checklist. **Controlled PDF custody, SHA-256, applicability review and all manual-derived technical gates remain OPEN.** Catalog evidence remains preliminary. No controller is selected; no auxiliary supply/rail/fuse/conductor is selected or sized; no schematic/BOM freeze, bench/mains test or energisation is claimed.

## 8. Next action

Retrieve the original official SEC-1000 manual binary and complete M37-01 through M37-08. Only then create a page-referenced technical review, reconcile discrepancies against M1.30/M1.33/M1.35 and update the controller and auxiliary budget evidence gates.

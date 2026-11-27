# VAZÃO EVSE Charger Hardware V1 — Official Manual Source Verification (M1.38)

**Status:** OFFICIAL FILE IDENTITY AND MANUFACTURER-PUBLISHED CHECKSUM FOUND / BINARY NOT YET ACQUIRED  
**Date:** 2026-11-27  
**Product:** Phoenix Contact CHARX SEC-1000, item 1139034  
**Scope:** Resolve the official manual identity, revision discrepancy and binary-integrity intake.

## 1. Purpose and result

M1.37 recorded the official manual portal and a preliminary portal result describing UM EN CHARX SEC, Revision 06, firmware 1.9.1. A separate official product-page download listing has now exposed a specific manual file:

- Filename: `um_en_charx_sec_109999_en_09.pdf`
- Description: UM EN CHARX SEC — CHARX control modular, installing and starting up the charging controller with firmware version 1.9.1
- Manufacturer-listed version: 09
- Manufacturer-listed size: 22.7 MB
- Manufacturer-published SHA-256: `753e7579ab961b85245c4b9cde7a1d4e2741cec7205616fa3d370bfeec0eae7a`

The official product download list identifies the SEC-1000 item 1139034 page and the official manual portal separately. The official portal search result also describes Revision 06 for firmware 1.9.1 and explicitly lists SEC-1000 item 1139034. These records are inconsistent in their revision labels (Revision 06 vs download Version 09). They must not be silently treated as equivalent.

## 2. Official source locations

| ID | Source | Evidence |
|---|---|---|
| M38-S01 | https://www.phoenixcontact.com/fr-be/produits/automate-de-charge-ac-charx-sec-1000-1139034 | Official product page for item 1139034; download table includes manual filename, version, size and SHA-256 |
| M38-S02 | https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm | Official manual portal; result lists UM EN CHARX SEC Revision 06, firmware 1.9.1, including SEC-1000 1139034 |
| M38-S03 | https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034 | Official Portuguese product page for the exact item |
| M38-S04 | https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Ordering_data.htm | Official family ordering/compatibility context |

## 3. Revision discrepancy — mandatory resolution

Observed manufacturer metadata:
- Manual portal: **Revision 06**, firmware 1.9.1, product table includes SEC-1000 item 1139034; portal result says published/reviewed 2026-06-29.
- Product download listing: **Version 09**, filename suffix `_en_09`, firmware 1.9.1, file size 22.7 MB and published checksum.

The terms “Revision” and “Version” may refer to different numbering schemes or separate document generations, but this is not proven. Until the original PDF is inspected:
- Do not overwrite Revision 06 with Version 09 in historical records.
- Do not assume one supersedes the other.
- Inspect title page, document number, revision history, publication date, product/firmware matrix and applicability statements.
- Compare both portal content and product download metadata to the PDF itself.
- If the official download binary says Revision 09 while the portal says Revision 06, record both and request clarification from Phoenix Contact before declaring the controlled-document baseline.

## 4. Checksum handling

The checksum shown above is a **manufacturer-published expected SHA-256**, not a locally computed digest. M38-01 remains OPEN until the exact PDF is downloaded from the official product page and a local SHA-256 calculation matches it byte-for-byte.

Required evidence:
1. Original downloaded file retained without modification.
2. Actual download URL and retrieval timestamp (UTC).
3. Actual byte size and PDF page count.
4. Local SHA-256 command output.
5. Exact match/mismatch against the manufacturer-published checksum.
6. PDF title/revision/date/model/firmware applicability captured from the binary itself.
7. Archive path and reviewer sign-off.

PowerShell:
```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath ".\um_en_charx_sec_109999_en_09.pdf"
```

Linux/macOS:
```sh
sha256sum um_en_charx_sec_109999_en_09.pdf
```

No downloaded PDF, local hash result or archive path is claimed by this milestone.

## 5. Claims newly supported by official product-page listing

The official listing supports the existence of the named manual file, its displayed version/size, firmware 1.9.1 description and manufacturer-published checksum. It does not by itself prove:
- the PDF binary was downloaded or is intact;
- the internal revision and date;
- the complete SEC-1000 applicability details or model-specific restrictions;
- the manual's wiring, terminal, configuration or safety instructions;
- that firmware 1.9.1 is the currently recommended firmware for a new design.

## 6. Technical evidence remains gated

After binary custody and revision reconciliation, extract page-referenced evidence for:
- supply conditions and complete controller current profile;
- all terminals, pin assignments and permitted external circuits;
- contactor output and feedback wiring/operating semantics;
- digital outputs, loading and simultaneous-operation constraints;
- residual-current sensor connection and fault handling;
- RFID and meter compatibility, bus topology and termination;
- temperature sensor configuration;
- bus/backplane architecture, client/stand-alone restrictions and controller combinations;
- startup, brownout, reset, watchdog, communications loss and safe-state behavior;
- firmware lifecycle, security notices and configuration-tool compatibility.

Do not infer a 4-output simultaneous 600 mA budget or treat the floating contact rating as a coil supply. Catalog claims remain bounded by M1.35.

## 7. Gate disposition

| Gate | Description | Status |
|---|---|---|
| M38-01 | Download original official PDF | OPEN |
| M38-02 | Compute local SHA-256 and compare with manufacturer checksum | OPEN |
| M38-03 | Inspect internal revision/date and resolve Rev 06 vs Version 09 | OPEN |
| M38-04 | Confirm SEC-1000 item 1139034 and firmware applicability from PDF | OPEN |
| M38-05 | Preserve binary and provenance metadata in controlled archive | OPEN |
| M38-06 | Produce page-referenced claims matrix | OPEN |
| M38-07 | Independent technical review and discrepancy closure | OPEN |

## 8. Disposition

M1.38 advances official source identification materially but does **not** close controlled binary custody. The manufacturer-published checksum is an expected value only. Revision 06 vs Version 09 is an explicit unresolved discrepancy. No controller is selected; no auxiliary PSU, rail, fuse, conductor or distribution topology is selected/sized; no schematic/BOM freeze, bench/mains test, energisation or compliance approval is claimed.

## 9. Next action

Acquire the exact official PDF binary, verify the local digest against the manufacturer's published SHA-256, inspect the internal revision and applicability, then complete the page-referenced technical claims matrix. If the download cannot be retrieved or the revision conflict persists, request clarification from Phoenix Contact; no supplier contact is claimed in this milestone.

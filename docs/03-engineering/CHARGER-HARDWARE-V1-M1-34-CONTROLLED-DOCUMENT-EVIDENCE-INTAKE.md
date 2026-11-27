# VAZÃO EVSE Charger Hardware V1 — Controlled Document Evidence Intake (M1.34)

**Status:** DOCUMENT INTAKE / CONTROLLED SOURCE CUSTODY OPEN  
**Date:** 2026-11-27  
**Scope:** Establish a traceable intake process and source register for controller and auxiliary-load component documents.

## 1. Purpose and limitations

M1.34 establishes a repeatable evidence-custody process for engineering documents. It distinguishes manufacturer catalog pages, catalog-generated PDFs, controlled manuals, third-party copies and future locally archived originals.

No PDF has been downloaded into the repository in this milestone. No SHA-256 custody hash is claimed. Public web evidence is a discovery reference only and must be superseded by retained original files with revision/date metadata and integrity hashes.

## 2. Document evidence classification

| Class | Evidence type | Acceptable use | Limits |
|---|---|---|---|
| E0 | Search result / third-party listing | Discovery only | Not design evidence |
| E1 | Manufacturer online product/catalog page | Product identity and preliminary catalog claims | Dynamic page; date capture and controlled manual required |
| E2 | Manufacturer catalog-generated PDF | Snapshot of catalog data | Manufacturer warns catalog PDF is not full user documentation |
| E3 | Manufacturer manual with explicit revision, applicability and date | Technical requirements, installation/use details within stated scope | Verify exact product variant, firmware, revision and complete file |
| E4 | Controlled technical document archived with original filename, metadata and SHA-256 | Evidence referenced by engineering review | Must still be reviewed for applicability and gaps |
| E5 | Qualified review / verified test evidence | Closure evidence for designated gates | Scope, reviewer, procedure, equipment, calibration and result must be recorded |

## 3. Source register — controller candidate

| Evidence ID | Product / document | Public discovery source | Preliminary claims visible | Evidence classification | Custody / review status |
|---|---|---|---|---|---|
| DOC-SEC-01 | Phoenix Contact CHARX SEC-1000, item 1139034 — manufacturer PT product page | https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034 | 12 V DC ±5%; range 11.4–12.6 V; max 2 A standalone; <50 mA no-load without external loads; 4 digital outputs max 600 mA each; floating contactor control interface catalog limits; RS-485 interfaces; controller catalog dimensions/environment | E1 | Official page accessed; values preliminary catalog evidence only; capture date recorded in milestone; original downloads and revision still OPEN |
| DOC-SEC-02 | CHARX SEC-1000 catalog PDF generated from online catalog | https://www.phoenixcontact.com/en-us/products/ac-charging-controller-charx-sec-1000-1139034?type=pdf | Catalog snapshot and commercial identity | E2 | Not archived or hashed; manufacturer explicitly points to user documentation for complete information |
| DOC-SEC-03 | CHARX control modular user manual — Firmware 1.6.2, revision 05, dated 2024-09-09; listed applicability includes SEC-1000 item 1139034 | Third-party discovery listing: https://www.notice-facile.com/en/manual/1428556/phoenix%2Bcontact%2Bcharx-sec-1000 | Manual applicability, revision and contents appear in listing; includes installation/startup, safety, product-family and system configuration topics | E0 discovery only | Obtain the exact PDF from manufacturer download channel; verify title page, complete pages, applicability, revision and official source. Do not rely on third-party host as controlled evidence |

**Critical distinction:** The product page and catalog PDF are not substitutes for the full manual. The 2 A catalog figure must not be used as a complete system auxiliary-power budget or supply sizing input.

## 4. Intake record template (one record per source file)

| Field | Required record |
|---|---|
| Evidence ID | Stable ID assigned by engineering |
| Manufacturer / source | Exact publisher and source URL |
| Product / item number | Exact part and variant |
| Document title | Exact title from source file |
| Document number | If stated |
| Revision / issue | Exact revision or issue identifier |
| Publication date | Date shown in document |
| Download / capture date | UTC timestamp |
| Original filename | Preserve filename |
| File format / size | Record |
| SHA-256 | Hash of retained original bytes |
| Applicability | Hardware variant, firmware, serial range or configuration |
| Scope | What claims the document supports |
| Limitations / gaps | What it does not support |
| Evidence class | E0–E5 |
| Review status | OPEN / REVIEWED / ACCEPTED FOR SPECIFIC CLAIMS / REJECTED |
| Reviewer / review date | Named accountable reviewer and date |
| Repository custody path | Location only after file is actually archived |
| Change history | New revision creates new record; do not overwrite original |

## 5. Document custody workflow

1. Locate the document through the manufacturer source or a manufacturer-confirmed channel.
2. Download the original bytes; do not reprint, optimize, merge or rename before recording the original filename.
3. Record capture date, source URL, title, document number, revision, date, exact product applicability and file size.
4. Calculate SHA-256 on the original downloaded file.
5. Store the original in the approved evidence archive. A future repository path must be assigned only after the file exists and storage/retention is approved.
6. Review the document for specific claims; reference page/section and claim IDs.
7. Mark each claim independently as supported, conflicting, obsolete, incomplete or not applicable.
8. Preserve superseded revisions; add a new evidence record instead of silently replacing.
9. Never state that a file is archived, hashed or controlled until the operation is verified.

## 6. Claims to verify in the controlled SEC-1000 manual

| Claim ID | Claim / parameter | Catalog discovery value | Manual evidence required | Status |
|---|---|---|---|---|
| SEC-C01 | Supply voltage and tolerance | 12 V DC ±5% | Exact input requirements and operation across conditions | OPEN |
| SEC-C02 | Stand-alone consumption | Max 2 A catalog statement | Conditions, scope, peripherals included/excluded, profile | OPEN |
| SEC-C03 | No-load consumption | <50 mA without external loads | Defined no-load condition, measurement and exclusions | OPEN |
| SEC-C04 | Digital output limits | Catalog max 600 mA each | Per-channel vs total limits, thermal/derating, protection and simultaneous loading | OPEN |
| SEC-C05 | Contactor control output | Catalog floating-contact limits | Wiring, isolation, contact rating conditions, external coil requirements | OPEN |
| SEC-C06 | RFID / meter / residual-current interfaces | Supported peripherals listed | Exact compatible modules, supply requirements and load contribution | OPEN |
| SEC-C07 | Temperature inputs | Pt1000/PTC listed in catalog | Sensor types, wiring, thresholds/configuration and faults | OPEN |
| SEC-C08 | Firmware/configuration applicability | Manual listing reports firmware 1.6.2 | Official document version, supported hardware, update/recovery rules | OPEN |
| SEC-C09 | Safety instructions and limitations | Catalog summary only | Complete safety sections and warnings | OPEN |
| SEC-C10 | Environmental limits | Catalog values present | Mounting, thermal/environmental conditions and derating context | OPEN |

## 7. Conflict and uncertainty handling

- If catalog and manual values differ, retain both claims with source/revision and raise a conflict; do not silently select one.
- If a datasheet uses “maximum,” “typical,” “standby” or “peak,” preserve the exact term and test condition.
- Missing peripheral data remains OPEN and is not inferred from controller outputs.
- Third-party copies may assist discovery but are not accepted as controlled source custody.
- Firmware-dependent features require firmware applicability to be documented separately from hardware identity.
- Any supplier response must be recorded as dated evidence with contact/source context and, where possible, written confirmation.

## 8. Evidence intake gates

| Gate | Description | Status |
|---|---|---|
| DI-01 | Official SEC-1000 manual downloaded and exact revision verified | OPEN |
| DI-02 | Original PDF archived and SHA-256 recorded | OPEN |
| DI-03 | Manual applicability to item 1139034/hardware revision verified | OPEN |
| DI-04 | Controller supply/consumption claims reviewed against manual | OPEN |
| DI-05 | Peripheral/module compatibility and power requirements captured | OPEN |
| DI-06 | Contactor-control interface limits reviewed | OPEN |
| DI-07 | Exact candidates for other auxiliary loads documented from manufacturer sources | OPEN |
| DI-08 | Evidence claims mapped to M1.33 budget rows | OPEN |
| DI-09 | Qualified engineering review of evidence applicability completed | OPEN |

## 9. Next action and disposition

M1.34 creates the source register, custody workflow, evidence classes and verification checklist. It does not claim that a controlled manual has been obtained or archived. No SHA-256 hashes, supplier confirmations, component selections, auxiliary budget totals, schematic/BOM freeze, tests or energisation are claimed.

Next: obtain the exact official manual/download, retain its original file and metadata, hash it, review relevant pages and update M1.33 only with claim-level evidence. Continue only one open work PR at a time.

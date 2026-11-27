# VAZÃO EVSE — Charger Hardware V1

**Status:** DRAFT / ENGINEERING BASELINE  
**Active work branch:** `work/charger-hardware-m1-33-auxiliary-power-budget`
**Branch:** `feat/charger-hardware-v1`  
**Scope:** AC EVSE modular, starting with single-output 22 kW Type 2 and designed for reuse in dual/quad/wallbox variants.

## Purpose

This document set defines the first hardware baseline of the VAZÃO EVSE charger family. The charger is a core product of the **VAZÃO EVSE Platform**, not a separate project.

## Product family

- Wallbox — 1 output
- Wallbox — 2 outputs
- Pedestal — 1 output
- Pedestal — 2 outputs
- Pedestal — 4 outputs, preferred cross layout
- MultiStation — multiple chargers under a local Master Controller
- Private/offline variant — no CPMS connectivity and no managed maintenance

## Engineering principles

1. Modular electrical architecture.
2. Reuse of the same controller, measurement and communication modules wherever practical.
3. Local safety functions must not depend on cloud connectivity.
4. Charging shall stop safely on critical faults.
5. Online operation and offline operation are first-class modes.
6. The CPMS manages commercial and fleet functions; the EVSE remains safe and operational locally.
7. The VAZÃO EVSE TestStation shall eventually be able to validate the same hardware interfaces and safety states.

## Documents

- `docs/01-requirements/CHARGER-HARDWARE-V1-REQUIREMENTS.md`
- `docs/02-architecture/CHARGER-HARDWARE-V1-ELECTRICAL-ARCHITECTURE.md`
- `docs/02-architecture/CHARGER-HARDWARE-V1-CONTROL-COMMUNICATIONS.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-WIRING-SCHEDULE.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-INTERNAL-ASSEMBLY.md`
- `docs/04-bom/CHARGER-HARDWARE-V1-BOM.md`
- `docs/05-decisions/ADR-001-AC-22KW-FIRST-PROTOTYPE.md`

## Recovered milestones

- [M1.1 — Component Selection Gate](../03-engineering/CHARGER-HARDWARE-V1-COMPONENT-SELECTION-GATE.md)
- [M1.2 — Evidence-backed Component Candidates](../03-engineering/CHARGER-HARDWARE-V1-COMPONENT-CANDIDATES-M1-2.md)
- [M1.3 — Controller Interface Review](../03-engineering/CHARGER-HARDWARE-V1-CONTROLLER-INTERFACE-REVIEW-M1-3.md) — recovered and merged; controller selection remains OPEN.
- [M1.4A — Phoenix CHARX 2902802 Interface Review](../03-engineering/CHARGER-HARDWARE-V1-PHOENIX-CHARX-2902802-INTERFACE-REVIEW-M1-4A.md) — merged; manufacturer-document review remains partial and not approved for wiring.
- [M1.23 — AC Feeder Topology and Conductor Sizing Design Basis](../03-engineering/CHARGER-HARDWARE-V1-M1-23-AC-FEEDER-TOPOLOGY-AND-CONDUCTOR-SIZING.md) — merged; independent and common dual/quad feeder alternatives defined, cable sections remain installation-calculation dependent.
- [M1.24 — Local Load Management Interface and Fail-Safe Contract](../03-engineering/CHARGER-HARDWARE-V1-M1-24-LOCAL-LOAD-MANAGEMENT-INTERFACE.md) — merged; local measurement, allocation, acknowledgement and fail-safe requirements defined.
- [M1.25 — Local Load Manager Candidate Evidence Matrix](../03-engineering/CHARGER-HARDWARE-V1-M1-25-LOCAL-LOAD-MANAGER-CANDIDATES.md) — merged; five manufacturer-described options compared, no candidate selected.
- [M1.26 — Supplier Technical Evidence Request](../03-engineering/CHARGER-HARDWARE-V1-M1-26-SUPPLIER-TECHNICAL-EVIDENCE-REQUEST.md) — merged internal RFI template; not sent to suppliers.
- [M1.27 — Local Load Management Verification and TestStation Acceptance Plan](../03-engineering/CHARGER-HARDWARE-V1-M1-27-LOAD-MANAGEMENT-TEST-PLAN.md) — merged test-plan gate; no tests claimed executed.
- [M1.28 — Repeatable Output Channel Architecture and Operating State Model](../03-engineering/CHARGER-HARDWARE-V1-M1-28-REPEATABLE-OUTPUT-CHANNEL-ARCHITECTURE.md) — merged functional architecture baseline; no hardware selected or schematic released.
- [M1.29 — Single-Output Prototype Requirements-to-Interface Traceability Matrix](../03-engineering/CHARGER-HARDWARE-V1-M1-29-SINGLE-OUTPUT-INTERFACE-TRACEABILITY.md) — merged traceability baseline; no components selected or schematic released.
- [M1.30 — EVSE Controller Evidence Review](../03-engineering/CHARGER-HARDWARE-V1-M1-30-EVSE-CONTROLLER-EVIDENCE-REVIEW.md) — merged catalog review; controller remains unselected, controlled PDFs not archived.
- [M1.31 — Protection Architecture Evidence Matrix](../03-engineering/CHARGER-HARDWARE-V1-M1-31-PROTECTION-ARCHITECTURE-EVIDENCE-MATRIX.md) — merged protection boundaries and evidence gates; no device selection or schematic release.
- [M1.32 — Contactor and Feedback Architecture](../03-engineering/CHARGER-HARDWARE-V1-M1-32-CONTACTOR-FEEDBACK-ARCHITECTURE.md) — merged switching requirements and feedback semantics; no actuator selected or tests run.
- [M1.33 — Auxiliary Power Budget Evidence Matrix](../03-engineering/CHARGER-HARDWARE-V1-M1-33-AUXILIARY-POWER-BUDGET-EVIDENCE-MATRIX.md) — auxiliary load inventory and calculation/evidence gates; no PSU, rail or distribution selected.
- [M1.34 — Controlled Document Evidence Intake](../03-engineering/CHARGER-HARDWARE-V1-M1-34-CONTROLLED-DOCUMENT-EVIDENCE-INTAKE.md) — evidence classes, custody workflow, SEC-1000 source register and claims checklist; controlled manual custody still OPEN.
- [M1.35 — Controller Catalog Claims Review](../03-engineering/CHARGER-HARDWARE-V1-M1-35-CONTROLLER-CATALOG-CLAIMS-REVIEW.md) — bounded interpretation of catalog values, non-assumptions and closure gates; controlled evidence OPEN.
- [M1.36 — Controller Evidence Request Matrix](../03-engineering/CHARGER-HARDWARE-V1-M1-36-CONTROLLER-EVIDENCE-REQUEST-MATRIX.md) — manufacturer document requests, clarification questions and draft outreach; no contact made.

## Safety status

This is an engineering/documentation baseline, **not a construction certificate or installation drawing**. Any mains-connected prototype must be reviewed and tested by a suitably qualified electrical engineer, and the production design must be validated against the applicable EU/Portuguese requirements and EVSE standards before deployment.

## Engineering drawings

- [Functional electrical architecture](../../hardware/charger/V1/CAD/diagrams/VAZAO-EVSE-V1-ELECTRICAL-ARCHITECTURE.svg)
- [Internal panel layout](../../hardware/charger/V1/CAD/diagrams/VAZAO-EVSE-V1-INTERNAL-PANEL-LAYOUT.svg)

## Current engineering baseline

The V1 baseline separates the local safety boundary from CPMS communications, defines the functional power/control architecture, establishes the internal panel zoning, and records the preliminary BOM. The drawings are conceptual engineering artefacts and are not authorisation for mains energisation.

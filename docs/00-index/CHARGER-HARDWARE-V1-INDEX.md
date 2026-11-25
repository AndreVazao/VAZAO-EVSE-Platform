# VAZÃO EVSE — Charger Hardware V1

**Status:** DRAFT / ENGINEERING BASELINE  
**Active work branch:** `work/charger-hardware-m1-4a-charx-advanced-manual-audit`  
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
- [M1.4A — Phoenix CHARX 2902802 Interface Review](../03-engineering/CHARGER-HARDWARE-V1-PHOENIX-CHARX-2902802-INTERFACE-REVIEW-M1-4A.md) — recovered and refreshed with official product-page and manual C05 evidence; remains OPEN, not approved for wiring.

M1.4A covers only the legacy CHARX control advanced 2902802. It must not be conflated with the newer CHARX control modular SEC-1000/SEC-3xxx family reviewed in later historical milestones. Later milestones will be ported in dependency-aware PRs.

## Safety status

This is an engineering/documentation baseline, **not a construction certificate or installation drawing**. Any mains-connected prototype must be reviewed and tested by a suitably qualified electrical engineer, and the production design must be validated against the applicable EU/Portuguese requirements and EVSE standards before deployment.

## Engineering drawings

- [Functional electrical architecture](../../hardware/charger/V1/CAD/diagrams/VAZAO-EVSE-V1-ELECTRICAL-ARCHITECTURE.svg)
- [Internal panel layout](../../hardware/charger/V1/CAD/diagrams/VAZAO-EVSE-V1-INTERNAL-PANEL-LAYOUT.svg)

## Current engineering baseline

The V1 baseline now separates the local safety boundary from CPMS communications, defines the functional power/control architecture, establishes the internal panel zoning, and records the preliminary BOM. The drawings are conceptual engineering artefacts and are not authorisation for mains energisation.

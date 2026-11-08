# VAZÃO EVSE — Charger Hardware V1

**Status:** DRAFT / ENGINEERING BASELINE  
**Baseline branch:** `main`  
**Active engineering branch:** `feat/charger-hardware-v1-component-selection`  
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
- `docs/03-engineering/CHARGER-HARDWARE-V1-COMPONENT-SELECTION-GATE.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-COMPONENT-CANDIDATES-M1-2.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-CONTROLLER-INTERFACE-REVIEW-M1-3.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-PHOENIX-CHARX-2902802-INTERFACE-REVIEW-M1-4A.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-BENDER-CC613-INTERFACE-REVIEW-M1-4B.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-MODULAR-CONTROLLER-ARCHITECTURE-REVIEW-M1-5.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-CHARX-MODULAR-MANUAL-INTERFACE-EXTRACTION-M1-5A.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-QUAD-MODULAR-ARCHITECTURE-M1-6.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-MODULE-COMPATIBILITY-AND-INTERFACES-M1-7.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-CHARX-QUAD-TOPOLOGY-AND-CONNECTOR-REGISTER-M1-8.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-CHARX-QUAD-METERING-FAULT-CONTAINMENT-POWER-BUDGET-M1-9.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-CHARX-COMPONENT-LIFECYCLE-AND-PERIPHERAL-REVIEW-M1-10.md`
- `docs/04-bom/CHARGER-HARDWARE-V1-BOM.md`
- `docs/05-decisions/ADR-001-AC-22KW-FIRST-PROTOTYPE.md`

## Safety status

This is an engineering/documentation baseline, **not a construction certificate or installation drawing**. Any mains-connected prototype must be reviewed and tested by a suitably qualified electrical engineer, and the production design must be validated against the applicable EU/Portuguese requirements and EVSE standards before deployment.


## Engineering drawings

- [Functional electrical architecture](../../hardware/charger/V1/CAD/diagrams/VAZAO-EVSE-V1-ELECTRICAL-ARCHITECTURE.svg)
- [Internal panel layout](../../hardware/charger/V1/CAD/diagrams/VAZAO-EVSE-V1-INTERNAL-PANEL-LAYOUT.svg)
- [Provisional component zoning — M1.3](../../hardware/charger/V1/CAD/diagrams/VAZAO-EVSE-V1-PROVISIONAL-COMPONENT-ZONING-M1-3.svg)

## Current engineering baseline

M1.6 now defines mandatory modular product architecture: a safe charging core per output plus physically prepared, optional RFID, communications, HMI, payment and service modules. It decomposes the quad pedestal into four repeatable output cells and shared services, and records fault-containment and release gates. Exact controller count, bus topology, per-output meter wiring and failure isolation remain unverified and are explicitly deferred to M1.7. The V1 baseline now separates the local safety boundary from CPMS communications, defines the functional power/control architecture, establishes the internal panel zoning, records the preliminary BOM, and adds the M1.3 controller-interface review matrix and the M1.4A/M1.4B manufacturer-interface evidence reviews. Phoenix terminal-level documentation remains incomplete; Bender CC613 is marked discontinued by its manufacturer and is blocked for procurement. The new component-zoning drawing is provisional and not a dimensioned mounting plate or wiring instruction. These drawings are not authorisation for mains energisation.


### M1.9 — metering, RFID failure and cluster fault containment

M1.9 records Phoenix Contact evidence for per-charging-point energy measurement and load management, the explicit RFID-reader-absent error condition, and the shared SEC-3xxx/SEC-1000 backplane/server dependencies. The quad assembly is therefore described as four locally controlled outputs in a shared cluster—not as four fully autonomous units—until server, client and bus fault-injection tests pass. The 6 A backplane limit remains a hard constraint; no PSU or branch protection rating is selected. Exact meter SKU, terminal schedule, 12 V load budget and fault recovery remain open. This is not a released wiring or energisation design.


### M1.10 — component lifecycle and peripheral candidates

M1.10 adds manufacturer data for the CHARX RFID/NFC-PCB (1391227), EV-RCM-6DC-WAT (1309697), accessory cable 1360462 and 12 V STEP3 supply 1170953. It identifies the previously shortlisted ISKRA WM3M4C meter 1429603 as no longer in the Phoenix Contact product range and blocks new procurement. The 2.5 A PSU is explicitly not approved for the quad cluster. Current meter replacement/CHARX compatibility, exact terminal-level pinout, approved cluster feed and complete power budget remain open. No BOM or wiring release is made.


### M1.11 — wiring evidence, meter lifecycle and 12 V power-budget closure

M1.11 identifies the official CHARX UM EN Revision 06 / firmware 1.9.1 manual and supported controller variants, while keeping the connector register functional rather than terminal-numbered because the complete wiring figures and exact terminal schedule were not extractable from the accessible manual landing page. It confirms EEM-MA370-R 2907980 as a Modbus RTU/TCP investigation candidate only; MID certification, direct/CT topology, CHARX integration and billing suitability remain unverified. EEM-MA370 2907983 is a distinct Modbus/TCP CT-input model and is not a drop-in replacement. The 12 V budget is formalised into separate controller/backplane, auxiliary, contactor-coil and safety domains; the 6 A nominal backplane limit remains hard, and no PSU is selected. The 1/2/4-output load schedules, terminal-level wiring, meter selection and SELV fault-injection remain open. No production BOM, wiring or energisation release.

- `docs/03-engineering/CHARGER-HARDWARE-V1-M1-11-WIRING-METER-POWER-BUDGET-CLOSURE.md`


### M1.12 — MID meter candidate and lifecycle review

M1.12 identifies Phoenix Contact EEM-XM375 1674510 as the strongest current MID candidate found: three-phase, CT 1 A/5 A, Modbus/TCP Ethernet, bidirectional, MID 2014/32/EU and manufacturer-stated class C EN 50470-3. It remains a candidate only: CT chain, certificate scope, CHARX profile, per-output transaction attribution and Portuguese billing suitability are open. Corrected lifecycle: EEM-EM355 2908578 is marked no longer in product range and its manufacturer-listed replacement is EEM-XM355 1674509; do not procure 2908578 for new design. EEM-MA370-R 2907980 supports Modbus RTU/TCP but MID was not evidenced on its reviewed page. No production meter is selected.

- `docs/03-engineering/CHARGER-HARDWARE-V1-M1-12-MID-METER-CANDIDATE-AND-LIFECYCLE-REVIEW.md`

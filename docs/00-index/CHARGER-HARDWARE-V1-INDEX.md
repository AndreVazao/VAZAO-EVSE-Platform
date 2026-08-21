# VAZÃO EVSE — Charger Hardware V1

**Status:** DRAFT / ENGINEERING BASELINE  
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

## Safety status

This is an engineering/documentation baseline, **not a construction certificate or installation drawing**. Any mains-connected prototype must be reviewed and tested by a suitably qualified electrical engineer, and the production design must be validated against the applicable EU/Portuguese requirements and EVSE standards before deployment.

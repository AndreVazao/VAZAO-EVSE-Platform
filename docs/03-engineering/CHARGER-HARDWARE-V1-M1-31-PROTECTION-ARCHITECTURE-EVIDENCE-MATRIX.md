# VAZÃO EVSE Charger Hardware V1 — Protection Architecture Evidence Matrix (M1.31)

**Status:** SAFETY ARCHITECTURE / EVIDENCE GATE — NO PROTECTIVE DEVICE SELECTED  
**Date:** 2026-11-27  
**Scope:** Single-output AC Mode 3 prototype, reusable protection boundary for each Output Cell  
**Parent:** M1.28 output-cell model, M1.29 interface traceability, M1.30 controller evidence review

## 1. Purpose and strict limitations

Establish the protection-function boundaries and evidence required before selecting protective devices, drawing a mains schematic, dimensioning conductors or authorizing a prototype build. This is an engineering requirements matrix, not a protective-device specification, wiring instruction, compliance declaration, or authorization to energize.

The protection architecture must be independently local to every output. Multi-output feeder/distribution arrangements and load-management control must not defeat individual output safety functions. Internet, CPMS and remote commands cannot be prerequisites for safe disconnection.

## 2. Functional boundary — conceptual only

For each output, the engineering design must identify and verify these functional layers, with their exact physical implementation still OPEN:

1. Installation/feeder protection and isolation upstream of charger.
2. Charger incoming protection and distribution.
3. Protective-earth continuity and bonding.
4. Residual-current protection strategy, including AC residual-current and smooth DC detection/response as applicable to the final design and applicable rules.
5. Per-output overcurrent/short-circuit protection coordination.
6. Per-output switching/contactor function with feedback and fault containment.
7. EVSE controller/CP state and authorization of power, subordinate to safety functions.
8. Output connector/cable and temperature/thermal protection where required by final design.
9. Surge/overvoltage protective strategy, coordinated with installation and equipment.
10. Emergency/service isolation, lockout and safe maintenance access.

No device type, trip curve, current rating, residual-current threshold, voltage rating, pole count, breaking capacity, conductor cross-section, contactor or protective coordination has been selected in this milestone.

## 3. Protection-function evidence matrix

| ID | Function / hazard | Required engineering definition | Evidence required | Status |
|---|---|---|---|---|
| P-01 | Supply isolation | Scope and location of upstream and charger isolation; service/maintenance access | Installation assumptions, drawing, isolation/lockout procedure, ratings | OPEN |
| P-02 | Overcurrent / short circuit | Fault levels at installation and charger; protective-device coordination with feeder, branch and components | Fault-current calculation, manufacturer curves, breaking capacity, coordination/selectivity study | OPEN |
| P-03 | Residual AC current | Applicable residual-current protection type and coverage per output and installation rules | Standards edition review, selected-device data, coordination and verification plan | OPEN |
| P-04 | Smooth DC residual current | Required DC detection/response arrangement; interaction with upstream RCD and per-point system | Exact detector/controller compatibility, thresholds/time response from controlled docs, test method | OPEN |
| P-05 | PE and bonding | Protective conductor continuity, enclosure/door/panel bonding, connector PE path, fault loop | Electrical design, materials/terminals, continuity and fault-loop test plan/results | OPEN |
| P-06 | Contactor / switching | Rated duty, switching coordination, fail-open state, feedback and welded-contact detection | Exact contactor/coil docs, controller interface, feedback design, fault analysis | OPEN |
| P-07 | CP/PP safety signalling | State transition and invalid-signal handling; safe power-enable conditions | Controller manual, state table, CP/PP interface calculations, independent tests | OPEN |
| P-08 | Surge / transient | Installation exposure and upstream coordination; charger withstand | Installation assessment, applicable standards, SPD coordination and manufacturer data | OPEN |
| P-09 | Thermal / temperature | Enclosure, terminals, contactor, conductor, connector and ambient limits | Thermal calculations, sensors/limits, derating data, verification under worst case | OPEN |
| P-10 | Connector/cable | Type 2 interface, current rating, temperature, strain relief, cable/connector variants | Component certificates/datasheets, mechanical and thermal integration, inspection/test plan | OPEN |
| P-11 | Auxiliary SELV/control | Separation, overcurrent, grounding strategy, fault propagation and source sizing | PSU datasheet, circuit design, segregation/creepage/clearance analysis, load budget | OPEN |
| P-12 | Metering separation | Safety/protection measurement vs energy/revenue metering roles | Interface/control diagram, meter documentation, independent safety measurement proof | OPEN |
| P-13 | Local safe-state | Defined response to controller reset, brownout, communications loss, sensor invalidity, safety-device trip | FMEA/Fault tree, state transitions, watchdog, verification cases | OPEN |
| P-14 | Multi-output fault containment | Fault on one Output Cell must not compromise other outputs or shared safety | Architecture, shared feeder limits, distribution fault study, test cases | OPEN |
| P-15 | Service/test interface | Safe diagnostic access without bypassing protections or energizing outputs unintentionally | Interface definition, access control, isolation boundary, service test procedure | OPEN |
| P-16 | Emergency/service stop | Applicability and implementation, including service-only isolation vs user emergency-stop requirement | Risk assessment, standards review, functional specification and verification | OPEN |

## 4. Required safe-state contract (to be verified, not assumed)

- Loss or invalidity of safety-critical sensing must not permit charging power to be enabled.
- Controller restart, brownout or watchdog reset must not produce an unintended re-energisation.
- Loss of CP/PP validity or an EVSE state not authorizing energy must inhibit/stop output power.
- Residual-current protection must act independently of CPMS, cloud, RFID, payment and user interface.
- Load manager may request a bounded power allocation, but cannot override local safety/protection trips.
- Protective device operation must latch or require defined recovery where the risk analysis calls for it; automatic retry behavior is OPEN.
- A detected contactor feedback mismatch must prevent unsafe reuse of that output until the recovery rule is defined and validated.
- Faults shared through feeder/distribution/control must be analyzed explicitly; individual-output isolation does not eliminate upstream common-mode hazards.

These are requirements to be verified against selected components and standards, not statements about candidate hardware capability.

## 5. Standards and conformity evidence gate

The design team must establish the applicable editions and national adoption before design decisions. The following standards families are listed as review targets only; edition, amendments, national adoption, scope and applicability have not been verified in this milestone:

- IEC/EN 61851 series — electric vehicle conductive charging system requirements and EVSE operation.
- IEC/HD 60364-7-722 — installation requirements for EV supply circuits.
- IEC 62955 — residual direct current detecting device (RDC-DD) for Mode 3 charging.
- Relevant IEC/EN 61008 / 61009 / 62423 family — RCD/RCCB/RCBO device characteristics and type selection, subject to application and edition review.
- IEC/EN 61439 series — assembly requirements where the charger enclosure/assembly falls within scope.
- IEC/EN 60664 series — insulation coordination, clearances and creepage where applicable.
- IEC/EN 62305 and/or applicable SPD product standards — lightning/surge risk and protection assessment, subject to installation conditions.

This list is not exhaustive and must not be interpreted as a conformity determination. Confirm the current applicable standards and Portuguese/EU regulatory obligations through controlled sources before prototype and product compliance planning.

## 6. Design inputs required before calculations

The protection design cannot be completed until these inputs are recorded:
- supply system (earthing arrangement), nominal voltage and frequency;
- maximum prospective fault current and upstream protective device;
- feeder length, conductor material, installation method, ambient and grouping;
- charger rated current and intended output power/current envelope;
- Single/dual/quad topology and whether feeders are independent or common;
- enclosure location, IP/environmental exposure, temperature and ventilation;
- cable/connector form (socket or tethered), connector ratings and thermal sensors;
- optional modules and their power/communications demand;
- required local operation/offline modes and maintenance access;
- installation, inspection and verification requirements.

## 7. Gate criteria before schematic release

All gates must be closed with controlled evidence and reviewed calculations:
- Applicable standards/editions and regulatory scope recorded.
- Fault-current and feeder/branch conductor calculations complete.
- RCD/RDC-DD architecture and device compatibility supported by controlled manufacturer documentation.
- PE/bonding and fault-loop approach defined.
- Contactor and feedback architecture proven against local safe-state contract.
- Surge, thermal, connector and enclosure design basis recorded.
- Safety-critical and commercial metering functions clearly separated.
- FMEA/fault tree and verification cases reviewed.
- Per-output fault containment and common-feeder hazards analyzed.
- Safety review signed by qualified responsible engineer before energisation.

## 8. Next milestone

M1.32 should focus on contactor/switching and feedback architecture evidence, including candidate ratings only after electrical assumptions and protection boundary are defined. Do not prematurely dimension or select devices. Auxiliary supply budget follows once controller and peripheral candidates have controlled manuals and load data.

## 9. Traceability / disposition

M1.31 establishes the function and evidence matrix only. All P-01 through P-16 remain OPEN. No protective component selected, no numerical trip threshold or conductor section approved, no schematic/BOM released, no hardware test or mains energisation claimed.

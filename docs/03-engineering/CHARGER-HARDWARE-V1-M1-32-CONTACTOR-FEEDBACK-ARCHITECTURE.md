# VAZÃO EVSE Charger Hardware V1 — Contactor and Feedback Architecture (M1.32)

**Status:** INTERFACE REQUIREMENTS / NO CONTACTOR SELECTED  
**Date:** 2026-11-27  
**Scope:** Single Output Cell switching boundary, reusable for AC charger family  
**Parent:** M1.28 output-channel state model; M1.29 interface traceability; M1.31 protection architecture matrix

## 1. Purpose

Define the switching function and feedback interface requirements before candidate contactor/relay selection. This document is not a schematic, rating specification, wiring guide, or approval to energize. Actual switching-device selection requires recorded supply, installation, fault-current, current envelope, controller interface and protective coordination data.

## 2. Functional separation

Conceptually, every Output Cell must distinguish:

- **Safety/protection boundary:** protection functions and the decision to prevent unsafe power delivery. Device details remain OPEN.
- **Switching actuator:** physical switching element(s) that establish or interrupt the power path. Exact contact topology, number of poles and device class remain OPEN.
- **Command interface:** EVSE controller's request/drive interface, subject to manufacturer limits and a defined safe-state contract.
- **Feedback interface:** independently observed switching state, with defined interpretation of mismatch and failure.
- **Measurement:** current/voltage/energy monitoring must not be confused with contact-state proof; meter readings alone are not approved as proof of contactor opening.
- **Service boundary:** isolation and maintenance access requirements; diagnostic/test interface must not create unintended switching.

## 3. Requirements and evidence matrix

| ID | Requirement | Evidence needed | Status |
|---|---|---|---|
| SW-01 | Device is suitable for EVSE switching duty and declared electrical load | Manufacturer datasheet, applicable duty/category, life-cycle data, application notes | OPEN |
| SW-02 | AC system voltage and current envelope are defined before rating selection | Design input record, load envelope, supply/topology assumptions | OPEN |
| SW-03 | Fault current and upstream protection coordination are considered | Fault-current study, breaking/short-circuit coordination evidence and manufacturer limits | OPEN |
| SW-04 | Switching element(s) and poles are defined for required isolation function | Applicable standards review, circuit topology, isolation assessment | OPEN |
| SW-05 | Controller output interface is compatible with actuator drive | Controller manual, coil voltage/current, interface ratings, transient suppression compatibility | OPEN |
| SW-06 | Actuator defaults to safe power-off on loss of control power, where required by design | Manufacturer documentation, state/fault analysis, bench verification plan | OPEN |
| SW-07 | Feedback identifies commanded vs actual switching state | Feedback contact/interface documentation, signal conditioning, state truth table | OPEN |
| SW-08 | Welded/stuck contact detection is defined | Detection method, independent observation path, failure analysis and test cases | OPEN |
| SW-09 | Feedback disagreement causes defined inhibit/latched fault and prevents reuse | State machine, recovery policy, verification cases | OPEN |
| SW-10 | Auxiliary power and transient loads fit supply budget | Coil data, inrush/holding, suppression, all option-module load budget | OPEN |
| SW-11 | Thermal limits and derating are satisfied | Manufacturer data, enclosure/terminal calculations, test plan | OPEN |
| SW-12 | Device/terminal assembly is mechanically serviceable | Mounting, spacing, torque, wiring access, enclosure/layout review | OPEN |
| SW-13 | Switching behavior under reset, brownout and communications loss is deterministic | Controller/actuator docs, fault-state table, test cases | OPEN |
| SW-14 | Output fault does not defeat other output safety boundaries | Cell and shared-feeder fault analysis, multi-output acceptance cases | OPEN |
| SW-15 | Maintenance isolation and safe test procedure prevent accidental energisation | Risk review, lockout procedure, access control, service documentation | OPEN |

## 4. Feedback semantics — logical requirements only

Feedback must be defined as a state observation, not merely a controller command echo. Before device selection, the design must decide and document:

- whether feedback is auxiliary contact(s), another certified/qualified sensing method, or a combination;
- whether the feedback path is independent enough to detect the relevant welded/stuck failure;
- expected state when command is OFF and ON, including transitional and invalid states;
- debounce/filtering and maximum permitted observation time (numerical limits remain OPEN pending component and standards evidence);
- how disagreement is logged, inhibits output, latches or recovers;
- what conditions permit fault clearing, reset and return to service;
- how feedback is checked in the prototype verification plan without creating hazardous live conditions.

**Required conceptual truth table (values/timeout still OPEN):**

| Command | Observed feedback | Interpretation | Required response |
|---|---|---|---|
| OFF | OFF/confirmed open | Expected open state | Output remains inhibited |
| OFF | ON/closed indication | Unexpected closed / welded-risk state | Fault, inhibit, no reuse pending defined recovery |
| ON | ON/closed indication | Expected commanded state, subject to other safety checks | Charging may proceed only if every other permissive is valid |
| ON | OFF/open indication | Failed to close / feedback mismatch | Stop/inhibit, fault handling |
| Either | Invalid/ambiguous feedback | Cannot prove switching state | Treat as unsafe/unknown, inhibit and fault |

The meaning of “ON/closed” and “OFF/open” must be verified against the selected device's actual feedback contact and signal circuit. This truth table is a requirement, not a claim that a candidate actuator provides suitable feedback.

## 5. Output Cell command contract

- A power-enable command is issued only after all locally required permissives and safety states are valid.
- Local protection trip or safety fault overrides charging command and energy-manager allocation.
- No cloud, CPMS, RFID/payment, HMI or remote test request can override the local protection boundary.
- Reset, brownout, controller restart, communication loss or invalid feedback cannot cause uncommanded power re-application.
- Output-cell fault and recovery policy must not automatically clear a safety-relevant mismatch without a verified recovery condition.
- Contactor drive and feedback signals must be documented separately from CP/PP, meter, load-manager communications and service/test interfaces.

## 6. Contactor selection prerequisites

No product shortlist/rating decision until the engineering input sheet is complete:
1. Nominal supply, earthing arrangement, frequency, phase and intended output envelope.
2. Prospective fault current at the switching/protection boundary and upstream protection.
3. Feeder topology and whether outputs are independently fed or locally distributed from a common trunk.
4. Load current, switching duty and expected lifetime/operating cycles.
5. Required pole/isolation function and applicable standards.
6. Controller candidate's exact command-output rating and interface type.
7. Coil voltage, pickup/holding consumption, inrush, suppression and supply budget.
8. Feedback method, contacts, electrical isolation, signal conditioning and detection path.
9. Thermal/environmental envelope, enclosure, mounting and service access.
10. Manufacturer lifecycle, availability, approved application and controlled document revision.

## 7. Verification plan seed (not executed)

| Test ID | Purpose | Evidence to collect | Status |
|---|---|---|---|
| SW-T01 | OFF command leads to verified open state | Command, feedback, time trace, safe test setup | NOT RUN |
| SW-T02 | ON command requires valid permissives | State/permissive logs, controlled test fixture | NOT RUN |
| SW-T03 | Feedback mismatch detected | Injected safe fault/simulation, log and inhibit evidence | NOT RUN |
| SW-T04 | Control supply loss/reset | State before/during/after, no unintended re-energisation | NOT RUN |
| SW-T05 | Invalid feedback signal | Detection, fault latch/inhibit and recovery evidence | NOT RUN |
| SW-T06 | Local protection trip overrides command | Safe simulation/fixture evidence, state log | NOT RUN |
| SW-T07 | Load-manager request cannot bypass local safety | Interface test and bounded-command trace | NOT RUN |
| SW-T08 | Cell fault containment across shared architecture | Analysis plus test method for later multi-output validation | NOT RUN |

Testing requires an approved safe fixture and qualified review. No mains testing is claimed or authorized by this document.

## 8. Disposition and next milestone

M1.32 establishes requirements and feedback semantics only. All SW-01–SW-15 remain OPEN; tests SW-T01–SW-T08 are NOT RUN. No contactor, relay, coil voltage, pole count, current rating, fault rating, feedback device or suppression circuit selected.

Next: close controlled controller and switching-interface documentation gaps, then prepare a complete auxiliary supply budget (controller, actuator coil, sensors, RCD/RDC-DD interface, meters, RFID, communications, HMI and option modules) with peak, steady-state and inrush data. No schematic/BOM freeze until all prerequisites and safety review are satisfied.

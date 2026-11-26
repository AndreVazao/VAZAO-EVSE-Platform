# VAZÃO EVSE Charger Hardware V1 — Single-Output Prototype Requirements-to-Interface Traceability Matrix (M1.29)

**Status:** ENGINEERING TRACEABILITY / COMPONENT EVIDENCE GATE — NOT A FROZEN DESIGN  
**Date:** 2026-11-26  
**Applies to:** V1 first controlled prototype, one AC Mode 3 Type 2 output, reference envelope up to 22 kW / 400 V three-phase / 32 A  
**Parent:** M1.1 component-selection gate; M1.2 candidate shortlist; M1.28 repeatable Output Cell architecture

## 1. Purpose and release rule

Convert the Output Cell architecture into a traceable interface register for the first single-output V1 prototype. Every interface must be classified as one of:

- **REQ DEFINED:** functional requirement is clear, but no exact part or implementation is approved.
- **CANDIDATE ONLY:** one or more candidates are recorded, but exact evidence/compatibility is incomplete.
- **EVIDENCE GAP:** a candidate or architecture exists, but a critical manufacturer document, rating, interface or test is missing.
- **OPEN:** no defensible implementation has been selected.
- **READY FOR REVIEW:** exact part and controlled evidence are assembled for engineering review; this is not automatic approval.

No row becomes **APPROVED** solely because a product page, marketing description or family-level datasheet exists. A release decision requires the exact order code, hardware revision, controlled manufacturer documentation, electrical/interface compatibility, system calculations and applicable verification evidence.

## 2. Prototype boundary and assumptions

| Parameter | Current baseline | Status / limitation |
|---|---|---|
| Charging mode | AC Mode 3 | Requirement baseline; normative implementation must match applicable standards |
| Vehicle interface | Type 2, socket or tethered cable | Exact variant and MPN OPEN |
| Nominal reference | Up to 22 kW, 400 V AC, three-phase, 32 A | Design envelope only; not a universal installation rating |
| Number of outputs | One | First prototype; Output Cell architecture reusable |
| Feeder | One incoming feeder | Site installation and protective coordination still required |
| Local safety | Independent local EVSE safety/control boundary | Must remain functional without CPMS/cloud |
| Managed communications | Ethernet baseline candidate; Wi-Fi/LTE optional | Exact hardware and cybersecurity lifecycle OPEN |
| User authentication | Optional RFID/NFC | Basic private/offline profile without RFID remains valid |
| Energy billing | Use-case dependent | Exact meter certificate and Portuguese metrology/fiscal applicability not approved |
| Prototype status | Design/evidence preparation | No mains energisation or physical validation claimed |

## 3. Interface traceability matrix

| ID | Interface / function | Required behavior and evidence | Existing candidate / source | Current status | Gate before schematic/BOM freeze |
|---|---|---|---|---|---|
| IF-01 | AC input and isolation | Supply system, earthing arrangement, input terminals, isolation and fault level must be defined | M1.23 feeder design basis; installation data not supplied | OPEN | Record target installation assumptions; calculate fault level and protective coordination |
| IF-02 | Overcurrent protection | Device and settings coordinated with cable, contactor, terminals and prospective short-circuit current | No exact QF1 candidate approved | OPEN | Manufacturer coordination tables and installation calculation |
| IF-03 | Residual-current / DC protection | Exact RCD/RDC-DD/RCM architecture, thresholds, diagnostics and coordination | M1.1 protection gate; Phoenix 2902802 integration evidence incomplete | EVIDENCE GAP | Exact device certificates, EVSE controller interface and standards review |
| IF-04 | Surge protection | Decide requirement/type from supply, earthing and installation risk | No exact SPD candidate | OPEN | Installation risk and manufacturer coordination data |
| IF-05 | PE bonding | Continuous PE path from input to enclosure and vehicle connector; PE never switched by normal contactor | M1.1 and electrical architecture | REQ DEFINED | Mechanical bonding design, conductor/terminal selection and continuity test plan |
| IF-06 | CP/PP and Mode 3 control | Generate/measure CP, detect vehicle states, decode PP/cable capability and handle faults | Phoenix CHARX SEC-1000 (1139034) leading evaluation candidate; EM-CP-PP-ETH 2902802 secondary one-point candidate | CANDIDATE ONLY | Exact manual, firmware, I/O map, CP/PP limits, state/fault behavior, isolation and reference schematic |
| IF-07 | Local safety controller | Own state machine, local current ceiling, contactor permission, watchdog and safe stop | SEC-1000 candidate; 2902802 alternative; exact safety case not closed | CANDIDATE ONLY | Confirm local safety behavior, watchdog, startup, brownout, fault response and supported operating modes |
| IF-08 | Application / CPMS processor | Networking, OCPP/CPMS, local services and update orchestration; never direct contactor authority | Application CPU boundary in M1.28; no exact module selected | REQ DEFINED | Decide whether required in first prototype; select hardware/software and isolation boundary |
| IF-09 | Contactor and power switching | AC-rated switching device, coil drive/suppression, auxiliary feedback and welded-contact response | No exact KM1/KMD1 candidate frozen | OPEN | Load category, pole arrangement, coil data, inrush, electrical life, fault coordination and feedback evidence |
| IF-10 | Metering per output | Attributable delivered energy and/or diagnostic measurements with documented accuracy and interface | Carlo Gavazzi EM340DINAV23XS1PFB candidate; EM24DINAV23XE1PFA Ethernet alternative | CANDIDATE ONLY | Exact order code, certificate scope, wiring, protocol, accuracy, sealing and intended billing suitability |
| IF-11 | Feeder current measurement | Measure the relevant phase currents at the actual feeder boundary for load management | Meter/CT candidates compared in M1.25; no final model/ratio | OPEN | Define measurement point, current range, phase mapping, accuracy, sampling and failure diagnostics |
| IF-12 | Local energy manager / setpoint | Accept a validated local current budget and enforce channel allocation without cloud dependency | Phoenix SEC-3xxx, Bender CC613, Versinetic LinkRay, aCharge TELECONTROL compared in M1.25 | CANDIDATE ONLY | Exact supported product/revision, point count, API/register map, acknowledgement, timeout and fail-safe evidence |
| IF-13 | Auxiliary SELV power | Supply controller, communications, sensors, coils and options with isolation and adequate peak/thermal margin | No exact PS1 selected; Phoenix 2902802 consumption discrepancy remains unresolved | EVIDENCE GAP | Close exact load list, coil inrush, simultaneous option budget, PSU derating and manufacturer discrepancy |
| IF-14 | Controller-to-meter bus | Defined physical layer, isolation, topology, termination, addressing and fault behavior | RS-485 Modbus RTU candidate path; exact bus topology OPEN | CANDIDATE ONLY | Exact wiring diagram, register map, baud/parity, bus loading, EMC and timeout tests |
| IF-15 | Ethernet / LTE / Wi-Fi | Modular connectivity, secure provisioning, update lifecycle and offline behavior | Ethernet baseline; optional Wi-Fi/LTE architecture | REQ DEFINED | Select module/antenna and confirm approvals, security support horizon and offline operation |
| IF-16 | RFID/NFC | Secure identity/authentication; credential is not an authoritative mutable monetary ledger | Optional modular reader; exact model and key management OPEN | OPEN | Select credential technology, secure element/key lifecycle, anti-replay and offline authorization policy |
| IF-17 | HMI / indicators | Clear channel state, fault indication and service status; must not own safety decisions | LED/HMI option in preliminary BOM | REQ DEFINED | Define minimum interface, visibility, fault taxonomy and environmental requirements |
| IF-18 | Temperature / thermal | Monitor defined hot spots and apply limits derived from exact component ratings | Generic sensors in BOM; no locations or thresholds approved | OPEN | Thermal-loss model, component temperature limits, sensor placement and validation |
| IF-19 | Enclosure / glands / mounting | IP/IK, corrosion, thermal, cable bend/service access and mechanical support | M1.21/M1.22 engineering baselines; no final dimensions/material frozen | EVIDENCE GAP | Exact component envelopes, thermal budget, ingress/impact targets and mechanical review |
| IF-20 | Service / TestStation port | Safe, controlled access to diagnostics, firmware identity, state observation and isolated test points | M1.27 acceptance plan; exact connector/interface OPEN | REQ DEFINED | Define isolation, access control, pinout, safe test levels and service procedure |
| IF-21 | Event storage / RTC | Monotonic event sequence, timestamp quality, retention and power-loss recovery | Local storage/RTC logical requirement; no exact implementation | REQ DEFINED | Define clock source, holdover, integrity, storage endurance and export format |
| IF-22 | Firmware / configuration integrity | Version identity, signed update, rollback/recovery and rejection of invalid configuration | Requirement in M1.1/M1.28; no implementation selected | REQ DEFINED | Threat model, boot/update chain, signing, recovery and support policy |
| IF-23 | Internal conductors / terminals | Cross-sections, insulation, temperature, routing, torque and terminal ranges derived from final design | No exact cable or terminal selected | OPEN | Complete current/thermal/voltage-drop/short-circuit calculations and manufacturer terminal data |
| IF-24 | Type 2 socket / tethered cable | Connector variant, current/temperature rating, CP/PP pin map, strain relief and service life | Generic Type 2 in requirements/BOM | OPEN | Exact supplier MPN, certificate, assembly drawing and cable/connector compatibility |

## 4. Candidate interpretation — single-output prototype

### 4.1 EVSE controller candidates

**Phoenix Contact CHARX control modular SEC-1000 (1139034):** leading candidate for evaluation of a dedicated per-point controller. It is not selected. Exact firmware, CP/PP behavior, contactor monitoring, RCM integration, local safety behavior, offline operation, cluster dependencies and supported interface must be confirmed from current controlled manufacturer documents.

**Phoenix Contact CHARX control advanced EM-CP-PP-ETH (2902802):** secondary one-point alternative. The M1.4A review records a manufacturer product-page/manual current-consumption discrepancy (40 mA versus 70 mA at 230 V / 140 mA at 110 V) and incomplete controlled source custody. Do not size PS1 or freeze wiring until the exact manual/revision is archived and Phoenix confirms the applicable value and interfaces in writing. Do not assume this one-point product provides multi-output dynamic load management.

**Bender CC613:** historical multi-point/load-management reference only. Lifecycle and exact supported successor remain unverified; procurement is blocked pending written Bender confirmation.

### 4.2 Meter candidates

**Carlo Gavazzi EM340DINAV23XS1PFB:** candidate for per-output three-phase direct metering with RS-485 Modbus RTU and manufacturer-indicated MID status. Exact certificate, order-code scope, configuration and Portuguese billing applicability remain to be verified.

**Carlo Gavazzi EM24DINAV23XE1PFA:** Ethernet/Modbus TCP alternative requiring the same certificate and application review.

Do not use a feeder meter as a substitute for per-output transaction attribution. Do not treat a manufacturer MID statement as blanket Portuguese billing approval.

### 4.3 Protection, switching and auxiliary supply

No QF1, RCD/RDC-DD/RCM, SPD, KM1, KMD1, PS1, cable, terminal or connector MPN is frozen. Their selection depends on the actual supply/earthing arrangement, fault level, installation conditions, coil/auxiliary loads, protection coordination, thermal design and exact manufacturer limits.

## 5. Interface dependency and release sequence

| Sequence | Interface group | Dependency / exit evidence |
|---:|---|---|
| 1 | Supply, PE, QF1, RCD/DC, SPD | Target installation assumptions, fault-level study and protection coordination |
| 2 | CP/PP, safety controller, KM1/KMD1 | Exact controller and switching documentation; validated safety-state and feedback design |
| 3 | PS1 and auxiliary domains | Verified worst-case load, coil inrush, derating and isolation |
| 4 | EM1 and feeder measurement | Exact meter certificate, wiring/protocol, accuracy and measurement boundary |
| 5 | Energy manager / setpoint | Exact local interface, timeout, acknowledgement and fault behavior |
| 6 | COM/RFID/HMI/storage | Cybersecurity, offline policy, service and transaction requirements |
| 7 | Enclosure, terminals, internal conductors | Exact component envelopes, thermal and electrical calculations |
| 8 | Integrated schematic/BOM | Cross-review of all interface evidence and unresolved risks |

A downstream item cannot be frozen by assuming an upstream dependency. In particular, PSU sizing cannot be closed before the controller and contactor-coil loads are known; contactor selection cannot be closed before the exact power path and protection coordination are defined.

## 6. Evidence register required for each selected part

For every candidate promoted toward selection, retain:

- manufacturer and exact order code;
- hardware/revision and firmware version where applicable;
- controlled datasheet, installation manual and wiring diagram;
- applicable declarations/certificates and their exact scope;
- electrical ratings, isolation and environmental limits;
- protocol/register/API documentation and timeout behavior;
- lifecycle/support confirmation and approved alternatives;
- exact interface pin/terminal mapping;
- calculation/test references and reviewer decision;
- supplier quotation date, currency, VAT/shipping and quantity break (commercial BOM only).

If any critical document is missing, mark the row EVIDENCE GAP and keep procurement/wiring blocked.

## 7. Open engineering inputs

The following information is still required before a defensible single-output schematic can be frozen:

1. Target installation supply system, earthing arrangement and prospective fault current.
2. Whether the first prototype is private/unbilled, commercial-billed or intended for public access.
3. Exact Type 2 socket versus tethered cable choice.
4. Exact EVSE controller order code and current manufacturer documentation.
5. Required residual-current/DC detection architecture and exact protective device.
6. Contactor coil voltage, switching duty, feedback and suppression requirements.
7. Complete auxiliary load budget including inrush and optional modules.
8. Exact metering certificate and billing/transaction model.
9. Required feeder measurement and whether M1 prototype includes local dynamic load management.
10. Enclosure thermal/environmental and service-access envelope.

No numerical cable size, breaker rating, RCD type, coil voltage, PSU wattage, CP threshold or timing value is inferred in M1.29.

## 8. Disposition and next milestone

M1.29 is a traceability baseline. It identifies which interfaces are defined, which have candidates and which remain blocked by evidence. It does not select components or release a schematic/BOM.

Next: close the highest-risk evidence gaps for the single-output prototype in dependency order, starting with exact EVSE controller documentation, protection architecture and the Phoenix source/consumption discrepancy. Only after those are resolved should the component-level schematic and terminal schedule be advanced.

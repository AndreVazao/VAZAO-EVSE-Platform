# TS-V1-M0-01 — Product Definition & System Requirements

**Project:** VAZAO EVSE Platform  
**Product:** VAZAO EVSE TestStation  
**Revision:** 0.1  
**Status:** Engineering Baseline / Draft for Review  
**Date:** 2026-08-11

---

## 1. Purpose

The VAZAO EVSE TestStation is a professional automated test and diagnostic platform for electric vehicle supply equipment (EVSE).

The first objective is to accelerate the development and validation of VAZAO AC EVSE products. The architecture shall also support future use in field service, repair, laboratory validation and automated production testing.

The product must evolve from an internal engineering tool into a commercial platform without requiring a fundamental redesign of the core architecture.

---

## 2. Product Family

### 2.1 TestStation Mini

Target use:

- installation;
- commissioning;
- field service;
- maintenance;
- rapid functional verification.

The Mini shall prioritize portability, simplicity and fast test execution.

### 2.2 TestStation PRO

Target use:

- R&D;
- engineering;
- firmware development;
- hardware validation;
- failure analysis;
- long-duration testing;
- calibration and laboratory work.

The PRO shall provide the complete first-generation AC instrumentation and diagnostic capability.

### 2.3 TestStation Factory

Target use:

- production lines;
- end-of-line testing;
- automated QA;
- traceability;
- batch validation;
- integration with manufacturing systems.

The Factory shall support automation and high repeatability and shall be architecturally compatible with the PRO test definitions.

---

## 3. First Generation Scope

### 3.1 Included

- AC single-phase EVSE;
- AC three-phase EVSE;
- Type 2 interface as the primary physical interface;
- IEC 61851 AC control pilot behaviour;
- PP validation;
- CP validation;
- PWM frequency and duty-cycle validation;
- EV state simulation;
- configurable current demand simulation;
- electrical measurements;
- thermal measurements;
- controlled fault simulation;
- automatic tests;
- manual engineering tests;
- stress and endurance tests;
- event logging;
- diagnostics;
- PDF reporting;
- test history;
- calibration support.

### 3.2 Initial electrical envelope

- maximum current: 32 A per phase;
- maximum nominal power: 22 kW;
- nominal system voltage: compatible with European low-voltage AC systems used by the target EVSE;
- single-phase and three-phase operation.

Exact operating limits, tolerances, transient limits and protective thresholds shall be frozen during the electrical and safety architecture phase.

### 3.3 Future scope

The architecture shall reserve interfaces and processing capacity for:

- CCS DC;
- PLC / HomePlug Green PHY;
- DIN 70121;
- ISO 15118;
- Plug & Charge;
- V2G;
- other regional EVSE interfaces;
- expanded power levels.

These capabilities are not requirements for the first AC MVP.

---

## 4. Primary User Workflow

The normal technician workflow shall be:

1. connect the EVSE to the TestStation;
2. identify or scan the EVSE under test;
3. select the test profile or allow automatic profile selection;
4. press **Start Test**;
5. TestStation performs the required sequence automatically;
6. TestStation records all relevant measurements and events;
7. faults are analysed;
8. a final result is generated;
9. the operator can inspect the detailed diagnosis;
10. a report can be saved/exported/printed.

The default workflow must not require specialist knowledge for routine tests, while the Engineering mode must expose advanced controls to qualified users.

---

## 5. Operating Modes

### 5.1 Quick Test

Fast functional verification intended for installation and service.

### 5.2 Complete Test

Full AC functional and electrical validation according to the applicable TestPack.

### 5.3 Stress Test

Long-duration operation with controlled load, monitoring and configurable limits.

### 5.4 Engineering Mode

Manual control and observation of individual EV states, CP/PP conditions, measurements, switching, loads and controlled fault conditions.

Engineering Mode shall require an explicit safety acknowledgement where appropriate.

---

## 6. Functional Requirements

### FR-001 — EV Simulation

The TestStation shall simulate an EV connected to the EVSE and shall control the relevant IEC 61851 states required by the selected test.

### FR-002 — Current Demand

The TestStation shall provide a controllable electrical load or load-control interface capable of testing the first-generation 32 A/22 kW envelope.

### FR-003 — CP Analysis

The system shall measure and analyse the control pilot signal, including voltage/state and PWM characteristics relevant to the selected test.

### FR-004 — PP Analysis

The system shall provide PP simulation and measurement appropriate to Type 2 AC testing.

### FR-005 — PWM Validation

The system shall validate PWM frequency, duty cycle and applicable limits.

### FR-006 — Voltage Measurement

The system shall measure the relevant AC conductors required by the test configuration.

Target design accuracy: ±0.5 %.

### FR-007 — Current Measurement

The system shall measure current per phase as applicable.

Target design accuracy: ±0.5 %.

### FR-008 — Power Measurement

The system shall calculate or directly measure active power.

Target design accuracy: ±1 %.

### FR-009 — Energy Measurement

The system shall accumulate energy during applicable tests.

Target: Class 1 performance for the intended measurement chain.

### FR-010 — Temperature

The system shall monitor temperatures at critical internal points and/or external interfaces defined during hardware design.

### FR-011 — Fault Injection

The system shall support controlled simulation of defined EV/EVSE conditions and faults. Fault injection shall be hardware-controlled and shall never bypass safety protections.

### FR-012 — Automatic Test Execution

The system shall execute versioned TestPacks without requiring manual intervention except where explicitly defined by the test.

### FR-013 — Manual Test Execution

Engineering users shall be able to execute individual actions and measurements under controlled safety conditions.

### FR-014 — Endurance Testing

The system shall support long-duration tests with continuous monitoring and automatic abort/safety behaviour.

### FR-015 — Event Logging

The system shall record time-stamped measurements, state changes, commands, faults, warnings and safety events.

### FR-016 — Results

Every test shall return a defined result status. At minimum:

- PASS;
- PASS WITH WARNING;
- FAIL;
- ABORTED;
- SAFETY TRIP;
- NOT TESTED.

### FR-017 — Diagnostics

For failures, the system shall provide an evidence-based diagnosis where sufficient information exists.

### FR-018 — Reporting

The system shall generate a detailed test report suitable for service, engineering and QA records.

### FR-019 — History

The system shall retain test history and permit retrieval by EVSE identity, serial number, date, result and other indexed attributes.

### FR-020 — Traceability

Test results shall be associated with EVSE hardware revision, firmware version, TestStation identity and TestPack version where available.

---

## 7. Safety Requirements

### SR-001 — Independent Safety Path

The safety function shall not depend exclusively on the main computer, GUI or application software.

### SR-002 — Emergency Stop

An emergency stop shall remove hazardous energy through the defined safety chain.

### SR-003 — Fail-Safe Default

Loss of control power, loss of communications, watchdog timeout or defined critical fault shall drive the relevant power path to a safe state.

### SR-004 — Contactor Control

Power contactors shall be controlled and monitored according to the final safety architecture.

### SR-005 — Interlock

Access or connection conditions that create hazardous states shall be monitored where applicable.

### SR-006 — Overcurrent

The system shall provide appropriately rated protective devices independently of software current limiting.

### SR-007 — Overvoltage / Undervoltage

The measurement and safety architecture shall detect defined abnormal voltage conditions and initiate the required safe response.

### SR-008 — Thermal Protection

Critical temperatures shall be monitored and excessive temperature shall cause controlled test termination.

### SR-009 — Fault Injection Isolation

Fault injection shall never create an uncontrolled hazardous condition or defeat the primary protection system.

### SR-010 — Safe Software Failure

A crash, freeze, restart or loss of the HMI computer shall not leave the power output in an unsafe state.

---

## 8. System Architecture Requirements

The architecture shall be modular.

Minimum logical modules:

- **TS-CORE** — main computing and orchestration;
- **TS-SAFE** — independent safety/control supervision;
- **TS-EV** — EV/IEC 61851 simulation;
- **TS-MEASURE** — measurement and acquisition;
- **TS-LOAD** — controlled load;
- **TS-COM** — communication interfaces.

The modules should communicate through a deterministic internal control protocol, with CAN/CAN-FD as the primary field bus candidate.

The final bus architecture is an engineering decision to be frozen after latency, safety and EMC analysis.

---

## 9. Software Requirements

The software shall be modular and shall separate:

- HMI;
- test orchestration;
- hardware abstraction;
- diagnostics;
- data storage;
- reporting;
- configuration;
- calibration;
- communication;
- update management.

Test definitions shall be versioned and data-driven where practical.

The HMI shall not contain the safety logic.

---

## 10. TestPack Requirements

Each TestPack shall contain or reference:

- unique identifier;
- semantic version;
- applicability;
- prerequisites;
- sequence;
- actions;
- measurements;
- expected values;
- tolerances;
- timeout rules;
- abort rules;
- result mapping;
- diagnostic mappings;
- report metadata.

Tests shall be reproducible and versioned.

---

## 11. Diagnostic Requirements

The diagnostic engine shall support a layered approach:

```text
Measurement
    ↓
Event / State Analysis
    ↓
Rule Evaluation
    ↓
Fault Classification
    ↓
Possible Causes
    ↓
Probability / Confidence
    ↓
Recommended Checks
    ↓
Repair Guidance
```

The system shall distinguish between:

- confirmed measurement fault;
- probable cause;
- possible cause;
- insufficient evidence.

The diagnostic engine must not present an uncertain diagnosis as a confirmed component failure.

---

## 12. Data and Traceability Requirements

A test session shall have a unique session identifier.

Minimum session metadata:

- session ID;
- EVSE ID / serial number;
- station ID;
- operator;
- timestamp;
- test mode;
- TestPack and version;
- hardware revision when known;
- firmware version when known;
- overall result.

Measurement streams and events shall be time-correlated.

---

## 13. Calibration Requirements

The measurement chain shall support controlled calibration procedures.

The architecture shall allow recording of:

- calibration date;
- calibration operator;
- calibration reference/instrument;
- calibration coefficients;
- calibration revision;
- verification result;
- next recommended calibration date.

Calibration data shall be protected from accidental modification.

---

## 14. Maintainability Requirements

Modules shall be replaceable without redesigning the complete machine.

Hardware and firmware revisions shall be identifiable.

Connectors and internal harnesses shall be documented.

The system shall support diagnostic self-tests at startup and before a test session where appropriate.

---

## 15. Self-Test Requirements

Before starting a potentially hazardous test, the TestStation should verify as applicable:

- safety chain healthy;
- emergency stop released;
- contactor state consistent;
- measurement channels available;
- communication links healthy;
- temperature within limits;
- load subsystem healthy;
- required calibration valid;
- configuration valid.

If a critical prerequisite fails, the test shall not start.

---

## 16. Mechanical Requirements

Target first-generation enclosure:

- trolley form factor;
- approximately 720 × 480 × 300 mm;
- wheels;
- telescopic handle;
- side handles;
- touch display;
- serviceable internal modules.

These dimensions are provisional and shall not be considered frozen until thermal, electrical-clearance, connector, EMC and serviceability studies are complete.

---

## 17. External Interfaces

Planned interfaces include:

- EVSE power connection;
- Type 2 interface;
- Ethernet;
- USB;
- CAN/CAN-FD;
- optional Wi-Fi;
- service/debug interfaces.

Future CCS/PLC interfaces shall be architecturally reserved but are outside V1.

---

## 18. Non-Functional Requirements

### NFR-001 — Reliability

The TestStation shall be designed for repeated professional use and predictable failure behaviour.

### NFR-002 — Repeatability

Identical test configurations shall produce comparable results within the defined measurement uncertainty.

### NFR-003 — Observability

All relevant internal states, errors and safety events shall be diagnosable by authorised engineering users.

### NFR-004 — Upgradeability

Firmware, software, diagnostic rules and TestPacks shall be independently versionable where practical.

### NFR-005 — Serviceability

Field-replaceable modules shall be identifiable and replaceable with documented procedures.

### NFR-006 — Security

Configuration, firmware, diagnostic data and calibration information shall have appropriate integrity protections before commercial release.

### NFR-007 — Localization

The software architecture shall permit Portuguese and English UI/report localization without redesigning the test engine.

---

## 19. Acceptance Strategy

The system shall not be considered V1 complete merely because the GUI works.

Acceptance shall require verification of:

1. electrical measurement accuracy;
2. IEC 61851 behaviour;
3. EV simulation;
4. load control;
5. safety response;
6. fault injection;
7. test repeatability;
8. event logging;
9. diagnostics;
10. report generation;
11. calibration procedure;
12. recovery from software and communication failures.

A formal verification matrix shall be created during the next architecture phase.

---

## 20. Engineering Decisions Still Open

The following items must be resolved before hardware freeze:

- exact load architecture: resistive, electronic or hybrid;
- measurement ICs/sensors;
- ADC architecture;
- safety MCU and architecture;
- main MCU(s);
- CAN vs CAN-FD topology;
- isolation strategy;
- contactor topology;
- leakage/fault detection architecture;
- CP/PP analogue front-end;
- enclosure thermal strategy;
- connector and harness architecture;
- calibration references and process;
- final regulatory/certification target set.

These are intentionally not guessed at this stage.

---

## 21. Baseline Status

This document establishes the **functional product baseline**, not the final component-level design.

The next engineering documents shall derive the architecture from these requirements and explicitly trace each hardware/software decision back to one or more requirements.

**Next:** `TS-V1-M1 — System & Electrical Architecture`

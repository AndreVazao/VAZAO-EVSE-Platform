# VAZAO EVSE TestStation V1 — M1.9 EDA/CAD Project Structure & Prototype Implementation Baseline

**Status:** Engineering implementation baseline — not production-approved
**Branch:** feat/charger-hardware-v1
**Related:** M1.2–M1.8
**Next milestone:** M2.0 — Component selection freeze + schematic review + prototype BOM

## 1. Purpose

M1.9 converts the M1.8 document-level schematic architecture into a practical EDA/CAD project structure. It defines the sheet hierarchy, reference designators, connector strategy, signal naming, harness architecture, PCB partition and prototype release structure.

This milestone does not claim that a mains circuit is safe or certified. Exact protective devices, creepage/clearance, conductor sizes, contactors, load stages and PCB dimensions remain subject to calculation, component datasheets, risk assessment and verification.

## 2. EDA project hierarchy

Recommended project root:

```text
VAZAO-EVSE-TestStation/
├── electrical/
│   ├── schematics/
│   │   ├── 00-COVER-INDEX
│   │   ├── 01-SINGLE-LINE-POWER
│   │   ├── 02-INPUT-PROTECTION
│   │   ├── 03-ZONE-A
│   │   ├── 04-EVSE-INTERFACE
│   │   ├── 05-ZONE-B
│   │   ├── 06-LOAD
│   │   ├── 07-SAFETY-ESTOP
│   │   ├── 08-24VDC
│   │   ├── 09-MEASUREMENT
│   │   ├── 10-EV-CP-PP
│   │   └── 11-COMMS-CAN-SERVICE
│   ├── pcb/
│   │   ├── TS-MEASURE
│   │   ├── TS-SAFE
│   │   └── TS-EV
│   ├── harness/
│   │   ├── H-HV
│   │   ├── H-MEASURE
│   │   ├── H-SAFE
│   │   ├── H-EV
│   │   ├── H-COMMS
│   │   └── H-CTRL
│   ├── enclosure/
│   └── calculations/
├── bom/
├── manufacturing/
├── test/
└── docs/
```

## 3. Schematic sheet rules

Every schematic sheet shall have:
- project identifier;
- sheet identifier;
- revision;
- engineering status;
- voltage/domain classification;
- author/reviewer fields;
- safety notes where applicable;
- connector references;
- net labels;
- test points;
- unresolved HOLD items clearly marked.

Sheet names are stable identifiers and should not be renamed casually after PCB/harness work begins.

## 4. Reference designator scheme

| Prefix | Function |
|---|---|
| Q | protective/isolation device |
| F | fuse/branch protection |
| K | contactor/relay |
| PS | power supply/DC-DC |
| U | IC/module |
| T | transformer/current transformer where applicable |
| R | resistor/load element |
| C | capacitor |
| D | diode/TVS/LED |
| J | connector |
| TB | terminal block |
| S | switch/interlock/E-stop |
| H | harness |
| TP | test point |
| FAN | fan |
| TH | thermal sensor |
| SPD | surge protection |

Reference designators must be unique within the complete product assembly.

## 5. Global net naming

### Hazardous power

```text
MAINS_L1
MAINS_L2
MAINS_L3
MAINS_N
PE
ZA_L1
ZA_L2
ZA_L3
ZA_N
ZB_L1
ZB_L2
ZB_L3
ZB_N
LOAD_L1
LOAD_L2
LOAD_L3
LOAD_N
```

### Control

```text
+24V_SAFE
+24V_CTRL
+24V_MEAS
0V_CTRL
0V_MEAS
SAFE_CHAIN
SAFE_STATUS
E_STOP
DOOR_INTERLOCK
LOAD_OVERTEMP
FAN_OK
```

### Contactor control/feedback

```text
KMAIN_EN
KMAIN_FB
KZA_EN
KZA_FB
KZB_EN
KZB_FB
KLOAD_EN
KLOAD_FB
```

### Measurement

```text
VA_L1
VA_L2
VA_L3
IA_L1
IA_L2
IA_L3
VB_L1
VB_L2
VB_L3
IB_L1
IB_L2
IB_L3
ADC_SYNC
MEAS_SYNC
```

### EV interface

```text
CP
PP
PE_EV
CP_FAULT
CP_PWM
PP_CODE
```

### Communications

```text
CAN_H
CAN_L
CAN_SHIELD
SERVICE_TX
SERVICE_RX
SERVICE_GND
```

## 6. Sheet 01 — single-line power

Functional chain:

```text
J1/TB1 → Q0 → QF1 → SPD1(if fitted) → K_MAIN
→ Zone A → TB2 → EVSE
→ TB3 → Zone B → K_LOAD
→ load protection → load stages
```

PE is shown as a separate protective-bonding path.

## 7. Sheet 02 — input protection

Contains:
- Q0;
- QF1;
- SPD1 where applicable;
- upstream/downstream protection interfaces;
- PE/earth-fault architecture;
- surge/protection notes;
- calculation references.

All final protection values remain HOLD until the protection worksheet is approved.

## 8. Sheet 03 — Zone A

Zone A contains the EVSE input power path and measurement interface.

Channels:
- ZA_L1 / VA_L1 / IA_L1;
- ZA_L2 / VA_L2 / IA_L2;
- ZA_L3 / VA_L3 / IA_L3;
- ZA_N;
- PE.

Measurement channels are isolated/protected according to the final sensor architecture.

## 9. Sheet 04 — EVSE interface

Primary power:
- L1;
- L2;
- L3;
- N;
- PE.

Control/service:
- CP;
- PP;
- optional CAN/service;
- selected low-voltage diagnostic signals.

Recommended physical interface concept:

```text
J_EVSE_PWR
  1 L1
  2 L2
  3 L3
  4 N
  5 PE

J_EVSE_SIG
  1 CP
  2 PP
  3 PE/reference where engineered
  4 CAN_H optional
  5 CAN_L optional
  6 SERVICE/diagnostic
```

Final pin assignment must be frozen together with the charger connector design before manufacturing.

## 10. Sheet 05 — Zone B

Zone B contains:
- ZB_L1 / VB_L1 / IB_L1;
- ZB_L2 / VB_L2 / IB_L2;
- ZB_L3 / VB_L3 / IB_L3;
- ZB_N;
- PE.

Zone B is never merged with Zone A in the measurement data model.

## 11. Sheet 06 — load

Logical stages:

```text
LOAD_L1/L2/L3/N
       │
 ┌─────┼─────┐
 K1    K2    K3 ... Kn
 │     │     │
 R1    R2    R3 ... Rn
 │     │     │
 └─────┴─────┘
       │
     RETURN
```

Each stage has an explicit thermal and protection status.

Load stages remain candidate until power, resistance, thermal duty and switching technology are validated.

## 12. Sheet 07 — safety / E-stop

Safety sheet contains:
- E-stop;
- door/service interlock;
- safety relay or safety-rated logic;
- K_MAIN enable;
- K_LOAD enable;
- emergency load disable;
- feedback monitoring;
- reset circuit;
- safe-state indication.

Software cannot bypass the hardwired safety path.

## 13. Sheet 08 — 24 VDC

Distribution:

```text
PS1 24VDC
  │
  ├── F_SAFE → safety chain
  ├── F_MEAS → measurement
  ├── F_CTRL → MCU/CAN
  ├── F_EV → CP/PP
  ├── F_ACT → contactors
  ├── F_FAN → fans
  └── F_AUX → display/service
```

Each branch gets a documented current budget and protection status.

## 14. Sheet 09 — measurement

Recommended PCB partition:

**TS-MEASURE**
- Zone A voltage inputs;
- Zone B voltage inputs;
- six current channels;
- synchronized ADC;
- reference;
- isolated interfaces;
- measurement MCU;
- calibration connector;
- CAN-FD interface.

Measurement PCB shall maintain physical separation between hazardous input interface and low-voltage processing.

## 15. Sheet 10 — EV CP/PP

Functions:
- CP voltage measurement;
- CP PWM generation;
- IEC 61851 state control;
- PP coding;
- controlled fault injection;
- discharge/protection;
- isolation from the main control computer where required.

Fault injection paths must be explicitly labelled and normally disabled.

## 16. Sheet 11 — CAN/service

CAN-FD network nodes:

```text
Main Computer
    │
    ├── TS-MEASURE
    ├── TS-SAFE
    ├── TS-EV
    └── optional TS-LOAD
```

Critical safety action must not depend on CAN availability.

CAN failure is a diagnostic/supervisory fault and, where required by the safety design, causes controlled shutdown.

## 17. PCB partition

### TS-MEASURE
Purpose: synchronized electrical measurement.

Functions:
- six voltage channels;
- six current channels;
- ADC;
- reference;
- measurement MCU;
- isolation;
- calibration;
- CAN-FD.

### TS-SAFE
Purpose: safety supervision.

Functions:
- safety inputs;
- watchdog;
- E-stop state;
- contactor feedback;
- independent safety outputs;
- safe-state indication.

### TS-EV
Purpose: CP/PP and EV communication.

Functions:
- CP;
- PP;
- PWM;
- IEC 61851 state machine;
- fault injection;
- isolated service interface.

## 18. PCB safety boundary

Each PCB must document:
- hazardous boundary;
- SELV boundary;
- isolation barrier;
- creepage/clearance requirements;
- connector keep-outs;
- test-point classification;
- mounting/PE requirements.

Do not place ordinary service/test connectors inside a hazardous boundary merely for convenience.

## 19. Harness architecture

### H-HV
Carries mains/load power. Physically segregated, appropriately rated and protected.

### H-MEASURE
Carries sensor outputs and isolated measurement connections.

### H-SAFE
Carries E-stop, interlock, feedback and safety-control signals.

### H-EV
Carries CP, PP and EVSE interface signals.

### H-COMMS
Carries CAN-FD/service communications.

### H-CTRL
Carries 24 VDC auxiliary/control distribution.

Harnesses shall have unique IDs and revision-controlled pinout drawings.

## 20. Harness identification

Format:

`H-[DOMAIN]-[NUMBER]-REV[XX]`

Examples:

```text
H-HV-001-REV01
H-MEASURE-001-REV01
H-SAFE-001-REV01
H-EV-001-REV01
H-COMMS-001-REV01
H-CTRL-001-REV01
```

## 21. Connector policy

Power connectors shall be mechanically distinct from service connectors.

Connector selection shall consider:
- voltage/current rating;
- touch protection;
- keying;
- locking;
- mating cycles;
- vibration;
- temperature;
- creepage/clearance;
- field serviceability.

Exact connector part numbers remain HOLD until the enclosure and harness geometry are frozen.

## 22. Test-point policy

Every critical subsystem shall expose a documented verification point.

Minimum:
- TP-24V;
- TP-SAFE;
- TP-KMAIN-FB;
- TP-KLOAD-FB;
- TP-CAN;
- calibration reference points;
- Zone A measurement verification;
- Zone B measurement verification.

Hazardous measurement points are restricted maintenance points and require appropriate barriers/procedure.

## 23. Prototype enclosure architecture

Functional physical zoning:

```text
+------------------------------------------------+
| USER / DISPLAY / CONTROLS                      |
|                                                |
| CONTROL / COMPUTE       MEASUREMENT           |
|                                                |
| SAFETY / CONTACTORS     EV INTERFACE           |
|                                                |
|----------------------------------------------- |
| HAZARDOUS POWER / LOAD / THERMAL              |
|                                                |
| AIR IN → LOAD/HEAT → FAN/EXHAUST              |
+------------------------------------------------+
```

High-energy load and heat-producing components should be physically separated from the main computer and precision measurement electronics.

## 24. BOM structure

Recommended BOM columns:

| Field | Purpose |
|---|---|
| RefDes | unique reference |
| Description | functional description |
| Manufacturer | manufacturer |
| MPN | exact part number |
| Supplier | approved source |
| Qty | assembly quantity |
| Revision | component revision |
| Status | Candidate/Validated/Approved/Hold |
| Safety class | safety relevance |
| Domain | HV/SELV/measurement/etc. |
| Datasheet | controlled reference |
| Alternative | qualified alternative |

## 25. Prototype release structure

Release package shall contain:

```text
R0.1 Prototype Engineering
├── Schematics
├── PCB
├── BOM
├── Harness
├── Enclosure
├── Calculations
├── Test Plan
├── Safety Review
└── Change Log
```

No manufacturing release shall be marked production-ready until the HOLD items are closed.

## 26. Initial prototype test sequence

### Stage A — unpowered
- visual inspection;
- PE continuity;
- connector verification;
- insulation/isolation checks as applicable;
- wiring continuity;
- polarity;
- short-circuit checks;
- safety-chain continuity.

### Stage B — control power only
- 24 VDC output;
- branch currents;
- E-stop;
- interlock;
- watchdog;
- contactor command/feedback without hazardous power;
- CAN;
- measurement electronics;
- CP/PP.

### Stage C — externally protected low-energy power
- verify voltage sensing;
- verify phase sequence;
- verify current sensing;
- verify contactor feedback;
- verify emergency shutdown;
- verify Zone A/Zone B data.

### Stage D — controlled load
- low-power load;
- staged current;
- thermal monitoring;
- fault injection;
- shutdown behaviour.

### Stage E — rated envelope
Only after previous stages pass and the required engineering approvals are complete.

## 27. Measurement validation matrix

| Test | Reference | Acceptance concept |
|---|---|---|
| Voltage gain | independent reference | within calibrated uncertainty |
| Current gain | independent reference | within calibrated uncertainty |
| Frequency | independent reference | within specified error |
| Phase angle | known phase source/reference | within allocated phase-error budget |
| Power | reference meter | within allocated error |
| Energy | reference meter | within target accuracy |

Acceptance limits are taken from M1.2 error-budget requirements and final applicable requirements.

## 28. Safety validation matrix

| Test | Expected result |
|---|---|
| E-stop | controlled hazardous-power shutdown |
| Door open | inhibit/stop according to risk design |
| Contactor welded simulation | fault detected/inhibited |
| Load overtemperature | load disabled |
| Fan failure | load reduced/disabled |
| MCU reset | safe state maintained |
| CAN loss | defined supervisory response |
| Measurement failure | affected test inhibited |
| Unexpected current | controlled shutdown |

## 29. Change-control rules

Any change to the following requires revision review:
- protective devices;
- safety circuit;
- contactors;
- measurement sensors;
- ADC/reference;
- connector pinout;
- CP/PP interface;
- load stages;
- harness routing;
- PCB isolation boundary.

Electrical safety changes require re-review of affected calculations and test cases.

## 30. M1.9 acceptance criteria

- [x] EDA project hierarchy defined
- [x] schematic sheet hierarchy defined
- [x] reference designator policy defined
- [x] global net naming defined
- [x] EVSE connector concept defined
- [x] PCB partition defined
- [x] harness families defined
- [x] connector policy defined
- [x] prototype enclosure zoning defined
- [x] BOM structure defined
- [x] prototype test sequence defined
- [x] measurement validation matrix defined
- [x] safety validation matrix defined
- [x] change-control rules defined
- [ ] exact component MPNs frozen
- [ ] exact connector MPNs frozen
- [ ] PCB schematic capture completed
- [ ] PCB layout completed
- [ ] harness drawings completed
- [ ] protection calculations approved
- [ ] safety risk assessment completed

## 31. Next milestone — M2.0

M2.0 will freeze the first prototype component set and perform a coordinated review of:

1. real component MPNs;
2. datasheets and ratings;
3. protection coordination;
4. contactor selection;
5. sensor/ADC selection;
6. CP/PP electronics;
7. connector family;
8. load technology;
9. 24 VDC PSU;
10. PCB isolation;
11. harness interfaces;
12. prototype BOM and purchasing status.

Only after this review should the project move toward manufacturing-oriented PCB and harness release.
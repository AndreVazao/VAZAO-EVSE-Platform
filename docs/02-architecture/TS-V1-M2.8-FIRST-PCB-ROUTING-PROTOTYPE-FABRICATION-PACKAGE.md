# VAZAO EVSE TestStation V1 — M2.8
## First Real PCB Routing Release / Prototype Fabrication Package

**Repository:** AndreVazao/VAZAO-EVSE-Platform  
**Branch:** feat/charger-hardware-v1  
**Status:** engineering prototype routing baseline — NOT a production/certification release  
**Date:** 2026-09-26

---

## 1. Purpose

M2.8 converts the M2.7 CAD implementation contract into the first concrete PCB routing release package.

This milestone freezes routing intent for PCB-A (isolated mains measurement), PCB-B (control/safety/communications), PCB-C (EV interface CP/PP) and PCB-D (DIN/point-to-point industrial wiring).

This document is an engineering release contract and fabrication checklist. It does **not** claim that binary KiCad files, Gerbers or fabricated hardware exist unless those artifacts are separately committed and verified.

No mains energization is authorized by this document.

---

## 2. Board responsibilities

### PCB-A — MEASURE-ISO
- 160 × 100 mm baseline.
- Six Zone-A voltage/current measurement channels.
- Six Zone-B voltage/current measurement channels.
- ADS131M06 measurement chain.
- AMC1311B isolated voltage channels.
- TMCS1123A3AQDVGR current sensing interface.
- Independent isolated supplies for each AMC1311B channel.
- Analog filtering, ADC reference, calibration and test points.
- Explicit isolation barriers.

### PCB-B — CTRL-SAFE
- 120 × 80 mm baseline.
- STM32G474RET6 main MCU.
- STM32G031K8T6 safety supervisor.
- ISO1044BDWR / CAN isolation.
- CAN-FD service interface.
- Contactor control and feedback.
- E-stop status interface and watchdog.
- 24 V / 5 V / 3.3 V distribution.
- Thermal/fan control and diagnostics.

### PCB-C — EV-IF
- 120 × 80 mm baseline.
- Type 2 CP interface.
- PP interface and resistor bank.
- CP PWM generation/measurement.
- CP state switching.
- EV connector service/test points.
- Protected service I/O.

### PCB-D — INDUSTRIAL POWER
Remains point-to-point / DIN-mounted industrial wiring for:
- mains protection;
- PE;
- contactors;
- load switching;
- 24 V PSU;
- terminal blocks;
- emergency isolation;
- high-current wiring.

The 32 A mains assembly is deliberately not forced into PCB form.

---

## 3. Placement baseline

PCB-A physical order:

```
ZONE A MEASURE | ISOLATION | ZONE B MEASURE
VA1 VA2 VA3    |  BARRIER  | VB1 VB2 VB3
IA1 IA2 IA3    |           | IB1 IB2 IB3
ISO-A1..A3     |           | ISO-B1..B3
ADC-01 / REF   |           | ADC-02 / REF
TEST / CAL     |           | TEST / CAL
```

PCB-B:
- power entry / 24 V;
- protected supply;
- safety MCU;
- contactor driver/feedback;
- main MCU;
- CAN isolation/service;
- debug.

PCB-C:
- Type-2/CP/PP connector side;
- CP protection/switch/PWM;
- PP bank/switch/ADC;
- service/test points;
- MCU/service interface.

Exact package-dependent placement must follow verified manufacturer land patterns and isolation envelopes.

---

## 4. Routing rules

Baseline:
- 4-layer FR-4;
- 1.6 mm nominal;
- 1 oz copper baseline;
- ENIG preferred for prototype;
- actual manufacturer stackup replaces nominal values before fabrication.

Suggested layer use:
`L1 = components / signal
L2 = GND / reference
L3 = power / secondary routing
L4 = signal / service`

Measurement routing:
- keep analog inputs short;
- route differential pairs together where applicable;
- avoid switching-node adjacency;
- avoid MCU clock/CAN routing through sensitive analog areas;
- place filtering at the receiving device;
- preserve channel symmetry;
- provide calibration/test access without compromising isolation.

ADC map:
`ADC-01
CH0 = A-L1 V
CH1 = A-L2 V
CH2 = A-L3 V
CH3 = A-L1 I
CH4 = A-L2 I
CH5 = A-L3 I

ADC-02
CH0 = B-L1 V
CH1 = B-L2 V
CH2 = B-L3 V
CH3 = B-L1 I
CH4 = B-L2 I
CH5 = B-L3 I`

Sampling rate remains an engineering parameter to validate during bring-up; no unsupported precision claim is made.

---

## 5. Isolation implementation

PCB-A requires explicit isolation keepouts around every AMC1311B channel.

The M2.7 8 mm prototype target remains a **design target**, not a universal certification value.

Final creepage/clearance depends on:
- working voltage;
- transient/overvoltage category;
- pollution degree;
- material group;
- altitude;
- insulation type;
- device/package ratings;
- applicable standards.

Rules:
- no copper pour crossing an isolation barrier;
- no signal via crossing a barrier;
- no mounting hardware compromising the barrier;
- isolated DC/DC return remains local to its isolated domain;
- each AMC1311B retains its own isolated supply domain;
- test equipment connections must respect the isolation architecture.

---

## 6. Power and return strategy

24 V distribution is partitioned into:
- main 24 V;
- protected safety branch;
- control branch;
- contactor branch;
- fan/thermal branch;
- isolated measurement converter inputs.

MEE1S2405SC remains the prototype candidate for 24 V → 5 V isolated conversion.

Its isolated return must never be merged with another AMC1311B floating return merely to simplify routing.

---

## 7. Footprint and 3D acceptance

Every production-intent footprint must have:
- manufacturer MPN;
- package drawing;
- pin mapping verification;
- verified land pattern;
- courtyard;
- orientation/polarity marker;
- 3D model where available;
- mechanical clearance review.

Special review:
- ADS131M06IPBSR;
- AMC1311BDWVR;
- TMCS1123A3AQDVGR;
- STM32G474RET6;
- STM32G031K8T6;
- ISO1044BDWR;
- MEE1S2405SC;
- terminal blocks;
- Phoenix/DIN components;
- CP/PP connectors.

3D review must cover enclosure clearance, connector access, heatsinks, cable bend radius, PCB-to-PCB clearance and mounting hardware.

---

## 8. ERC release gate

ERC must detect at minimum:
- unconnected pins;
- power input/output conflicts;
- multiple power drivers;
- missing references;
- MCU output-to-output conflicts;
- missing safety feedback;
- missing CP reference;
- missing ADC reference;
- missing isolated supply;
- connector pins without controlled nets.

ERC pass does not prove electrical safety.

Intentional ERC exceptions must be documented rather than globally suppressed.

---

## 9. DRC release gate

DRC must check:
- minimum clearance;
- minimum track width;
- minimum via diameter;
- copper-to-edge clearance;
- courtyard collisions;
- hole-to-copper clearance;
- solder-mask constraints;
- unconnected copper;
- routing constraints;
- custom isolation keepouts.

No global DRC exclusion is acceptable for an unresolved isolation violation.

---

## 10. Thermal and high-current review

PCB routing shall consider:
- driver dissipation;
- regulator dissipation;
- isolated converter dissipation;
- sensor losses;
- connector current capability;
- copper temperature rise;
- enclosure ambient;
- fan airflow.

The 22 kW external resistive load remains an industrial thermal subsystem, not a high-current PCB trace.

---

## 11. Test-point release

Mandatory controlled access for:
- 24 V;
- 5 V isolated domain;
- 3.3 V;
- ADC reference;
- MCU reset;
- CAN-H;
- CAN-L;
- CP;
- PP;
- safety state;
- contactor command;
- contactor feedback;
- measurement calibration points.

Hazardous/isolated test points must be physically identified and protected against accidental contact.

---

## 12. Manufacturing package

Target release tree:
```
CAD/
├── project/
├── schematics/
├── pcb/
├── footprints/
├── symbols/
├── 3d/
├── manufacturing/
│   ├── gerber/
│   ├── drill/
│   ├── fab-drawing/
│   ├── assembly-drawing/
│   ├── bom/
│   └── pick-place/
└── verification/
    ├── ERC/
    ├── DRC/
    ├── isolation/
    ├── mechanical/
    └── release-manifest/
```

Final fabrication package must contain checksums and exact Git commit.

---

## 13. Assembly and prototype build sequence

Assembly drawings shall identify board revision, references, polarity, orientation, connectors, keepouts, isolation boundaries, mounting holes, critical heights and test points.

Prototype sequence:
1. fabricate PCB-A/B/C without mains connection;
2. inspect bare boards and isolation;
3. assemble passive/low-risk parts;
4. inspect soldering;
5. install measurement ICs, isolated converters and MCUs;
6. power only from current-limited bench supplies;
7. verify rails and isolation;
8. program firmware;
9. verify ADC acquisition;
10. verify CP/PP;
11. verify CAN;
12. verify safety logic;
13. verify contactor feedback with power path de-energized;
14. connect industrial power only after separate safety review.

---

## 14. Calibration strategy

Calibration uses an independent reference.

Required datasets:
- zero-current offset;
- voltage gain;
- current gain;
- phase offset;
- channel-to-channel skew;
- energy accumulation;
- temperature drift.

Phase calibration:
```
measured phase
      ↓
reference phase
      ↓
offset correction
      ↓
residual error
      ↓
accept/reject
```

The TestStation must not be its own sole calibration reference.

---

## 15. Zone A / Zone B validation

Zone A = upstream / pre-EVSE measurement.  
Zone B = EVSE-side measurement.

For each phase:
`Δφ = φ_B - φ_A`

The diagnostic engine shall distinguish:
- anomaly already present upstream;
- anomaly introduced after the EVSE boundary;
- measurement-chain disagreement;
- phase-sequence error;
- sensor/channel calibration error.

No arbitrary phase threshold is hard-coded in M2.8. Limits derive from measurement uncertainty, calibration data and applicable engineering requirements.

---

## 16. Capacitor diagnostic guardrail

The diagnostic system may calculate a **candidate correction** for measured reactive power. It must not present it as an automatic repair command.

For a balanced three-phase candidate calculation:
`Q = P · tan(acos(PF))
C ≈ Qc / (3 · ω · Vph²)`

The software must identify:
- assumed topology;
- frequency;
- measured voltage;
- measured PF;
- measured reactive power;
- uncertainty/confidence;
- candidate capacitor value;
- engineering HOLD requiring verification.

---

## 17. Release status

M2.8 is an **engineering routing/prototype baseline**.

It is not:
- a production PCB;
- a certified EVSE;
- a certified measuring instrument;
- a mains-safe product;
- a final EMC design;
- a final thermal design.

The next release requires actual KiCad source files and machine-generated ERC/DRC/manufacturing outputs.

---

## 18. Verification checklist

- [x] M2.7 CAD contract reviewed
- [x] PCB-A/B/C responsibilities frozen
- [x] PCB-D industrial wiring retained
- [x] routing zones defined
- [x] ADC channel map frozen
- [x] isolation strategy frozen
- [x] footprint acceptance criteria defined
- [x] 3D model policy defined
- [x] ERC gate defined
- [x] DRC gate defined
- [x] manufacturing package defined
- [x] assembly requirements defined
- [x] calibration path defined
- [x] Zone A/B diagnostic boundary retained
- [x] capacitor recommendation guardrails retained
- [ ] actual KiCad PCB-A routing generated
- [ ] actual KiCad PCB-B routing generated
- [ ] actual KiCad PCB-C routing generated
- [ ] actual ERC report generated
- [ ] actual DRC report generated
- [ ] actual Gerbers generated
- [ ] actual drill files generated
- [ ] actual assembly outputs generated

The unchecked items require real CAD artifact generation and are deliberately not marked complete.

---

## 19. Next milestone — M2.9

M2.9 is the **real KiCad source/artifact generation and first electrical review** milestone:

1. create actual `.kicad_pro`;
2. create actual `.kicad_sch` hierarchy;
3. create actual PCB-A/B/C `.kicad_pcb`;
4. assign verified footprints;
5. place components;
6. route;
7. run ERC;
8. run DRC;
9. export fabrication files;
10. inspect generated outputs;
11. commit the complete CAD package.

M2.9 is complete only when those files exist and can be fetched from GitHub.

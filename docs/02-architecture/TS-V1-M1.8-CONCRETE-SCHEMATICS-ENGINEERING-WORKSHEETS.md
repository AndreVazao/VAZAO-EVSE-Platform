# VAZAO EVSE TestStation V1 — M1.8 Concrete Electrical Schematics & Engineering Worksheets

**Status:** Engineering baseline — schematic-ready, not production-approved
**Branch:** feat/charger-hardware-v1
**Related:** M1.2–M1.7
**Next milestone:** M1.9 — EDA/CAD implementation + component-level validation

## 1. Purpose

M1.8 converts the M1.7 power architecture into a concrete schematic baseline suitable for transfer into an electrical CAD/EDA project.

Defines: single-line power topology; safety/E-stop circuit; 24 VDC distribution; Zone A / Zone B measurement channels; contactor coil and feedback architecture; programmable-load switching; terminal plan; protection/coordination worksheet; conductor-sizing worksheet; power/thermal budget; candidate/approved component status.

This is an engineering baseline, not a mains commissioning drawing. Protective-device ratings and conductor sections remain HOLD until installation-specific calculations are complete.

## 2. Design envelope

| Parameter | Baseline |
|---|---:|
| Supply | 3P + N + PE |
| Nominal voltage | 400/230 VAC |
| Frequency | 50 Hz |
| Maximum EVSE test current | 32 A/phase |
| Maximum EVSE test power | 22 kW |
| Control voltage | 24 VDC |
| Measurement | Zone A + Zone B |
| Phase-angle diagnostic | L1-L2 / L2-L3 / L3-L1 |
| Load | staged programmable AC load |
| Safety | hardwired safety chain + monitored logic |
| Communications | CAN-FD + service |

## 3. Single-line electrical topology

```text
3P+N+PE 400/230 VAC
        │
   [TB1 INCOMING]
        │
 [Q0 MAIN ISOLATOR]
        │
 [QF1 INPUT PROTECTION]
        │
 [SPD1 if fitted]
        │
     [K_MAIN]
        │
      ZONE A
        │
 [TB2 EVSE INPUT]
        │
   EVSE UNDER TEST
        │
 [TB3 EVSE OUTPUT]
        │
      ZONE B
        │
     [K_LOAD]
        │
 [LOAD PROTECTION/STAGES]
        │
 PROGRAMMABLE LOAD
```

PE runs continuously to all required protective-bonding points. N switching/isolation is subject to final installation and equipment requirements.

## 4. Electrical domains

1. POWER-HV — hazardous mains/load power.
2. MEASURE-ISO — isolated voltage/current measurement.
3. SELV-CTRL — 24 VDC control and safety.
4. EV-INTERFACE — CP/PP and EVSE service interface.
5. COMMS — CAN-FD/service communications.

No direct galvanic connection between POWER-HV and SELV/COMMS is permitted unless specifically engineered and isolated.

## 5. Terminal plan

| Terminal | Function | Domain | Notes |
|---|---|---|---|
| TB1 | L1/L2/L3/N/PE incoming | POWER-HV | protected enclosure |
| TB2 | EVSE input L1/L2/L3/N/PE | POWER-HV | Zone A |
| TB3 | EVSE output/load path | POWER-HV | Zone B |
| TB4 | Programmable-load connection | POWER-HV | staged |
| TB5 | 24 VDC distribution | SELV-CTRL | fused branches |
| TB6 | E-STOP/interlock | SELV/SAFETY | safety chain |
| TB7 | CP/PP | EV-INTERFACE | isolated/protected |
| TB8 | CAN-FD | COMMS | final shield/reference TBD |
| TB9 | service/diagnostics | SELV/COMMS | keyed |

Terminal numbering should remain stable across Mini/PRO/Factory variants where practical.

## 6. Main isolation and input protection

Q0 is the physical hazardous-power isolation point. It shall be mechanically operated, accessible without software, clearly marked, lockable where required, and rated for the final voltage/current and prospective fault level.

QF1 is a design variable. Required inputs are: Ib, In, Iz, prospective short-circuit current, interrupt rating, ambient/grouping correction, voltage drop, and coordination/selectivity.

For 22 kW at 400 V:

I = 22000 / (sqrt(3) × 400) = 31.75 A

This is the nominal three-phase current at unity power factor and does not automatically determine breaker rating.

## 7. Residual-current and surge protection

The final RCD/earth-fault architecture depends on EVSE technology, internal EVSE residual-current detection, DC residual-current behaviour, upstream installation, applicable standards and intended TestStation application.

SPD1 remains an architecture point where required. Selection depends on earthing arrangement, nominal voltage, short-circuit level, upstream protection and coordination.

**Hold M1.8-RCD-01:** freeze final residual-current protection only after the VAZAO charger architecture and applicable requirements are reviewed.

## 8. Contactor architecture

Logical contactors:
- K_MAIN — main controlled energisation;
- K_ZONE_A — optional Zone A isolation;
- K_ZONE_B — optional Zone B isolation;
- K_LOAD — load isolation.

Each safety-critical contactor should expose auxiliary feedback. A software command is never treated as proof of physical isolation.

Functional K_MAIN path:

```text
+24V → safety chain → K_MAIN coil → 0V
                         │
                         └→ feedback → safety MCU
```

Coil suppression shall follow the selected contactor/coil technology.

## 9. E-STOP and safety

Baseline:

```text
+24V
 │
[F-SAFE]
 │
[E-STOP NC]
 │
[DOOR NC]
 │
[LOAD SAFETY NC]
 │
[SAFETY RELAY / SAFETY LOGIC]
 ├── K_MAIN enable
 ├── K_LOAD enable
 └── SAFE_STATUS
```

The MCU monitors the safety state but is not the sole safety mechanism. Automatic restart after E-stop is prohibited; reset requires explicit operator action and a new pre-energisation check.

## 10. 24 VDC distribution

```text
[PSU1 24VDC]
      │
 [F0 MAIN 24V]
      │
 ┌────┼───────────┐
 │    │           │
FSAFE FMEASURE   FCONTROL
 │    │           │
safe  ADC/sensors MCU/CAN
chain
 │
K_MAIN / K_LOAD
```

Critical branches should be separately protected so a non-critical fault does not collapse the complete safety system.

### Preliminary 24 VDC budget

| Branch | Budget |
|---|---:|
| Safety chain | 0.25 A |
| K_MAIN/K_ZONE contactors | 1.00 A |
| K_LOAD/staged contactors | 1.50 A |
| Measurement electronics | 0.75 A |
| Safety/measurement MCU | 0.25 A |
| CAN/service | 0.25 A |
| CP/PP electronics | 0.50 A |
| Fans/control auxiliaries | 2.00 A |
| Main computer DC/DC | 2.00 A |
| Engineering margin | 2.50 A |
| **Preliminary total** | **11.00 A** |

Initial target is approximately 24 V / 15 A class, subject to measured startup/inrush and simultaneous-load validation.

## 11. Zone A and Zone B measurement

Each zone contains three voltage channels and three current channels:

```text
Zone A: VA_L1 VA_L2 VA_L3 + IA_L1 IA_L2 IA_L3
Zone B: VB_L1 VB_L2 VB_L3 + IB_L1 IB_L2 IB_L3
```

Voltage channels are isolated/appropriately protected. Current channels use the Hall/CT/shunt architecture selected during component approval.

All channels use a common deterministic time base suitable for phase measurement.

Measurement object:

```text
timestamp
VA_L1..VA_L3, IA_L1..IA_L3
VB_L1..VB_L3, IB_L1..IB_L3
frequency, P, Q, S, PF
phase angles
status and quality flags
```

## 12. Phase-angle measurement

Calculate φ12, φ23 and φ31 independently for Zone A and Zone B.

The algorithm shall account for zero crossing, sampling skew, channel delay, amplitude threshold, waveform distortion, frequency variation and phase wrap-around.

A nominal 120° relationship is a reference expectation for balanced three-phase operation, not a universal pass/fail threshold. Limits must derive from the applicable electrical requirement plus measurement uncertainty.

## 13. Power calculation

For each phase:

P_phase = mean(v(t) × i(t))

Total:

P_total = P1 + P2 + P3

Reactive/apparent power algorithms shall be explicitly defined and calibrated. Do not infer real power from V_RMS × I_RMS alone when phase/displacement matters.

## 14. Programmable load

Baseline staged architecture:

```text
LOAD BUS
  │
 ┌┼─────────────┐
 ││             │
[K1] [K2]      [K3]
 │    │          │
[R1] [R2]       [R3]
 └────┴──────────┘
          │
        RETURN
```

Each stage requires branch protection, thermal monitoring, suitable switching technology, switching-cycle analysis and feedback where required.

The final choice between contactor, SSR, thyristor or hybrid switching depends on stage power, duty cycle, heat and required control resolution.

### Load-stage worksheet

| Stage | Role | Power | Status |
|---|---|---:|---|
| L0 | low-power diagnostic | TBD | candidate |
| L1 | low/medium | TBD | candidate |
| L2 | medium | TBD | candidate |
| L3 | high | TBD | candidate |
| L4 | fine/programmable | TBD | candidate |

## 15. Thermal budget

For a resistive load, P_heat ≈ P_electrical. At 22 kW continuous, approximately 22,000 W of heat must be managed.

The thermal design must calculate resistor temperature, enclosure temperature, airflow, fan performance, pressure drop, hot spots, external surface temperature, duty cycle and cooldown time.

22 kW continuous rating remains HOLD until thermal modelling and prototype validation demonstrate the required duty cycle.

## 16. Protection and conductor worksheets

### Protection

```text
SOURCE → Ik max/min → UPSTREAM PROTECTION → Q0 → QF1 → K_MAIN
→ CONDUCTOR → EVSE → K_LOAD → LOAD PROTECTION → LOAD
```

For every protective device record manufacturer, model, poles, In, characteristic, interrupt rating, voltage, application, upstream/downstream relationship, coordination evidence and approval status.

### Conductors

| Circuit | Ib | Iz | Section | Length | Method | Derating | ΔV | Short-circuit withstand | Status |
|---|---:|---:|---|---:|---|---|---:|---|---|
| Input | 31.8 A | TBD | TBD | TBD | TBD | TBD | TBD | TBD | HOLD |
| Zone A | 32 A | TBD | TBD | TBD | TBD | TBD | TBD | TBD | HOLD |
| Zone B | 32 A | TBD | TBD | TBD | TBD | TBD | TBD | TBD | HOLD |
| Load | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | HOLD |
| PE | — | TBD | TBD | TBD | TBD | TBD | — | TBD | HOLD |
| 24 VDC | ≤15 A target | TBD | TBD | TBD | SELV | TBD | TBD | — | HOLD |

No conductor section is frozen by this table.

## 17. Creepage and clearance

PCB and enclosure design shall separately consider mains-to-SELV, mains-to-comms, phase-to-phase, phase-to-neutral, mains-to-PE, pollution degree, material group, working voltage, transient overvoltage category and altitude where relevant.

Final distances shall be derived from the applicable standard and insulation system.

## 18. EV CP/PP interface

The EV simulation system remains separate from mains measurement. It shall support CP voltage monitoring, PWM generation/measurement, IEC 61851 state simulation, PP coding, controlled fault injection, isolation/protection and safe discharge.

Fault injection shall be explicitly commanded and logged.

## 19. Diagnostic data model

```text
FACT → MEASUREMENT → QUALITY/UNCERTAINTY → ANOMALY
→ POSSIBLE CAUSES → RECOMMENDED CHECKS → ENGINEERING RECOMMENDATION
```

The system must never silently convert a hypothesis into a confirmed component failure.

## 20. Calibration architecture

The TestStation shall not calibrate itself solely against its own measurement chain.

Calibration fixture should provide independent voltage/current references, known phase relationship, frequency reference and traceable reference instrumentation where required.

Calibration records include serial number, channel, date, reference value, measured value, correction, uncertainty, operator/system and calibration status.

## 21. Component status model

Every BOM item shall be marked:
- CANDIDATE — engineering option;
- BENCH-VALIDATED — tested in prototype;
- APPROVED — approved for defined design;
- OBSOLETE/REPLACED — no longer preferred;
- HOLD — missing required calculation/test.

## 22. Engineering hold points

- **HP-M1.8-01 Supply:** define target installation/supply model.
- **HP-M1.8-02 Short circuit:** establish Ik before freezing interrupt ratings.
- **HP-M1.8-03 Conductor:** define method, length, ambient and derating before freezing sections.
- **HP-M1.8-04 RCD/earth fault:** review charger residual-current behaviour and applicable requirements.
- **HP-M1.8-05 Contactor:** validate switching duty, inrush, endurance and thermal conditions.
- **HP-M1.8-06 Load:** validate resistor/stage values with thermal simulation and prototype test.
- **HP-M1.8-07 Measurement:** validate ADC/sensor phase and gain errors.
- **HP-M1.8-08 Safety:** complete risk assessment and safety validation.

## 23. M1.8 acceptance criteria

- [x] single-line topology defined
- [x] terminal plan defined
- [x] Q0 architecture defined
- [x] QF1 calculation worksheet defined
- [x] K_MAIN circuit defined
- [x] contactor feedback defined
- [x] E-stop architecture defined
- [x] 24 VDC distribution defined
- [x] Zone A schematic defined
- [x] Zone B schematic defined
- [x] phase measurement path defined
- [x] load switching architecture defined
- [x] thermal budget structure defined
- [x] protection worksheet defined
- [x] conductor worksheet defined
- [x] calibration architecture defined
- [x] component status model defined
- [x] engineering hold points defined
- [ ] EDA schematic capture completed
- [ ] exact protective devices calculated/approved
- [ ] exact conductor sections calculated/approved
- [ ] exact contactors validated
- [ ] load stage values validated
- [ ] thermal prototype validated
- [ ] safety validation completed

## 24. Next milestone — M1.9

M1.9 moves from document-level schematics to implementation:

1. electrical CAD/EDA project structure;
2. component symbols and footprints;
3. detailed schematic sheets;
4. harness drawings;
5. connector pinouts;
6. PCB partition;
7. BOM with manufacturer part numbers;
8. preliminary enclosure layout;
9. thermal/mechanical integration;
10. Design Rule Check;
11. safety-domain review;
12. prototype test plan.

The first physical prototype shall use controlled laboratory conditions and appropriately rated external protection. It shall not rely on the TestStation's own unvalidated protection architecture as the sole safety barrier.

## Engineering note

M1.8 is the bridge between architecture and implementation. Numerical values that depend on installation, final charger architecture, protection coordination, thermal design or applicable standards remain HOLD rather than being invented as universal values.
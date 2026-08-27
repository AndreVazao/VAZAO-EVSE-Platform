# TS-V1-M1.3 — Real Component Baseline

**Project:** VAZAO EVSE Platform  
**Product:** VAZAO EVSE TestStation V1  
**Revision:** 0.1  
**Status:** Preliminary Engineering BOM — NOT production approved  
**Date:** 2026-08-27

## 1. Purpose

This document converts the M1 architecture into a practical first hardware baseline. It is deliberately a preliminary component architecture: final ratings, creepage/clearance, thermal design, protection coordination and certification evidence must be verified before fabrication or mains energisation.

## 2. Design Envelope

V1 target:

- 1-phase AC;
- 3-phase AC;
- 230/400 VAC class systems;
- up to 32 A per phase;
- up to 22 kW;
- 50 Hz nominal;
- IEC 61851 AC EV simulation;
- phase-angle diagnostic;
- Pre-EVSE and post-EVSE comparison.

## 3. Proposed Electronics Partition

```text
┌─────────────────────────────────────────────────────┐
│ TS-CORE                                             │
│ Industrial Mini-PC / Raspberry Pi-class computer    │
├─────────────────────────────────────────────────────┤
│ TS-SAFE                                             │
│ Independent MCU + watchdog + safety I/O             │
├─────────────────────────────────────────────────────┤
│ TS-MEASURE                                          │
│ Synchronized ADC / metrology + isolated AFE        │
├─────────────────────────────────────────────────────┤
│ TS-EV                                               │
│ CP / PP / IEC 61851 simulator                       │
├─────────────────────────────────────────────────────┤
│ TS-LOAD                                              │
│ Controlled 3-phase load + thermal management        │
├─────────────────────────────────────────────────────┤
│ POWER / SAFETY                                      │
│ protection + contactors + PE + emergency isolation  │
└─────────────────────────────────────────────────────┘
```

## 4. TS-CORE

Initial recommendation:

- industrial Mini-PC preferred for PRO/Factory;
- Raspberry Pi-class computer remains viable for Mini/prototype;
- Linux-based application stack;
- Ethernet;
- USB;
- CAN-FD through isolated interface;
- local touchscreen.

The computer is supervisory only. It is not the safety isolation element.

## 5. TS-SAFE MCU

Candidate families shall prioritize long-term industrial availability, watchdog capability, deterministic I/O and safety-oriented development support.

A practical first prototype may use an STM32-class MCU with an external hardware watchdog and hardwired safety chain. Production architecture shall be reviewed against the applicable functional-safety requirements and certification strategy.

The safety MCU shall control:

- contactor enable;
- emergency-stop state monitoring;
- interlock state;
- watchdog;
- critical thermal trip;
- contactor feedback;
- communication heartbeat.

## 6. Measurement ADC / Metering Architecture

Preferred architecture:

- synchronized multi-channel acquisition;
- precision voltage front ends;
- isolated current sensing;
- stable reference;
- local measurement MCU;
- CAN-FD to TS-CORE.

Candidate component families to evaluate include precision simultaneous-sampling ADCs from established industrial vendors and dedicated energy-metering ICs where their phase data and waveform access satisfy the diagnostic requirement.

**Selection rule:** do not freeze a metering IC until its channel skew, phase error, reference architecture, input range and calibration behaviour have been experimentally or manufacturer-data validated.

## 7. Voltage Measurement

The first prototype shall use isolated voltage transducers or isolated amplifier/AFE architectures designed for the applicable mains category.

Each phase requires:

- input protection;
- precision scaling;
- anti-alias filtering;
- galvanic isolation where required;
- ADC input protection.

The exact divider/transducer values are deferred to the detailed schematic after insulation and transient requirements are calculated.

## 8. Current Measurement

The baseline shall evaluate two preferred candidates:

### Candidate A — Precision Hall Current Sensor

Used where isolation, overload tolerance and straightforward mechanical integration are priorities.

### Candidate B — Current Transformer

Used where AC-only accuracy and phase stability are more favourable.

A controlled engineering comparison shall measure amplitude error and phase error at representative currents and temperatures.

## 9. Safety Switching

The power path shall use appropriately rated AC contactors with auxiliary feedback.

The exact part must be selected against:

- 400 VAC class;
- 32 A continuous per phase;
- switching duty;
- utilization category;
- inrush;
- expected test cycles;
- coil voltage;
- auxiliary contacts;
- temperature.

For the prototype, industrial contactors from established electrical manufacturers are preferred over generic relay modules.

## 10. Protection

The detailed protection design shall include, as applicable:

- main disconnect/isolator;
- branch overcurrent protection;
- surge protection;
- EMI filtering;
- control-circuit protection;
- load protection;
- PE bonding;
- residual-current/fault detection where required;
- emergency isolation.

Protection ratings shall be calculated from the actual prospective fault current and installation conditions. They shall not be guessed from the 32 A operating current alone.

## 11. IEC 61851 CP/PP Module

TS-EV shall be a dedicated low-power interface module.

It shall support:

- CP measurement;
- CP state simulation;
- PWM generation/measurement;
- PP resistor coding;
- controlled state transitions;
- fault injection.

The module shall include protection against accidental application of hazardous voltage to its low-voltage electronics.

## 12. Load Stage

The load is the dominant thermal and mechanical subsystem.

Three architectures remain valid:

1. staged resistive load;
2. electronic load;
3. hybrid load.

For the first physical prototype, a staged/hybrid architecture is recommended for investigation because it allows robust baseline power dissipation while leaving room for controlled dynamic testing.

The final topology must be engineered for 22 kW continuous test duty where required. A 22 kW load produces substantial heat and cannot be treated as a small electronics module.

## 13. Thermal Baseline

The load subsystem shall provide:

- temperature sensors at thermal hotspots;
- forced-air or other engineered cooling;
- airflow monitoring where fans are safety-critical;
- independent overtemperature trip;
- derating capability;
- serviceable filters/fans where used.

The enclosure shall be validated against worst-case ambient and continuous test duration.

## 14. Low-Voltage Power

Preferred baseline:

- 24 VDC industrial PSU for contactors/actuators;
- isolated DC/DC converters for sensitive electronics;
- protected 5 V and 3.3 V rails as required;
- separate low-voltage and mains wiring zones.

The 24 V control supply shall have its own protection and monitoring.

## 15. CAN-FD

CAN-FD shall be the preferred internal fieldbus.

Recommended logical nodes:

```text
CAN-FD
  ├── TS-SAFE
  ├── TS-MEASURE
  ├── TS-EV
  └── TS-LOAD
```

CAN transceivers shall be selected with appropriate EMC robustness and galvanic isolation at boundaries where required by the system architecture.

## 16. Test Points

The PCB and harness design shall include controlled service test points for:

- measurement references;
- ADC inputs;
- CP;
- PP;
- CAN;
- 24 V;
- logic rails;
- contactor feedback;
- safety state.

Hazardous test points shall be enclosed, labelled and accessible only through a controlled service procedure.

## 17. Charger Co-Design Requirements

The VAZAO charger hardware should expose a defined service/diagnostic interface where practical.

Recommended signals for a controlled diagnostic connector include:

- CP;
- PP;
- contactor feedback;
- controller status;
- selected measurement references;
- PE/earth monitoring interface where appropriate;
- service communication.

This must never bypass protective barriers or permit unsafe energisation.

## 18. Pre-EVSE / Internal-EVSE Phase Diagnostic

The TestStation shall have two conceptual measurement zones:

```text
GRID / INSTALLATION
       │
   [ZONE A]
       │
       ▼
   EVSE INPUT
       │
   [EVSE]
       │
   EVSE OUTPUT
       │
   [ZONE B]
       │
      LOAD
```

Zone A determines whether abnormal voltage, phase sequence, phase imbalance or phase displacement already exists before the charger.

Zone B determines whether the charger introduces an abnormal condition.

This enables the diagnostic engine to distinguish installation faults from EVSE faults.

## 19. Phase-Shift Diagnostic Logic

Example:

```text
ZONE A:
L1-L2 = 120.1°
L2-L3 = 119.8°
L3-L1 = 120.1°
        ↓
INSTALLATION OK
        ↓
ZONE B:
L1-L2 = 104.7°
L2-L3 = 135.0°
L3-L1 = 120.3°
        ↓
FAULT INTRODUCED BY EVSE / INTERNAL PATH
```

The actual thresholds shall be defined from measurement uncertainty and applicable electrical requirements, not from an arbitrary single degree limit.

## 20. Diagnostic Repair Guidance

The diagnostic engine may recommend corrective components only when the fault model and measurement evidence support such a recommendation.

For example, where power-factor correction or phase compensation is technically applicable, the report may identify:

- estimated reactive component;
- calculated capacitance range;
- connection phase;
- expected correction;
- verification test.

The report must clearly distinguish **calculated recommendation** from **approved repair instruction**. Capacitor selection and connection shall account for voltage rating, frequency, switching transients, resonance, discharge requirements and applicable standards.

## 21. First Prototype BOM Categories

| Category | Qty | Status |
|---|---:|---|
| Industrial Mini-PC / SBC | 1 | Candidate |
| Touch display | 1 | Candidate |
| Safety MCU board | 1 | Prototype |
| Measurement board | 1 | To design |
| EV simulator board | 1 | To design |
| Load controller | 1 | To design |
| Safety contactors | TBD | To calculate |
| Main protection | TBD | To calculate |
| 24 VDC PSU | 1 | To calculate |
| DC/DC converters | TBD | To calculate |
| Current sensors | 3 | Candidate |
| Voltage channels | 3 | To design |
| Temperature sensors | TBD | To design |
| Emergency stop | 1 | Required |
| Enclosure/trolley | 1 | Mechanical phase |
| Cooling system | TBD | Thermal phase |

This is a design BOM, not a procurement BOM.

## 22. Component Approval Gates

A component may become production-approved only after:

1. electrical rating verification;
2. thermal verification;
3. isolation verification;
4. EMC suitability review;
5. availability/lifecycle review;
6. schematic review;
7. PCB/layout review;
8. prototype test;
9. calibration/measurement validation where applicable;
10. documentation update.

## 23. Safety Warning

The TestStation interfaces directly with potentially lethal mains energy. This architecture is for engineering design and must not be treated as permission to assemble or energize an unverified prototype.

Before physical commissioning, the design requires formal electrical safety review, insulation/PE verification, protective-device coordination, enclosure review and controlled commissioning procedures.

## 24. Next Milestone

**TS-V1-M1.4 — Detailed Measurement Schematic + Safety Schematic + Preliminary BOM**

The next stage will turn this architecture into actual circuit-level design, including component part numbers, ratings, protection values, connector definitions and measurement-channel calculations.

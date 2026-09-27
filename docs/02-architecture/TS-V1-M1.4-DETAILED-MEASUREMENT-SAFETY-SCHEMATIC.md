# TS-V1-M1.4 — Detailed Measurement & Safety Schematic Baseline

**Project:** VAZAO EVSE Platform  
**Product:** VAZAO EVSE TestStation V1  
**Revision:** 0.1  
**Status:** Preliminary circuit-level baseline — NOT for mains commissioning  
**Date:** 2026-08-27

## 1. Scope

This document establishes the circuit-level architecture to be transferred into the electrical schematic/PCB design. It intentionally avoids pretending that unverified component ratings are final.

V1 target: 1/3-phase AC EVSE, 230/400 VAC class, 32 A per phase, 22 kW, IEC 61851 AC testing.

## 2. Electrical Domains

The design shall be divided into explicit domains:

```text
DOMAIN A — MAINS / HAZARDOUS POWER
DOMAIN B — ISOLATED MEASUREMENT FRONT END
DOMAIN C — SELV CONTROL / MCU
DOMAIN D — COMMUNICATIONS
DOMAIN E — LOAD POWER
```

No PCB routing decision shall bridge these domains without a reviewed isolation barrier.

## 3. Three-Phase Voltage Measurement

Conceptual channel, repeated for L1/L2/L3:

```text
Lx
 │
[Input protection]
 │
[Precision scaling / sensing]
 │
[Anti-alias filter]
 │
[Isolation boundary]
 │
[ADC input]
 │
TS-MEASURE MCU
```

The detailed schematic shall include appropriately rated resistors, protection devices and isolation components after the applicable overvoltage category, pollution degree, insulation and transient requirements are established.

The three channels must share a deterministic acquisition clock or a validated simultaneous-sampling mechanism.

## 4. Current Channels

Three independent AC current channels:

```text
L1 ── Current Sensor 1 ── AFE ── ADC
L2 ── Current Sensor 2 ── AFE ── ADC
L3 ── Current Sensor 3 ── AFE ── ADC
```

The selected sensor must be characterised for amplitude and phase error at the operating range and temperature range.

## 5. Measurement Reference

The measurement board shall have a stable voltage reference appropriate to the ADC architecture. Reference health shall be monitored where practical.

A reference fault shall mark measurements invalid and, where required by the safety analysis, inhibit hazardous tests.

## 6. ADC Interface

Preferred digital connection:

```text
Synchronized ADC / Metering IC
        │
        ├── SPI / deterministic bus
        │
        ▼
Measurement MCU
        │
      CAN-FD
        │
        ▼
TS-CORE
```

The firmware shall timestamp measurement frames and identify hardware/calibration revision.

## 7. Measurement Data Object

Every published measurement shall conceptually contain:

```text
channel_id
value
unit
timestamp
valid
range_state
overload_state
calibration_id
hardware_revision
quality_flags
```

This becomes the contract between TS-MEASURE and the diagnostic engine.

## 8. Phase Measurement

The measurement MCU shall retain access to synchronized voltage samples or fundamental-component estimates for:

- L1→L2;
- L2→L3;
- L3→L1.

The algorithm shall report:

- angle;
- frequency;
- sequence;
- waveform quality;
- confidence/validity.

The system shall not report a precise angle when signal quality is insufficient.

## 9. Pre-EVSE / Post-EVSE Measurement

The station shall implement two logical measurement planes:

```text
                  ┌───────────────┐
GRID / INSTALL ──►│   ZONE A      │
                  │ Reference     │
                  └───────┬───────┘
                          │
                       EVSE
                          │
                  ┌───────▼───────┐
                  │   ZONE B      │
                  │ EVSE output   │
                  └───────┬───────┘
                          │
                         LOAD
```

Where the physical topology permits, Zone A is the installation/reference measurement and Zone B is the EVSE-side measurement.

The diagnostic engine compares both planes to localise abnormalities.

## 10. Safety Control Circuit

Conceptual architecture:

```text
24 V CONTROL
    │
    ├──────────────┐
    │              │
 E-STOP         Safety MCU
    │              │
    └──────┬───────┘
           │ safety permission
           ▼
      Contactor Driver
           │
           ▼
     Main Contactors
           │
           ▼
        EVSE OUT
           │
   Auxiliary Feedback
           │
           └────────► Safety MCU
```

The final implementation may use a safety relay, safety-rated contactor driver or a hybrid architecture after risk assessment.

## 11. Emergency Stop

The emergency-stop chain shall not rely exclusively on an application software command.

Opening the E-stop circuit shall remove the permission for hazardous power connection through the safety architecture.

Reset shall require a deliberate operator action and a complete safety revalidation.

## 12. Contactor Feedback

Each safety-controlled power contactor should expose auxiliary feedback where required.

The logic shall detect at minimum:

```text
OFF command + CLOSED feedback = FAULT
ON command + OPEN feedback   = FAULT
Unexpected transition          = FAULT
```

A suspected welded contact shall block restart until inspected and cleared.

## 13. Watchdog / Heartbeat

```text
TS-CORE ── heartbeat ──► TS-SAFE
TS-SAFE ── watchdog ───► own firmware
```

Loss of heartbeat shall cause a defined transition to safe state after the safety analysis timeout.

The watchdog shall be hardware-based.

## 14. Load Safety

TS-LOAD shall provide:

- independent overtemperature trip;
- power-stage protection;
- current monitoring;
- cooling supervision where cooling is safety-critical;
- contactor/enable feedback;
- safe shutdown.

The 22 kW load must be treated as a major thermal subsystem.

## 15. CP Interface

Conceptual path:

```text
EVSE CP
  │
Protection / level adaptation
  │
CP measurement
  │
TS-EV MCU
  │
PWM generator / state control
```

The implementation shall comply with the applicable IEC 61851 test conditions and maintain isolation/protection between CP and SELV electronics as required.

## 16. PP Interface

Conceptual path:

```text
EVSE PP
  │
Protected measurement
  │
Selectable resistor network
  │
TS-EV control
```

The resistor network shall use appropriate tolerances and switching devices so that simulated cable/current coding remains within the applicable test tolerances.

## 17. Fault Injection

TS-EV shall provide controlled simulation of defined EV/CP/PP abnormal states.

Fault injection shall be hardware-bounded and shall not be capable of bypassing the station's safety isolation.

## 18. Internal Communications

Preferred bus:

```text
             CAN-FD
                │
      ┌─────────┼──────────┐
      │         │          │
 TS-SAFE   TS-MEASURE   TS-EV   TS-LOAD
```

CAN shall be used for control/data. It shall not be considered the sole safety mechanism.

## 19. 24 VDC Control Supply

Conceptual architecture:

```text
Protected AC
    │
24 VDC industrial PSU
    │
    ├── Safety / contactors
    ├── TS-LOAD controls
    └── DC/DC
          ├── 5 V
          └── 3.3 V
```

Sensitive measurement electronics should have appropriately isolated/filtered supplies according to the final EMC architecture.

## 20. PE / Earth

Protective earth shall have a dedicated, low-impedance bonding strategy.

PE continuity shall not depend on PCB traces intended for signal return.

The enclosure, exposed conductive parts and relevant power hardware shall be included in the PE design and verification procedure.

## 21. Protection Coordination

The final schematic shall explicitly document:

- main disconnect;
- overcurrent protection;
- surge protection;
- control protection;
- load branch protection;
- conductor sizing;
- terminal ratings;
- prospective fault current assumptions;
- selectivity/coordination where relevant.

Ratings must be calculated from the installation/test configuration.

## 22. Connector Strategy

Separate connector families or mechanical keying shall be used for:

- hazardous power;
- SELV;
- CAN;
- service/debug;
- CP/PP;
- measurement references.

No connector should allow a hazardous power harness to be accidentally inserted into a SELV interface.

## 23. Test Points

Controlled test points shall be provided for:

- L1/L2/L3 measurement diagnostics;
- current sensor outputs;
- ADC reference;
- CP;
- PP;
- CAN-H/CAN-L;
- 24 V;
- 5 V;
- 3.3 V;
- safety state;
- contactor feedback.

Accessible hazardous test points are prohibited on the external service interface.

## 24. PCB Layout Rules

The PCB design shall enforce:

- physical isolation barriers;
- creepage/clearance calculations;
- controlled return paths;
- short analogue sensor paths;
- separation of switching nodes from precision analogue channels;
- defined shield strategy;
- thermal copper where required;
- test-point accessibility without compromising insulation.

## 25. Phase-Error Calibration

The calibration fixture shall apply a known three-phase reference to the measurement system.

The station shall derive per-channel phase correction and verify all three phase relationships.

Calibration acceptance shall be based on the final uncertainty budget and reference-system capability.

## 26. Charger Interface Requirements

The VAZAO EVSE charger design should reserve a controlled service connector carrying only approved diagnostic signals.

Potential signals:

- CP;
- PP;
- contactor feedback;
- controller status;
- selected low-voltage diagnostic signals;
- measurement references;
- service communication.

Any signal connected to hazardous mains shall require a separately engineered isolation interface.

## 27. Repair Guidance Data

The measurement subsystem shall expose enough data for the diagnostic engine to calculate evidence-based repair hypotheses.

For phase-related faults the diagnostic record should include:

```text
Zone A angle L1-L2
Zone A angle L2-L3
Zone A angle L3-L1
Zone B angle L1-L2
Zone B angle L2-L3
Zone B angle L3-L1
Voltage imbalance
Frequency
Waveform quality
Measurement confidence
```

Only after these values are valid should a repair recommendation be generated.

## 28. Capacitor Recommendation Guardrail

The software may calculate a capacitor value when the diagnosed phenomenon is compatible with reactive compensation. It must not automatically command or imply that a capacitor is safe to install.

The report shall state that the recommendation requires engineering verification of:

- voltage rating;
- frequency;
- capacitance tolerance;
- switching method;
- discharge resistor;
- resonance/harmonics;
- current;
- thermal duty;
- applicable installation requirements.

## 29. Preliminary BOM Structure

The BOM shall be split into:

### Safety / Power

- industrial 24 V PSU;
- main disconnect;
- overcurrent devices;
- surge protection;
- EMI filter;
- safety contactors;
- auxiliary contacts;
- emergency stop;
- terminal blocks;
- PE hardware.

### Measurement

- voltage sensing/isolation components;
- precision resistors where applicable;
- current sensors;
- synchronized ADC/metrology IC;
- voltage reference;
- protection/filter components;
- measurement MCU.

### EV Simulation

- CP protection/interface;
- PP resistor network;
- switching devices;
- EV simulator MCU;
- CAN interface.

### Control

- TS-SAFE MCU;
- watchdog;
- isolated CAN transceivers where required;
- DC/DC converters;
- diagnostic indicators.

### Load

- load elements/power stages;
- contactors/semiconductors;
- temperature sensors;
- fans/cooling;
- protection.

## 30. Engineering Hold Points

Before mains power is applied to any prototype:

1. schematic peer review;
2. PCB creepage/clearance review;
3. PE continuity verification;
4. insulation verification;
5. protective-device review;
6. contactor and feedback test;
7. E-stop test;
8. low-voltage-only functional test;
9. measurement calibration;
10. controlled energisation procedure.

## 31. Status

This document is a circuit-level design baseline. It is not a certified schematic and must not be used as a construction/commissioning drawing until the component values, ratings, PCB geometry and applicable standards have been verified.

## 32. Next Milestone

**TS-V1-M1.5 — Component Part-Number Selection, Protection Calculations, Preliminary BOM and PCB Partitioning**

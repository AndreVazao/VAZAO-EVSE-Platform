# TS-V1-M1.1 — Measurement & Safety Architecture

**Project:** VAZAO EVSE Platform  
**Product:** VAZAO EVSE TestStation V1  
**Revision:** 0.1  
**Status:** Engineering Baseline  

## 1. Objective

Define the measurement and independent safety architecture required to build the first AC TestStation prototype for single-phase and three-phase EVSE up to 32 A per phase / 22 kW.

This document deliberately defines engineering requirements and architecture before freezing specific ICs or part numbers.

## 2. Measurement Objectives

The measurement subsystem shall support:

- L1, L2, L3 voltage;
- neutral/reference where applicable;
- L1, L2, L3 current;
- phase-to-phase voltage;
- RMS voltage;
- RMS current;
- active power;
- apparent power;
- reactive power where sufficiently supported;
- power factor;
- energy;
- frequency;
- phase angle;
- phase sequence;
- voltage/current imbalance indicators;
- temperature;
- diagnostic waveform capture where supported.

Target V1 performance from the product definition remains:

- voltage: ±0.5 %;
- current: ±0.5 %;
- power: ±1 %;
- energy: Class 1 target.

These are system-level targets and must be confirmed by uncertainty analysis and calibration.

## 3. Critical Phase Measurement Requirement

L1/L2/L3 voltage acquisition must be simultaneous or have deterministic, calibrated time synchronisation.

Independent asynchronous ADC sampling is not acceptable as the default architecture for precision phase-angle measurement.

At 50 Hz, one electrical cycle is 20 ms. The acquisition system shall control timing error sufficiently that channel timing contributes only a small, quantified portion of the total phase-angle uncertainty.

The design shall explicitly specify:

- sample timing;
- channel skew;
- sampling rate;
- analogue bandwidth;
- anti-alias filtering;
- clock source;
- timestamping;
- phase calibration;
- frequency tracking.

## 4. Recommended Acquisition Structure

```text
                 ┌──────────────────────────┐
L1 ─ Protection ─► Isolated Voltage AFE ────┐
L2 ─ Protection ─► Isolated Voltage AFE ────┼─► Synchronized ADC
L3 ─ Protection ─► Isolated Voltage AFE ────┘
                                           │
I1 ─ Isolated Sensor/AFE ──────────────────┤
I2 ─ Isolated Sensor/AFE ──────────────────┤
I3 ─ Isolated Sensor/AFE ──────────────────┘
                                           │
                                      Measurement MCU
                                           │
                                         CAN-FD
                                           │
                                       TS-CORE
```

The exact ADC/AFE topology remains an engineering selection item.

## 5. Voltage Measurement Chain

Each hazardous voltage input shall have a dedicated protected measurement path.

Conceptual chain:

```text
EVSE / SUPPLY
      │
Input protection
      │
Current limiting / fusing as required
      │
Surge protection
      │
Anti-alias filter
      │
Isolation / isolated sensing topology
      │
ADC / acquisition
```

The measurement front end shall not create a hazardous path from the measured circuit to SELV electronics.

Creepage, clearance, dielectric strength and insulation coordination shall be addressed in the detailed PCB and mechanical design.

## 6. Current Measurement Chain

Each phase shall have an independent current measurement channel.

Candidate technologies remain:

1. Hall-effect transducer;
2. current transformer;
3. isolated shunt/amplifier architecture where appropriate;
4. integrated isolated current sensing solutions.

The selection shall consider:

- AC accuracy;
- phase error;
- bandwidth;
- overload;
- saturation;
- isolation;
- temperature coefficient;
- mechanical integration;
- calibration.

For phase/power calculations, current-channel phase error must be characterized, not assumed to be zero.

## 7. Phase Calculation

The firmware shall calculate phase relationships from synchronized voltage waveforms or an equivalent validated measurement method.

Required outputs:

```text
L1 → L2
L2 → L3
L3 → L1
```

The algorithm shall account for waveform polarity and determine the actual positive/negative sequence.

The system shall distinguish:

- balanced positive sequence;
- reversed sequence;
- missing phase;
- abnormal phase relationship;
- insufficient signal quality;
- measurement channel fault.

A phase-angle result shall include a quality/validity indicator rather than only a numeric angle.

## 8. Frequency

Frequency shall be measured from the voltage waveform using a robust zero-crossing, phase-locked or equivalent validated method.

The measurement system shall avoid false frequency estimates caused by noise or waveform distortion.

## 9. Power Calculation

For each phase:

```text
P = average(v(t) × i(t))
```

The total active power shall be the sum of the phase powers.

Where waveform quality permits, the system should additionally derive apparent power, reactive power and power factor.

The implementation shall not assume sinusoidal waveforms when calculating true power.

## 10. Energy

Energy shall be accumulated from measured active power over time.

The firmware shall use a monotonic timebase and preserve accumulated energy through normal communication interruptions.

Energy data shall include measurement quality and calibration status in the report metadata.

## 11. Calibration Architecture

Calibration shall be treated as a first-class subsystem.

The calibration model should support:

- per-channel gain correction;
- per-channel offset correction;
- phase correction;
- temperature compensation where justified;
- calibration date;
- calibration reference ID;
- operator/service record;
- hardware revision;
- firmware revision.

Calibration constants shall be versioned and protected against accidental modification.

## 12. Measurement Self-Test

On startup and before hazardous testing, the system shall perform available self-checks.

Examples:

- ADC communication;
- reference voltage;
- sensor plausibility;
- channel range;
- temperature sensor health;
- isolation monitor status where available;
- measurement module heartbeat.

Self-test failure shall inhibit tests that depend on the failed measurement path.

## 13. Safety Architecture

Safety shall be independent from the normal application processor.

```text
                 ┌───────────────┐
                 │   TS-CORE     │
                 │ Application   │
                 └───────┬───────┘
                         │ heartbeat / request
                         ▼
                 ┌───────────────┐
                 │   TS-SAFE     │
                 │ Safety logic  │
                 └───────┬───────┘
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
       E-STOP       INTERLOCKS       FAULT INPUTS
        │                │                 │
        └────────────────┼─────────────────┘
                         ▼
                SAFETY CONTACTOR
                         │
                    EVSE POWER
```

TS-CORE may request energisation. TS-SAFE grants or removes permission according to the safety state.

## 14. Safety Inputs

The architecture shall provide provisions for:

- emergency stop;
- enclosure/service interlock where applicable;
- contactor auxiliary feedback;
- overtemperature;
- overcurrent trip;
- overvoltage trip where required;
- residual-current/fault detection interface where implemented;
- power supply health;
- watchdog;
- communication heartbeat;
- load fault;
- measurement fault.

The detailed safety analysis shall define which inputs are hardwired and which may be supervised digitally.

## 15. Emergency Stop

Emergency stop shall force the TestStation into a defined safe state independently of the normal UI.

The emergency-stop architecture shall be designed so that software cannot mask an active emergency condition.

The system shall record the event after the hazardous energy path has been made safe.

## 16. Watchdog Strategy

At least two supervision layers are recommended:

1. hardware watchdog on TS-SAFE;
2. application heartbeat between TS-CORE and TS-SAFE.

The failure of TS-CORE shall not leave the EVSE energized indefinitely.

The timeout and safe-state behaviour shall be defined during safety analysis and validated by fault injection.

## 17. Contactor Feedback

Power contactors shall provide auxiliary feedback where required by the safety design.

The safety controller shall detect inconsistent states such as:

- command OFF + contactor still closed;
- command ON + contactor not closed;
- unexpected contact transition;
- welded contact indication.

A detected welded-contact condition shall inhibit unsafe restart and generate a high-priority fault.

## 18. Safety Power Path

The recommended conceptual path is:

```text
MAINS
  │
Protection
  │
Safety switching / contactor
  │
EVSE OUTPUT
```

The final design shall ensure that opening the safety path removes hazardous energy as required by the risk assessment.

No single application-level software command shall be treated as the safety isolation mechanism.

## 19. Load Safety

TS-LOAD shall have independent protection appropriate to its power level.

Required monitoring includes, as applicable:

- heatsink/element temperature;
- fan status;
- current;
- load contactor state;
- abnormal internal temperature;
- power stage fault.

A load fault shall prevent continued operation when required to avoid damage or unsafe temperature.

## 20. Measurement vs Safety Separation

A critical design rule is:

**Measurement may inform safety; measurement failure must not silently defeat safety.**

For example, a failed voltage ADC shall not cause the system to assume that voltage is absent and energise a hazardous circuit.

Safety-critical thresholds shall have appropriate independent sensing or fail-safe assumptions where required by the risk analysis.

## 21. Communication Failure

If CAN-FD communication between TS-CORE and a safety-controlled module is lost:

- the module shall enter a defined communication-fault state;
- active hazardous test operation shall be terminated according to the safety strategy;
- contactor permission shall be removed where required;
- the fault shall be logged.

CAN-FD is a control/data bus, not the sole safety isolation mechanism.

## 22. Temperature Monitoring

Temperature sensors shall be distributed according to thermal risk.

Minimum candidate locations:

- load thermal zone;
- power electronics where applicable;
- main contactor/power zone where justified;
- enclosure ambient;
- measurement electronics where required.

Temperature thresholds shall have warning, controlled derating and trip states where applicable.

## 23. Isolation and PCB Partitioning

The PCB architecture shall maintain explicit domains:

```text
HAZARDOUS AC DOMAIN
        ║ isolation barrier
        ║
SELV / CONTROL DOMAIN
        │
        ├── MCU
        ├── CAN
        ├── HMI
        └── Ethernet
```

Creepage and clearance shall be calculated from the applicable voltage, pollution degree, material group, overvoltage category and insulation requirements during detailed design.

## 24. Diagnostic Integrity

Every measurement result used by the diagnostic engine shall carry:

- timestamp;
- channel ID;
- hardware revision;
- calibration revision;
- validity state;
- range/overload state;
- sensor health state.

This prevents the diagnostic engine from treating invalid sensor data as genuine EVSE behaviour.

## 25. Test Sequence Safety Gate

Before starting an automated test:

```text
Self-test
   ↓
Safety status
   ↓
E-stop released?
   ↓
Interlocks valid?
   ↓
Measurement valid?
   ↓
Contactor state valid?
   ↓
Load ready?
   ↓
EV simulator ready?
   ↓
START TEST
```

Any failed gate shall block the hazardous test stage and present the reason to the operator.

## 26. Fault Injection

The safety architecture shall support controlled fault-injection tests during development.

Examples:

- disconnect measurement channel;
- stop TS-CORE heartbeat;
- simulate overtemperature;
- simulate contactor feedback mismatch;
- simulate load fault;
- interrupt CAN-FD;
- activate E-stop.

Fault injection shall only be performed in a controlled engineering mode with appropriate physical safeguards.

## 27. Architecture Decisions Still Open

The following require component-level engineering:

- exact simultaneous ADC / metering IC;
- voltage sensing topology;
- current sensors;
- isolation components;
- TS-SAFE MCU;
- TS-CORE MCU where applicable;
- contactor topology and ratings;
- residual-current detection method;
- safety relay architecture if required;
- exact CP/PP switching topology;
- thermal sensor selection;
- calibration reference hardware.

## 28. Exit Criteria for M1.1

M1.1 is complete when:

- measurement block diagram is approved;
- safety block diagram is approved;
- phase synchronisation requirement is quantified;
- measurement error budget exists;
- safety fault list exists;
- safety state machine is defined;
- component selection can begin without changing the architecture.

## 29. Next Milestone

**TS-V1-M1.2 — Measurement Error Budget, ADC/Sensor Selection & Safety Component Selection**

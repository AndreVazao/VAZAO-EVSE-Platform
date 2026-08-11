# TS-V1-M1 — System & Electrical Architecture

**Project:** VAZAO EVSE Platform  
**Product:** VAZAO EVSE TestStation V1  
**Revision:** 0.1  
**Status:** Architecture Baseline  
**Date:** 2026-08-11

## 1. Objective

Define the first implementable system architecture for the VAZAO EVSE TestStation AC platform while preserving modularity for Mini, PRO and Factory variants and future CCS/DC expansion.

This document defines architecture, interfaces and safety boundaries. It does not yet freeze individual component part numbers.

## 2. Architecture Principle

The TestStation is divided into independent functional domains:

```text
                         ┌──────────────────────┐
                         │       HMI / UI       │
                         │      TS-CORE         │
                         └──────────┬───────────┘
                                    │
                              Control API
                                    │
                         ┌──────────▼───────────┐
                         │    TEST ENGINE        │
                         │ Diagnostics / Data    │
                         └──────────┬───────────┘
                                    │
                              CAN-FD / Ethernet
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
       ┌──────▼──────┐      ┌───────▼──────┐      ┌──────▼──────┐
       │   TS-SAFE   │      │ TS-MEASURE   │      │   TS-EV      │
       │ Safety MCU  │      │ ADC / Sensors │      │ CP / PP / EV │
       └──────┬──────┘      └──────────────┘      └──────┬──────┘
              │                                          │
              │                                  EV simulation
              │                                          │
       ┌──────▼──────────────────────────────────────────▼──────┐
       │                    POWER / EVSE PATH                    │
       │  Input → Protection → Safety Contactors → EVSE         │
       │                          ↓                              │
       │                       TS-LOAD                           │
       └─────────────────────────────────────────────────────────┘
```

## 3. Physical Module Set

The first physical prototype should be designed around six logical modules.

### TS-CORE

Main computer and supervisory software. Responsibilities: HMI, test orchestration, diagnostics, database/history, reports, configuration, updates and communications.

### TS-SAFE

Independent safety controller. Responsibilities: emergency-stop monitoring, interlocks, watchdog supervision, contactor permission, critical limits, safe-state control and heartbeat supervision of TS-CORE.

The main computer shall not be the sole authority capable of keeping hazardous power connected.

### TS-MEASURE

Precision acquisition module for L1/L2/L3 voltage, N where applicable, phase-to-phase voltage, current per phase, active power, energy, frequency, phase angle, waveform capture where supported, temperature and measurement self-test.

The three phase-voltage channels shall be synchronised sufficiently for phase-angle measurement.

### TS-EV

EV/IEC 61851 simulation module for CP state generation/measurement, PWM generation/measurement, PP resistor network, configurable EV states, controlled diode/state behaviour and fault simulation.

### TS-LOAD

Controlled load subsystem for EV current demand simulation up to the V1 envelope, thermal monitoring, load protection and safe shutdown.

The final V1 implementation may use a resistive, electronic or hybrid load. This remains open pending efficiency, size, thermal and cost analysis.

### TS-COM

Communication/service domain supporting CAN/CAN-FD, Ethernet, USB, optional Wi-Fi, service/debug and future PLC/CCS expansion. It may be integrated into TS-CORE or separated later.

## 4. AC Power Architecture

Preliminary power chain:

```text
MAINS INPUT
    │
[Input Connector]
    │
[Main Isolator / Protection]
    │
[Surge / EMI Protection]
    │
[Safety Contactor Stage]
    │
[Measurement Reference]
    │
[EVSE Connection]
    │
[EVSE UNDER TEST]
```

The exact measurement reference position and switching topology shall be frozen in the detailed schematic and safety analysis.

## 5. Pre-EVSE Measurement

A safe reference measurement point shall exist before the EVSE. For three-phase V1 this includes L1, L2, L3 and N/reference as applicable.

The measurement chain shall provide RMS voltage, frequency, phase relationship, phase sequence, voltage imbalance and waveform analysis where implemented.

This is the reference for the previously defined Pre-EVSE / EVSE fault-localisation function.

## 6. Measurement Architecture

The phase measurement architecture shall prioritize channel synchronisation over independent low-cost ADC channels.

```text
L1 ── Protection ── Isolation/AFE ──┐
L2 ── Protection ── Isolation/AFE ──┼──> Synchronized acquisition
L3 ── Protection ── Isolation/AFE ──┘

I1 ── Sensor/AFE ── ADC
I2 ── Sensor/AFE ── ADC
I3 ── Sensor/AFE ── ADC

Temperature ───────────────> ADC / digital sensors
```

Voltage and current channels shall be calibrated for gain and phase error. Phase-angle accuracy shall have its own specification and verification procedure.

## 7. Current Measurement

One current channel per phase is required for the V1 three-phase architecture.

Candidate technologies include Hall-effect sensors, isolated current transformers and other galvanically isolated transducers suitable for the accuracy and bandwidth requirements.

Selection shall consider the ±0.5 % target, bandwidth, isolation, thermal drift, saturation, cost and calibration.

## 8. Voltage Measurement

Voltage sensing shall use galvanic isolation or an equivalent safe topology appropriate to the final design, with suitable overvoltage protection, filtering, current limiting, creepage/clearance and isolation barriers where applicable.

A sensor or ADC failure shall not create an unsafe power-control condition.

## 9. Safety Architecture

```text
Emergency Stop
      │
Safety Controller
      │
      ├── Safety Interlocks
      ├── Watchdog
      ├── Temperature Limits
      ├── Contactor Feedback
      └── Critical Fault Inputs
      │
Safety Contactor / Energy Isolation
      │
EVSE POWER
```

TS-CORE may request a test but cannot override an active safety trip. A communication failure shall produce a defined safe-state transition where required by the safety analysis.

## 10. Contactor Strategy

V1 shall use contactor-based power isolation suitable for the intended AC voltage/current and switching duty.

Contactor feedback shall be monitored where required to detect welded or unexpected contacts.

The final topology must address phase switching, neutral switching if required, inrush, contact welding detection, arc suppression, contactor life and fault isolation.

No component selection is frozen at this stage.

## 11. EV Simulation Architecture

The EV simulator shall emulate the electrical conditions necessary for IEC 61851 AC testing.

```text
              CP
EVSE ─────────┤──────── TS-EV
              │
          CP State / PWM

              PP
EVSE ─────────┤──────── TS-EV
              │
        Cable / current coding
```

Exact resistor values, switching topology and diode implementation shall be defined against the selected IEC 61851 test cases and applicable Type 2 requirements.

## 12. Load Architecture

V1 requires operation up to 32 A per phase / 22 kW and controlled current demand with safe disconnection.

Three implementation families remain under evaluation.

### Option A — Resistive Load

Simple, predictable and robust, but produces substantial heat and has limited dynamic behaviour.

### Option B — Electronic Load

Programmable and dynamic, but substantially more complex in power electronics, cooling and cost.

### Option C — Hybrid Load

Combination of staged resistive power and controlled electronic stages. This is a strong candidate for PRO/Factory if cost and thermal analysis support it.

No option is frozen yet.

## 13. Communications

CAN-FD is the primary candidate for deterministic module control.

```text
TS-CORE
   │
 CAN-FD
   ├──── TS-SAFE
   ├──── TS-MEASURE
   ├──── TS-EV
   └──── TS-LOAD
```

Ethernet shall be available for high-level service, diagnostics, software updates and future integration.

Safety-critical shutdown shall not depend on a software CAN message alone.

## 14. Low-Voltage Power

Low-voltage control power shall be separated from the hazardous AC path.

```text
AC MAINS
   │
   ├── Protected AC path → EVSE / LOAD
   │
   └── Protected AC path → 24 VDC PSU
                           │
                     ┌─────┴─────┐
                     │ DC/DC rails│
                     ├── 12 V     │
                     ├── 5 V      │
                     └── 3.3 V    │
```

Exact rails will be derived from selected hardware.

## 15. EMC / Grounding Concept

The architecture shall explicitly address protective earth, functional earth where applicable, shield termination, measurement isolation, common-mode noise, EMI filtering, separation of power and signal wiring, high-current paths and switching noise from the load.

The measurement system must be designed together with the final EMC strategy.

## 16. Internal Physical Layout

The trolley enclosure should use separated zones:

```text
┌─────────────────────────────────────┐
│ HMI / TS-CORE                       │
├─────────────────────────────────────┤
│ TS-MEASURE     │ TS-COM             │
├────────────────┼────────────────────┤
│ TS-SAFE        │ TS-EV              │
├─────────────────────────────────────┤
│ POWER / CONTACTORS / PROTECTION     │
├─────────────────────────────────────┤
│ TS-LOAD / THERMAL MANAGEMENT        │
└─────────────────────────────────────┘
```

High-energy components shall be physically separated from low-voltage electronics and service-access areas according to the safety and EMC design.

## 17. Modular Connector Strategy

Each module shall have documented interfaces and preferably keyed connectors. The design should prevent accidental connection of incompatible signals or hazardous power domains.

Harnesses shall be labelled by module, signal, voltage class, connector, pinout and revision.

## 18. Serviceability

A technician shall be able to identify and replace a module without tracing the complete machine.

The service interface shall expose module health, firmware version, hardware revision, communication status, measurement status, safety status and calibration status.

## 19. Factory Variant

Factory uses the same core architecture and TestPack model. Possible additions include barcode/QR scanner, automatic serial-number capture, PLC/MES interface, fixture interlock, production result API, automatic report upload and station-to-station calibration management.

## 20. Mini Variant

Mini is a reduced implementation of the same architecture rather than a separate software platform. Possible reductions include fewer instrumentation channels, smaller load capability, reduced display and fewer advanced hardware modules. TestPack and diagnostic concepts remain compatible.

## 21. CCS/DC Expansion

V1 shall reserve processing capacity, communication interfaces, physical expansion space, software abstraction points and safety extension points for future CCS/DC.

CCS/DC will be a separate power/protocol architecture when introduced, not an improvised extension of the AC power path.

## 22. Decisions Pending

The next engineering sub-phase shall resolve:

1. measurement IC / ADC architecture;
2. voltage isolation method;
3. current sensor technology;
4. safety MCU;
5. main MCU architecture;
6. CAN-FD physical layer;
7. contactor topology;
8. load technology;
9. CP/PP analogue and switching topology;
10. protective device ratings;
11. thermal architecture;
12. enclosure partitioning;
13. calibration reference architecture.

## 23. Baseline

The architecture is sufficiently defined to begin detailed engineering without prematurely freezing component choices.

**Next milestone:** `TS-V1-M1.1 — Measurement & Safety Architecture`.

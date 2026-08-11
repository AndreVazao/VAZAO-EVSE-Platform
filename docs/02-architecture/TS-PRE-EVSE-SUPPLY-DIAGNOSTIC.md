# TS — Pre-EVSE Supply & Fault Localization

**Project:** VAZAO EVSE TestStation  
**Revision:** 0.1  
**Status:** Engineering Baseline  
**Date:** 2026-08-11

## 1. Purpose

The TestStation shall be capable, when the installation and test procedure permit, of separating faults originating in the electrical installation from faults introduced by the EVSE itself.

The principle is: **measure before the EVSE → measure at/inside the EVSE where accessible → compare → localise the fault.**

## 2. Test Layers

### Layer A — PRE-EVSE SUPPLY TEST

Performed at the supply point before the EVSE, using a safe and appropriate connection method.

Measurements shall include, as applicable:

- L1-N, L2-N and L3-N voltage;
- phase-to-phase voltages;
- frequency;
- L1→L2, L2→L3 and L3→L1 phase angles;
- phase sequence;
- phase presence;
- voltage imbalance;
- abnormal supply conditions.

Future instrumentation may add waveform quality, harmonics and transient analysis.

### Layer B — EVSE INTERNAL TEST

Where the EVSE design, service procedure and safety provisions provide a valid measurement point, the TestStation shall assess the corresponding electrical conditions inside the EVSE.

For VAZAO EVSE, the platform may use the known approved electrical architecture and service points. For third-party EVSE, only measurements that are safely and legitimately accessible shall be used.

### Layer C — POST-EVSE / OUTPUT TEST

Where physically and electrically applicable, the system may compare conditions at the EVSE output/load side. This layer is optional per test configuration and must never require unsafe probing or defeat of the EVSE protection system.

## 3. Phase Analysis

The TestStation shall calculate and record phase relationships for three-phase systems.

Target ideal relationship for a balanced positive-sequence system:

- L1→L2 ≈ 120°;
- L2→L3 ≈ 120°;
- L3→L1 ≈ 120°.

Exact acceptance limits shall be established by measurement uncertainty analysis and applicable test requirements rather than hard-coded solely as 120°.

The system shall identify, where supported by the measurement chain:

- correct phase sequence;
- reversed phase sequence;
- phase loss;
- abnormal phase relationship;
- significant voltage imbalance;
- inconsistent measurement channels.

The voltage channels must be synchronised sufficiently to make phase-angle measurement valid.

## 4. Comparative Fault Localisation

The diagnostic engine shall compare measurements from each layer.

Example:

```text
PRE-EVSE
L1→L2 = 119.9°
L2→L3 = 120.1°
L3→L1 = 120.0°
PASS

EVSE INTERNAL
L1→L2 = 119.8°
L2→L3 = 63.2°
L3→L1 = 177.0°
FAIL
```

The diagnosis should conclude that the abnormality appears after the supply reference point and therefore investigate the EVSE/internal wiring rather than immediately blaming the installation.

Conversely, if the PRE-EVSE test already fails, the system should identify the installation/supply as the primary suspect and avoid falsely attributing the fault to the EVSE.

## 5. Fault Localisation Result

The report shall support a dedicated **FAULT LOCALISATION** section.

Possible classifications:

- SUPPLY / INSTALLATION;
- EVSE;
- LOAD / DOWNSTREAM;
- TESTSTATION / MEASUREMENT;
- MULTIPLE / AMBIGUOUS;
- INSUFFICIENT EVIDENCE.

Where evidence permits, the report may provide a confidence value. Confidence is diagnostic inference, not proof, and shall be labelled accordingly.

## 6. Repair Guidance

The report shall distinguish between:

- measurement finding;
- probable cause;
- recommended inspection;
- approved repair procedure;
- calculated correction;
- prohibited/unsupported intervention.

For VAZAO equipment, approved service information may be linked to the exact hardware revision. For third-party equipment, the TestStation shall not invent internal repair instructions when the required schematic or service information is unavailable.

## 7. Capacitive Correction

Where a circuit legitimately supports power-factor/reactive-power compensation or another approved capacitive correction, the diagnostic system may calculate or recommend a capacitor solution.

The recommendation shall only be generated when the applicable electrical topology and operating conditions are known sufficiently. Calculations may consider voltage, frequency, active/reactive power, power factor, load topology, star/delta configuration, target compensation, capacitor voltage rating, capacitance, tolerance, temperature and duty requirements.

When applicable, the report may provide:

- calculated capacitance;
- recommended component class/type;
- minimum voltage rating;
- intended connection topology;
- wiring diagram or approved reference diagram;
- verification procedure after intervention.

A capacitor shall **not** be recommended merely because measured phase angles differ from 120°. Phase-angle errors can result from phase loss, incorrect wiring, measurement problems, switching devices, waveform distortion, supply problems or other faults for which capacitive correction is inappropriate.

Any physical repair recommendation must respect the approved electrical design, protective devices, applicable standards and qualified-person procedures.

## 8. Technician Workflow

```text
1. Identify installation and EVSE
          ↓
2. PRE-EVSE SUPPLY TEST
          ↓
3. PASS / FAIL supply
          ↓
4. Connect / test EVSE
          ↓
5. EVSE TEST
          ↓
6. Compare measurements
          ↓
7. Fault localisation
          ↓
8. Diagnostic guidance
          ↓
9. Repair / installation correction
          ↓
10. Repeat PRE/EVSE test as applicable
          ↓
11. Final validation report
```

## 9. Applicability

This capability shall work as:

- VAZAO EVSE commissioning aid;
- VAZAO EVSE service/repair tool;
- third-party EVSE diagnostic tool where safe measurement access exists;
- laboratory engineering function;
- production diagnostic function where appropriate.

## 10. Engineering Implications

The measurement subsystem shall support:

- simultaneous or sufficiently synchronised voltage acquisition;
- known phase relationships between channels;
- suitable sampling rate and analogue bandwidth;
- channel isolation appropriate to the measurement topology;
- calibration of amplitude and phase error;
- traceable timing between measurement channels.

Phase-angle accuracy must be treated as a separate measurement specification from simple voltage accuracy.

## 11. Traceability Requirements

This document introduces:

- FR-PHASE-001 — three-phase angle measurement;
- FR-PHASE-002 — phase sequence analysis;
- FR-PHASE-003 — pre-EVSE supply test;
- FR-PHASE-004 — comparative before/inside/after analysis;
- FR-PHASE-005 — fault localisation;
- FR-PHASE-006 — conditional repair guidance;
- FR-PHASE-007 — conditional capacitive-correction calculation.

## 12. Status

**Baseline approved for architecture development.**

Detailed measurement architecture, sensor/ADC selection, isolation and calibration method remain to be designed in TS-V1-M1.

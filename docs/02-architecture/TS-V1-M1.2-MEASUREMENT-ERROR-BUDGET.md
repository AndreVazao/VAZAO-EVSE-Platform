# TS-V1-M1.2 — Measurement Error Budget & Component Selection Strategy

**Project:** VAZAO EVSE Platform  
**Product:** VAZAO EVSE TestStation V1  
**Revision:** 0.1  
**Status:** Engineering Baseline  
**Date:** 2026-08-27

## Objective

Turn the measurement requirements into quantified engineering targets before freezing electronic components.

V1 covers single-phase and three-phase AC EVSE up to 32 A per phase / 22 kW and the Pre-EVSE versus EVSE diagnostic method.

## System Targets

| Quantity | Product target | Engineering objective |
|---|---:|---|
| Voltage | ±0.5 % | Total uncertainty comfortably below target |
| Current | ±0.5 % | Total uncertainty comfortably below target |
| Power | ±1 % | True-power calculation using synchronized v(t), i(t) |
| Energy | Class 1 target | Traceable calibration and controlled accumulation |
| Phase angle | Diagnostic-grade | Quantified channel skew + sensor phase error |
| Frequency | Diagnostic-grade | Robust waveform-derived measurement |

The final uncertainty budget shall include sensor, analogue front end, ADC, reference, temperature, calibration, timing skew and algorithm contributions.

## Phase-Angle Error Budget

At 50 Hz, one electrical cycle is 20 ms and one degree corresponds to approximately 55.56 µs of time.

The acquisition architecture therefore needs deterministic inter-channel timing. A fast ADC with unknown or variable channel skew is not sufficient.

The V1 design shall quantify:

- sample timing;
- channel skew;
- sampling rate;
- analogue bandwidth;
- anti-alias filtering;
- clock source;
- timestamping;
- phase calibration;
- frequency tracking.

Phase error shall be measured during calibration and stored per channel pair.

## Preferred Acquisition Strategy

```text
L1 voltage ─┐
L2 voltage ─┼─> synchronized voltage acquisition
L3 voltage ─┘

I1 current ─┐
I2 current ─┼─> synchronized current acquisition
I3 current ─┘
                 │
                 ▼
          Measurement MCU
                 │
              CAN-FD
                 │
              TS-CORE
```

The selected solution should allow raw or decimated waveform data for engineering diagnostics while keeping normal control traffic compact.

## ADC / Metering IC Selection Criteria

Evaluate:

- simultaneous sampling or deterministic channel timing;
- effective resolution at 50 Hz;
- input architecture;
- reference stability;
- sample rate;
- analogue bandwidth;
- anti-alias requirements;
- protection;
- isolation architecture;
- deterministic digital interface;
- temperature performance;
- calibration support;
- lifecycle/availability;
- software support;
- cost.

A multi-channel energy-metering IC is acceptable only if its phase measurement behaviour and available data satisfy the TestStation diagnostic objectives.

## Voltage Front End

Compare:

- isolated amplifier + precision divider;
- isolated ADC;
- metering front end;
- suitable isolated voltage transducer.

The front end must tolerate foreseeable transients without materially degrading phase accuracy.

## Current Sensor Selection

### Hall Sensor

Advantages: galvanic isolation, AC measurement, overload tolerance.

Risks: offset drift, temperature drift, device-dependent phase error and cost.

### Current Transformer

Advantages: galvanic isolation and potentially excellent AC accuracy/cost ratio.

Risks: no DC measurement, burden/filter dependence and saturation.

### Isolated Shunt

Advantages: strong linearity potential and precision.

Risks: dissipation, thermal drift, isolation complexity and fault-energy considerations.

For AC-only V1, CT and Hall solutions shall be compared quantitatively before selection.

## Measurement Channel

```text
INPUT
  ↓
Protection
  ↓
Scaling / Sensor
  ↓
Anti-alias filtering
  ↓
Isolation as required
  ↓
ADC
  ↓
Calibration correction
  ↓
DSP / algorithms
  ↓
Validated measurement object
```

Every validated measurement shall carry value, unit, timestamp, validity, overload state and calibration revision.

## Power Measurement

True active power should be calculated from synchronized samples:

`P = mean(v(t) × i(t))`

This avoids assuming ideal sinusoidal waveforms and supports diagnostics under distorted loads.

## Phase Algorithm

Candidate methods:

- cross-correlation;
- fundamental-frequency DFT/Goertzel extraction;
- phase-locked estimation;
- calibrated zero-crossing.

The preferred engineering approach is a fundamental-component phase estimator because it is less sensitive than raw zero-crossing to moderate waveform distortion.

Each angle result shall include a signal-quality indicator.

## Calibration Architecture

Calibration shall support:

- voltage gain and offset;
- current gain and offset;
- voltage-channel phase correction;
- current-channel phase correction where applicable;
- frequency validation;
- calibration date;
- reference ID;
- operator/service record;
- hardware revision;
- firmware revision.

Calibration constants shall be versioned and protected against accidental modification.

## Minimum Calibration Sequence

1. zero/offset;
2. low-range voltage;
3. nominal voltage;
4. high-range voltage;
5. low current;
6. nominal current;
7. high current;
8. frequency;
9. phase relationship;
10. active power;
11. energy accumulation.

Exact reference points and tolerances will be defined in the calibration specification.

## Safety Component Selection

Safety architecture shall be selected independently of the measurement MCU.

Compare:

- safety relay architecture;
- safety-rated contactor control;
- independent safety MCU;
- hybrid safety relay + MCU supervision.

The final design must reach a predictable de-energized state after emergency stop, watchdog failure, control-power loss and defined critical faults.

## Contactor Selection

Base selection on:

- system voltage;
- continuous current;
- utilization category;
- switching frequency;
- inrush;
- EVSE test duty cycle;
- expected life;
- auxiliary feedback;
- coil voltage;
- suppression method.

Prefer robust industrial components over marginal low-cost switching devices.

## Residual-Current / Fault Detection

Reserve a dedicated fault-detection path for residual-current or equivalent protective monitoring as required by the safety analysis and applicable test requirements.

Ordinary phase-current measurements shall not be treated as a substitute for a required protective function.

## Safety State Machine

```text
BOOT → SELF_TEST → SAFE_IDLE → ARMING → ENERGIZED → TEST_RUNNING
                                      ↓
                              CONTROLLED_STOP
                                      ↓
                                  SAFE_IDLE

ANY STATE ── critical fault ──> SAFE_TRIP
SAFE_TRIP ── inspection/reset ──> SELF_TEST
```

Emergency stop shall force the safety path safe independently of the application flow.

## Watchdog

TS-SAFE shall have a hardware watchdog. TS-CORE shall additionally use an application heartbeat. Watchdog timeout shall be derived from the complete safety response-time analysis.

## Self-Diagnostics

At startup the station should verify measurement communication, ADC/reference health, sensor plausibility, temperature channels, safety inputs, contactor feedback, emergency stop, load availability, EV simulator status and storage/report capability.

A failed diagnostic shall inhibit affected test classes.

## Charger/TestStation Co-Design Rule

The TestStation measurement architecture shall be checked against VAZAO charger hardware before either design is frozen.

The charger may expose controlled test points and diagnostic information where this improves serviceability without compromising safety or certification. The TestStation shall never require undocumented or unsafe access.

## Exit Criteria

M1.2 is complete when the measurement error budget and phase-error target are quantified, ADC/metrology, voltage sensing, current sensors and safety switching are shortlisted, and the calibration architecture is defined.

## Next Milestone

**TS-V1-M1.3 — Real Component Selection + Measurement Schematic + Safety Schematic**

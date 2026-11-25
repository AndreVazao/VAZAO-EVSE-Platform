# VAZÃO EVSE Charger Hardware V1 — Local Load Management Verification and TestStation Acceptance Plan (M1.27)

**Status:** TEST PLAN / ACCEPTANCE CRITERIA — NOT EXECUTED  
**Date:** 2026-11-25  
**Parent:** M1.24 local load-management contract; M1.25 candidate matrix; M1.26 supplier evidence request  
**Purpose:** define how a selected local load manager and EVSE channel controllers will be proven before their behavior is used to justify feeder sizing.

## 1. Test boundary and safety

This document defines tests, not results. No hardware has been selected or tested by M1.27. Do not connect a mains feeder or vehicle until the test rig, protection, isolation, emergency stop, measurement equipment and procedures have been reviewed and approved by qualified personnel.

Early tests should use simulation, isolated low-voltage interfaces, protocol emulators and controlled current injection. Mains-connected tests require a separately approved laboratory setup.

## 2. TestStation service levels

The VAZÃO EVSE TestStation must support three service levels, with a traceable report at the end of every run:

### Level 1 — Technician quick verification
- Rapid local check of meter communication, phase mapping, controller connectivity and current-limit response.
- Guided pass/fail checks with minimal setup.
- Capture device IDs, firmware/configuration, timestamp, measured values and operator.
- Never override protection or energize a channel merely to make a test pass.

### Level 2 — Service and fault diagnosis
- Isolate failures in phase measurement, CT polarity, bus wiring/termination, stale setpoints, channel acknowledgements, controller resets and degraded-mode behavior.
- Run controlled fault injection and compare observed behavior with the approved M1.24 fallback contract.
- Produce a diagnostic report with raw measurements, event timeline, fault injection and recovery result.

### Level 3 — Factory / development / design validation
- Full multi-channel tests for dual and quad variants, common and independent feeder arrangements, phase imbalance, simultaneous demand, transient response and long-duration stability.
- Verify all acceptance limits against calibrated reference instruments.
- Preserve raw data, test scripts, firmware, configuration, calibration certificates, environmental conditions and reviewer approval.
- This level is the evidence gate before relying on load management to reduce a common feeder design current.

All levels produce a printable, exportable evidence report. A report must distinguish PASS, FAIL, NOT RUN and INCONCLUSIVE; absence of a test is never represented as a pass.

## 3. Test equipment and evidence prerequisites

Before execution, identify and verify:
- exact manager, EVSE controller, meter and CT order codes and hardware revisions;
- firmware, configuration version and checksum;
- calibrated three-phase reference meter/current source;
- phase-current injection or safe simulator for sensor faults;
- protocol simulator/logger for Modbus RTU/TCP or the selected bus;
- controllable channel load simulators or approved EVSE test loads;
- isolated power supplies and approved protective test fixture;
- synchronized timestamps and event logging;
- current/voltage limits and stop conditions approved by the test engineer.

Calibration status and uncertainty must be suitable for each acceptance tolerance. No numeric tolerance is invented in M1.27; it must be derived from selected component specifications and the approved feeder limit.

## 4. Functional test matrix

| ID | Test | Setup / stimulus | Required evidence / expected result |
|---|---|---|---|
| LM-T01 | Phase identity and polarity | Apply known current separately to L1/L2/L3 | Correct phase mapping and sign; wrong mapping detected |
| LM-T02 | Measurement accuracy | Compare manager readings against calibrated reference across operating range | Error within approved measurement budget |
| LM-T03 | Dual simultaneous demand | Both channels request maximum current | Aggregate demand remains within configured feeder budget |
| LM-T04 | Quad simultaneous demand | All four channels request maximum current | Aggregate demand remains within configured feeder budget |
| LM-T05 | Step load response | Increase/decrease one channel demand while others remain active | Stable allocation without exceeding limit or oscillating |
| LM-T06 | Fairness / priority | Competing channels request more than available budget | Deterministic configured policy, auditable allocation |
| LM-T07 | Phase asymmetry | Introduce permitted single-phase load/imbalance | Per-phase limits respected; no scalar-only blind spot |
| LM-T08 | New vehicle admission | Start a new session while existing channels are near limit | New channel admitted only after safe budget allocation |
| LM-T09 | Sensor open circuit | Disconnect one phase sensor under controlled conditions | Fault detected; no further load increase; approved fallback occurs |
| LM-T10 | Sensor short/reversal | Inject safe simulated short/reversed polarity/implausible data | Invalid measurement detected and handled per contract |
| LM-T11 | Meter communication loss | Interrupt meter bus | Defined fallback; no stale measurement treated as valid indefinitely |
| LM-T12 | Channel bus loss | Disconnect one EVSE channel | Channel timeout fallback; remaining budget recalculated only from confirmed state |
| LM-T13 | Manager watchdog/reset | Trigger controlled watchdog or power cycle | Channels do not ramp on stale setpoints; conservative recovery |
| LM-T14 | Stale/duplicate/rejected setpoint | Inject delayed, duplicated and rejected commands | Sequence/acknowledgement handling prevents stale command from raising current |
| LM-T15 | Configuration corruption | Load invalid version/checksum | Configuration rejected; approved safe defaults retained |
| LM-T16 | CPMS/Internet loss | Remove WAN/cloud while local bus remains | Local current control continues independently |
| LM-T17 | Full power restoration | Remove and restore auxiliary/control power | Sensor validation and channel acknowledgements precede ramp-up |
| LM-T18 | Long-duration stability | Run representative variable loads for approved duration | No limit violation, uncontrolled oscillation or unexplained state divergence |
| LM-T19 | Independent feeder mode | Simulate each feeder's own limit and fault | Each output respects its own feeder budget; shared manager does not mask isolation |
| LM-T20 | Common feeder mode | Simulate common trunk plus each protected branch | Trunk and branch budgets independently respected |

## 5. Topology-specific acceptance

### Common incoming feeder
- Verify total current at the common feeder measurement point.
- Verify each branch's individual current and protective state.
- Verify that the aggregate limit remains respected during channel start/stop, communications loss and controller restart.
- Demonstrate that a single branch fault cannot silently cause an unsafe increase in other channels.

### Independent incoming feeders
- Verify each feeder measurement and current limit independently.
- Verify loss/fault on one feeder does not corrupt the limits applied to another.
- If a site-level manager coordinates all feeders, verify each local feeder limit remains independently enforced.

## 6. Acceptance gates

A test campaign can pass only when:
1. All safety-critical tests are PASS; no FAIL or INCONCLUSIVE remains.
2. Measurement uncertainty and response time are inside approved budgets.
3. The maximum permitted feeder current is never exceeded during normal or fault transitions.
4. Local control continues without cloud/CPMS.
5. Every channel enforces a local timeout/fallback independently.
6. Reboot, configuration corruption and communication loss cannot restore a higher unapproved current limit.
7. Raw evidence and printable reports are complete and reproducible.
8. An independent reviewer approves the results and configuration.

If any gate fails, the system cannot be used to justify a reduced common-feeder current. Use the full simultaneous-demand envelope from M1.23 until a corrected system is retested.

## 7. Required report schema

Each TestStation report must include:
- run ID, test level, date/time, operator and reviewer;
- product/serial IDs, hardware revisions, firmware and configuration hashes;
- feeder topology and configured aggregate/per-output limits;
- meter/CT model, phase mapping, calibration details and uncertainty;
- test ID, stimulus, expected result, observed result and PASS/FAIL/NOT RUN/INCONCLUSIVE;
- raw time-series data and event timeline;
- injected faults and recovery actions;
- deviations, evidence links and corrective action references;
- final approval and explicit scope limitations.

## 8. Open parameters

The exact measurement tolerance, maximum response time, setpoint granularity, fallback current, timeout, ramp rate, stability duration and test-load profile must be derived from selected manufacturer data and the final system risk assessment. They remain TBD until exact hardware and supplier documentation are approved.

## 9. Disposition

M1.27 is a test-plan baseline only. No tests are claimed as executed, no hardware is accepted, and no reduced feeder rating is approved. The TestStation must implement all three service levels and generate traceable reports before the load-management function can be considered production-ready.

## 10. Next step

After supplier evidence is received and evaluated, instantiate this plan with exact numeric acceptance limits and selected hardware. Run Level 1 and Level 2 first, then Level 3 factory validation. Only approved Level 3 evidence can support a reduced common-feeder design current.

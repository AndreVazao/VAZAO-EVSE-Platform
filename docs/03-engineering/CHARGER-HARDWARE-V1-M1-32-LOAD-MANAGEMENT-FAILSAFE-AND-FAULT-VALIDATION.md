# VAZÃO EVSE Charger Hardware V1 — M1.32 Load Management Fail-Safe and Fault Validation

**Status:** control/safety requirements and verification plan. No load-manager hardware, firmware, response time, feeder limit or fail-safe mode is approved.

## 1. Purpose and relationship to M1.29–M1.31

M1.32 defines how dynamic load management may constrain a shared feeder without becoming the only safety barrier. It converts the M1.31 capacity dimensions into explicit operating states, fault responses and acceptance evidence.

The physical feeder and protective devices must remain safe for the maximum demand that the installed local control system can actually enforce. A CPMS, cloud service, mobile app or remote operator command is never the sole enforcement mechanism for a reduced feeder rating. Every output retains its own local EVSE control and safety chain.

## 2. Control boundaries

| Layer | Responsibility | Must not be relied upon for |
|---|---|---|
| Site measurement | Measure relevant site/feeder currents per phase and report quality/timestamp | Replacing protective devices or EVSE local safety |
| Local load manager | Calculate available per-phase EV current, allocate limits and enforce aggregate cap | Defeating per-output protections or silently increasing the commissioned cap |
| Output EVSE controller | Enforce valid current limit through the EVSE control pilot and manage local session/safety state | Assuming a shared master is always healthy |
| Power switching/protection | Disconnect or protect against electrical faults according to approved design | Dynamic optimisation or cloud policy |
| CPMS/cloud/app | Authentication, billing, monitoring, remote policy and reporting | Real-time feeder protection or sole load-limit enforcement |

The physical enforcement point and measurement boundary must be drawn on the single-line diagram. A controller command is not proof that the commanded current limit was applied; the system must detect missing, stale or inconsistent feedback where applicable.

## 3. Required measured and configured values

For every managed feeder/group, record:
- Maximum permitted current per phase at the feeder boundary.
- Site incomer limits and any reserved capacity for non-EV loads.
- Measurement device location, phase mapping, accuracy class, sampling/update interval, timestamp and quality flags.
- Output phase mapping and maximum current for each output.
- Minimum controllable charging current and stop/resume behaviour under the applicable EVSE standard.
- Allocation priority/fairness policy and treatment of newly connected sessions.
- Maximum command-to-effective-current response time and transient overshoot, established by measurement.
- Local configuration protection, commissioning identity, audit trail and anti-tamper controls.
- Safe fallback envelope for each fault, justified against the physical feeder and branch ratings.

No universal current cap, update period, response time or overshoot allowance is assigned by this document.

## 4. Operating states

| State | Entry condition | Required behaviour | Exit condition |
|---|---|---|---|
| INIT | Power-up/restart | Outputs remain inhibited or within a separately approved conservative envelope until measurement, configuration and controller health are validated | All start-up checks pass |
| NORMAL | Valid measurements and healthy control | Allocate current per phase without exceeding the commissioned cap | Fault, stale data or cap/configuration change |
| LIMITED | Available capacity reduced or measurement/control quality degraded but bounded safe operation is proven | Apply a prevalidated lower envelope; never assume full nameplate | Healthy measurements and stable validation window |
| SAFE_STOP | No defensible safe allocation, unknown feeder demand, critical controller/bus failure or failed output response | Stop affected charging sessions and prevent new energisation; preserve local safe state | Fault cleared, diagnostics pass and controlled restart authorised |
| MAINTENANCE | Deliberate isolation/service | Inhibit affected outputs and require documented return-to-service checks | Commissioning checks pass |

The design must specify whether each fault causes a group-wide stop or a selective output stop. Selective operation is permitted only when the remaining demand is measured/known and the aggregate cap remains guaranteed.

## 5. Fault-response matrix

| Fault / abnormal condition | Minimum detection evidence | Required response principle | Validation |
|---|---|---|---|
| Site meter missing or disconnected | Communication/heartbeat and plausibility checks | Enter prevalidated bounded mode or SAFE_STOP; never continue using an indefinitely frozen value | Inject disconnect and verify detection/response |
| Meter data stale | Timestamp age threshold and update supervision | Reject stale sample; apply bounded fallback or stop | Freeze data and measure response |
| Meter phase mapping wrong | Commissioning phase verification and controlled load test | Block managed operation until mapping is corrected | Swap/simulate phase mapping and detect mismatch |
| Meter value implausible/out of range | Range, rate-of-change and cross-check rules | Reject value and transition to bounded/safe state | Inject invalid and discontinuous values |
| Load-manager process hangs | Independent watchdog/heartbeat | Remove permission to increase demand; transition to approved fallback | Stall process and observe outputs |
| Load-manager power loss | Power-good and watchdog supervision | Outputs enter defined safe state; no automatic unrestricted restart | Remove/reapply control supply |
| Internal communication bus failure | Bus health, sequence/timeout and endpoint feedback | Affected group stops or enters proven bounded mode; no stale limit retention without expiry | Disconnect bus and restore |
| One output ignores lower limit | Compare commanded limit with measured current/EVSE state | Stop that output; if aggregate cap cannot be guaranteed, stop group | Simulate non-responsive output |
| Contactor feedback mismatch/weld suspicion | Auxiliary feedback and current/voltage evidence as designed | Local EVSE fault handling and isolation; load manager cannot override | Inject feedback mismatch on safe bench |
| CPMS/network/cloud loss | Communications heartbeat | Local charging and local feeder cap remain controlled without cloud dependency | Disconnect WAN/CPMS |
| Controller reboot/watchdog reset | Reset cause and boot-state supervision | INIT; do not restore prior full current until all checks pass | Reboot during idle and charging bench tests |
| Configuration tampering or invalid limit | Signed/authorised config, range checks and audit | Reject invalid/increased limit; retain safe commissioned envelope or stop | Attempt unauthorised change |
| Site demand suddenly rises | Per-phase measurement and response monitoring | Reduce EV allocation before exceeding the commissioned boundary; prove transient margin | Apply step load on test rig |
| Sensor disagreement | Redundancy/cross-check rules where implemented | Use validated fallback or SAFE_STOP; no silent selection of optimistic value | Inject sensor disagreement |

## 6. Allocation and phase constraints

For each phase Lx, the allocator must enforce:

- Sum of output current commands on Lx does not exceed the EVSE allocation available on Lx.
- Other site load plus EVSE allocation does not exceed the commissioned site limit on Lx.
- A single-phase output is charged against its actual phase, not divided across three phases.
- Neutral loading and phase imbalance are explicitly assessed where single-phase outputs are mixed with three-phase outputs.
- Output minimum-current constraints, session stop/restart hysteresis and fairness are defined; the allocator must not oscillate rapidly or violate EVSE protocol requirements.
- The current limit is capped by the lowest applicable limit from output rating, branch design, feeder allocation and commissioned site capacity.

The allocator's arithmetic is not itself proof of physical compliance. Measurement latency, controller execution time, EVSE response time, contactor state, current ramp and non-EV site load transients must be included in the tested margin.

## 7. Safe fallback design rule

A fallback is acceptable only if its maximum possible aggregate current, by phase, is bounded below the safe capacity of the actual feeder and protective architecture under the fault being considered.

Possible design patterns for evaluation:
1. **Group stop:** stop all outputs served by the affected manager. Simplest to reason about where no independent trustworthy measurement remains.
2. **Prevalidated fixed cap:** continue under a fixed local limit only if the feeder is physically designed for that limit and the control path enforcing it remains independently healthy.
3. **Selective isolation:** stop only failed outputs while continuing healthy outputs, only where independent current measurement/branch control proves the remaining aggregate bound.

No fallback pattern is selected universally. The selected response must be fault-specific and supported by fault-injection results. A cloud command, cached unlimited setting or stale meter value is not an acceptable fallback.

## 8. Verification and evidence plan

Tests must start on an isolated, current-limited bench/test rig with no vehicle or mains exposure beyond an approved laboratory procedure. A competent test engineer must define the rig, instrumentation, safe fault injection and stop criteria.

For each test, record:
- hardware/firmware revisions, configuration hash and wiring/schematic revision;
- feeder/branch ratings and simulated or measured site loads;
- calibrated instrument identity and uncertainty;
- injected fault, initial state, timestamps and raw time-series data;
- command-to-response latency, peak/transient current and duration;
- state transitions, per-output current limits, contactor feedback and event logs;
- pass/fail against predeclared numeric acceptance criteria;
- reviewer and deviations/corrective actions.

### Minimum test sequence

| Test ID | Scenario | Required observation | State |
|---|---|---|---|
| LM32-T01 | Normal allocation, balanced three-phase | Per-phase sum remains within commissioned cap | NOT STARTED |
| LM32-T02 | Mixed single-/three-phase output allocation | Phase and neutral constraints respected | NOT STARTED |
| LM32-T03 | Site load step increase | EV allocation reduces within validated transient envelope | NOT STARTED |
| LM32-T04 | Site meter disconnect | Bounded fallback or safe stop occurs | NOT STARTED |
| LM32-T05 | Stale/frozen/implausible measurement | Invalid data rejected and state changes correctly | NOT STARTED |
| LM32-T06 | Phase mapping error | Managed mode inhibited | NOT STARTED |
| LM32-T07 | Load-manager process hang/watchdog | No uncontrolled increase; approved fallback reached | NOT STARTED |
| LM32-T08 | Internal bus/communications loss | Affected outputs enter defined state | NOT STARTED |
| LM32-T09 | One output ignores curtailment | Failed output isolated; group cap preserved or group stopped | NOT STARTED |
| LM32-T10 | CPMS/WAN loss | Local feeder cap and local EVSE safety continue | NOT STARTED |
| LM32-T11 | Power cycle during charging | INIT checks prevent unrestricted restart | NOT STARTED |
| LM32-T12 | Invalid/unauthorised configuration | Limit increase rejected and audited | NOT STARTED |
| LM32-T13 | Contactor feedback discrepancy | Local fault response operates | NOT STARTED |
| LM32-T14 | Sustained maximum managed load | Thermal/current stability and no cap violation | NOT STARTED |

No test in this table is claimed to have been executed.

## 9. Release gates

| Gate | Evidence required | State |
|---|---|---|
| M32-1 | Physical measurement and enforcement boundaries on single-line diagram | OPEN |
| M32-2 | Exact meter, controller, firmware and communication interfaces selected | OPEN |
| M32-3 | Per-phase site and feeder maximums commissioned and protected from unauthorised increase | OPEN |
| M32-4 | State machine and fault-specific fallback envelope approved | OPEN |
| M32-5 | Watchdog, power-loss, stale-data and bus-loss detection demonstrated | NOT STARTED |
| M32-6 | Command-to-current response and transient overshoot measured | NOT STARTED |
| M32-7 | All output non-response and contactor fault cases validated | NOT STARTED |
| M32-8 | Offline/CPMS-independent operation demonstrated | NOT STARTED |
| M32-9 | Full fault-injection evidence reviewed independently | OPEN |
| M32-10 | Qualified electrical/safety design approval and release | BLOCKED |

## 10. Release statement

M1.32 defines requirements and tests only. It does not select a load manager, meter, controller, communication bus, fallback current, response time or protection device. It does not prove the four-output CHARX cluster or any other controller topology is autonomous or fail-safe. No physical tests have been executed and no cable/protection reduction may be based on this document. The feeder must not rely on dynamic management until the exact installed system has passed the relevant calculations, fault-injection tests and independent competent review. No procurement, fabrication, installation or energisation release is granted.

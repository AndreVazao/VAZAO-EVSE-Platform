# VAZÃO EVSE Charger Hardware V1 — Local Load Management Interface and Fail-Safe Contract (M1.24)

**Status:** SYSTEM REQUIREMENTS / INTERFACE CONTRACT — NOT IMPLEMENTATION APPROVAL  
**Date:** 2026-11-25  
**Applies to:** dual and quad chargers; also reusable for multiple chargers sharing a site feeder  
**Parent:** M1.23 AC feeder topology and conductor sizing design basis

## 1. Purpose

Define the local control boundary that allows two or four EV outputs to share a constrained electrical supply without exceeding the approved feeder current. This is a system-level contract, not a claim that any controller already shortlisted supports the required interface.

## 2. Architecture boundary

The load manager is a local energy-allocation function. Each EVSE output remains responsible for its own CP/PP state machine, contactor control, feedback, protection and safe termination.

```text
COMMON FEEDER
   |
[Phase current measurement]
   |
[Local Energy Manager] <---- controlled configuration / site limit
   |       |       |       |
   A       B       C       D   (local setpoint + status interfaces)
   |       |       |       |
[EVSE A][EVSE B][EVSE C][EVSE D]
   |       |       |       |
 Type 2  Type 2  Type 2  Type 2
```

For independent incoming feeders, the measurement and control boundary is adapted to the actual site arrangement. The architecture must not assume one shared sensor is sufficient for electrically independent supplies.

## 3. Measurement contract

For a common three-phase feeder, measure all phases at the point that represents the total charger demand. The measurement system must document:
- current range and overload capability;
- accuracy class and calibration method;
- phase identification, polarity and phase sequence;
- sampling/update rate and communication latency;
- loss-of-supply, open-circuit, short-circuit and implausible-reading diagnostics;
- behavior during sensor replacement, reboot and configuration changes.

Use a measurement device suitable for the actual feeder and installation. No CT ratio, meter model or measurement accuracy is selected in M1.24.

## 4. Current allocation contract

The local manager must enforce:
- approved aggregate feeder limit per phase;
- maximum current per output and minimum controllable current required by the EVSE/vehicle interface;
- total allocated current never exceeding the configured aggregate budget, including measurement/control tolerances;
- deterministic allocation and fairness policy when demand exceeds available capacity;
- controlled ramping and hysteresis to avoid rapid oscillation;
- explicit behavior when one or more outputs start, stop or change demand;
- priority policy only when configured and auditable.

The allocation algorithm must account for phase balance. A three-phase EV output may draw across all phases, while future single-phase loads or auxiliaries can create phase asymmetry. Aggregate scalar current alone is insufficient if the site contains materially unbalanced loads.

## 5. Local enforcement and communications

- Setpoints and status exchange must use a validated local interface with documented timeout, acknowledgement and integrity behavior.
- The EVSE channel controller must enforce the accepted limit locally; the manager cannot rely on a cloud command or on a UI-only display.
- CPMS/cloud connectivity is not required for the current-limit safety function.
- The protocol, addressing, security, update rate and supported setpoint range must be confirmed for the exact controller model and firmware.
- Phoenix Contact CHARX control advanced 2902802 remains unproven for a multi-output master/cluster role in M1.4A. Do not assume its Stand-Alone/Client modes provide dynamic load management or multi-point control.

## 6. Fail-safe and degraded-mode matrix

| Fault / condition | Required system response (to be validated) |
|---|---|
| Phase sensor invalid, missing or out of range | Declare measurement invalid; prevent new load increase; transition to configured conservative fallback or stop affected charging if safe limit cannot be guaranteed |
| Local manager watchdog/reset | Outputs must not continue increasing demand on stale setpoints; apply local timeout fallback |
| Channel communication timeout | Channel rejects stale commands and applies its prevalidated local fallback; manager marks channel unavailable |
| Channel rejects setpoint | Recalculate using confirmed accepted limits; if aggregate cap cannot be maintained, reduce/stop affected channels |
| Configuration checksum/version invalid | Reject configuration and use approved safe defaults; no automatic restoration of an unverified higher limit |
| CPMS/cloud disconnected | Local allocation continues with last approved local configuration; no dependence on cloud |
| Reboot / power restoration | Start from conservative state; validate sensors and channel acknowledgements before ramping charging |
| One channel fault | Isolate/stop the affected channel as designed; redistribute capacity only after its actual state and isolation are confirmed |
| Master-to-channel bus fault | Do not assume last setpoint remains safe indefinitely; enforce timeout and local fallback at every channel |

The exact fallback current or stop action is a product safety decision and must be proven with the chosen EVSE controller. It is not assigned by this document.

## 7. Independent versus common feeder implications

- **Common feeder:** the local manager must measure the common trunk demand and allocate the shared budget across all branches. The common feeder protection remains independent of the software function.
- **Independent feeders:** each feeder must remain within its own approved current limit. A shared manager may coordinate site demand, but must not obscure or replace the independent feeder measurements/protection.
- **Both topologies:** each output retains individual protective coordination and local EVSE safety. Load management is not a substitute for overcurrent protection, RCD/DC residual-current protection, PE continuity or contactor safety.

## 8. Verification and commissioning evidence

Before relying on load management to reduce a common feeder design current, test and record:
1. all outputs requesting maximum current simultaneously;
2. phase-current measurement accuracy against a traceable reference;
3. allocation response to step changes in demand;
4. phase imbalance and single-phase auxiliary loads where applicable;
5. sensor disconnection, short circuit and implausible values;
6. loss of manager power and watchdog reset;
7. communication interruption to each channel;
8. rejected, delayed, duplicated and stale setpoints;
9. power restoration and configuration corruption;
10. CPMS/network loss while local allocation remains active;
11. proof that the aggregate feeder limit is never exceeded during transitions and faults.

Test results must include firmware/configuration identifiers, instruments, calibration status, raw measurements, timestamps, acceptance limits and reviewer.

## 9. Open evidence gates

- Exact local energy manager and phase sensor/meter model.
- Exact local fieldbus/protocol and channel setpoint API.
- Supported current setpoint range, resolution, update rate and timeout.
- Confirmed controller behavior when communication is lost.
- Allocation fairness and priority policy.
- Phase-imbalance handling.
- Validated fail-safe/default current or stop behavior.
- Hardware/software architecture independence from CPMS/cloud.
- Independent review and TestStation coverage.

## 10. Disposition

M1.24 defines requirements only. No controller, meter, sensor, protocol, current setpoint, fallback current, cable, protective device or load-management algorithm is selected or approved. M1.23 cable sections remain installation-calculation dependent.

## 11. Next step

M1.25 shall compare concrete local energy-manager and EVSE-controller interfaces against this contract using manufacturer manuals and testable protocol evidence. Do not mark the Phoenix 2902802 as compatible unless the manufacturer explicitly documents the necessary interface and behavior.

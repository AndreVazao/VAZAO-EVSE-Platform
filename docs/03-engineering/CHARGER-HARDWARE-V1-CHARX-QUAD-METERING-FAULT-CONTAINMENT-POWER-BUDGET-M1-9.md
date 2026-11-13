# VAZÃO EVSE — CHARX Quad Metering, Fault Containment and Power Budget Review (M1.9)

**Status:** DRAFT / MANUFACTURER EVIDENCE REVIEW — NOT A RELEASED DESIGN  
**Reviewed:** 2026-11-02  
**Applies to:** 1-, 2- and 4-output AC EVSE  
**Controller family:** Phoenix Contact CHARX control modular, candidate only

## 1. Purpose and result

M1.9 uses the current Phoenix Contact CHARX help pages to tighten three architectural questions left open by M1.8: per-output measurement, RFID failure behaviour, and the limits of independence between controllers in one DIN-rail cluster.

**Result:**
- The manufacturer documents a dedicated RS-485 energy-meter connection on the charging-controller interface and describes load management using a measuring device at each charging point. This supports a design basis of one correctly configured meter per independently measured output, subject to exact meter compatibility and configuration validation.
- The manufacturer documents a dedicated RS-485 RFID interface, but its error table says an RFID reader error or absent reader is an error condition. Therefore, VAZÃO must not assume that leaving the RFID port physically empty automatically produces a working public/no-RFID product. The selected controller profile must explicitly disable/ignore RFID dependency and pass cold-start and disconnect tests.
- A SEC-3xxx + SEC-1000 cluster has automatic internal communications, shared backplane power and central web-based configuration/diagnostics. The evidence does not establish independent continued operation after a SEC-3xxx failure or backplane interruption. Cluster-level dependency remains a design risk.
- The 6 A backplane limit is confirmed. It is not a 12 V auxiliary distribution design and must not be used as a substitute for branch-level power budgeting.

No production part numbers, terminal schedule, protection design or energisation approval are released by this review.

## 2. Per-output energy measurement — manufacturer evidence

The controller overview identifies a Meter connection group with:
- 12 V and GND supply;
- A+ and B− for the RS-485 energy measuring device;
- RxD and TxD reserved for future applications.

The manufacturer's load-management page describes measuring device F at each charging point. The server controller distributes current limits to client charging controllers and bases the total load-circuit limit on momentary current values read from the individual charging points. The page states that only loads detected at the charging points through the F energy meter may be installed behind the protected load-circuit fuse.

**VAZÃO design rule:** every output that participates in load management or requires session-level energy attribution must have a meter whose measurement is unambiguously associated with that output. Do not use a single shared meter as a substitute for per-output measurement.

The manufacturer also describes an optional higher-level measuring device M for the grid connection/main fuse. It can account for unknown or uncontrollable loads upstream/downstream of the charger group as described by the manufacturer's topology. This is a separate grid-feed measurement function, not a replacement for point meters.

### 2.1 Meter interface constraints

- Use the controller's dedicated meter RS-485 interface and the exact supported meter type/configuration.
- The load-management documentation says only one type of energy measuring device is to be used at the RS-485 interface in the described configuration.
- If the higher-level measuring device M is connected by RS-485 on the relevant charging point, the manufacturer requires it to be the same type as the point meters and its Modbus address to be incremented by one relative to the default settings.
- Ethernet ETH0 is also documented as an option for connecting a measuring device for total-current recording.
- Exact model compatibility, Modbus register map, address plan, baud/parity, termination, cable limits, MID status and accuracy class remain to be validated for the chosen SKU and firmware.

**Procurement gate:** Carlo Gavazzi EM340DINAV23XS1PFB remains a candidate only. Its RS-485 protocol/register map, electrical ratings, MID certificate/variant and compatibility with the current CHARX firmware must be checked before selection. The EM24 Ethernet alternative is not automatically equivalent to the documented point-meter arrangement.

### 2.2 Meter failure policy

The manufacturer's error list includes a measuring-device communication error when communication with the configured meter cannot be established.

VAZÃO must implement an explicit policy for each commercial profile:
- never fabricate, interpolate or silently reuse stale energy values as valid billing readings;
- mark the affected output's measurement as invalid/unavailable and raise a persistent diagnostic;
- prevent new billable sessions or place the output in a defined restricted mode unless a legally and contractually valid fallback exists;
- do not unnecessarily stop unrelated outputs whose own measurement and safety paths remain valid;
- preserve the fault and recovery event for audit.

Whether charging may continue without valid metering depends on the declared use case and applicable metrology/fiscal requirements; this document does not decide that legal question.

## 3. RFID optionality — important failure-mode correction

The controller overview documents a dedicated RS-485 RFID reader interface with 12 V, GND, A+ and B−.

The manufacturer's error-code table explicitly defines **RFID reader error** for a reader that triggers an error or is not connected. This is material: the physical absence of a reader cannot be treated as proof that the controller will operate in public/open-access mode.

**Required VAZÃO configuration behaviour:**
1. BASE-PUBLIC must use a documented release/authentication configuration that does not depend on RFID.
2. The RFID peripheral must be omitted from the BOM and harness population when not selected.
3. The controller configuration must not leave a mandatory RFID dependency enabled.
4. Cold-start with no reader, reader unplug during idle, reader failure during a session, and power-cycle recovery must be tested.
5. RFID failure must not cause an unsafe contactor state. The exact charging interruption/lockout response must be verified against the selected firmware and configured Event Actions.
6. For RFID profiles, define whether reader loss blocks only new authorisations or also active sessions. Do not assume this behaviour.

The documentation confirms a reader interface on the controller; it does not confirm that one shared reader can serve all four charging points. Shared-reader architecture remains prohibited for design freeze until manufacturer confirmation and multi-point tests establish addressing, session attribution and fault behaviour.

## 4. Cluster topology and failure containment

The manufacturer confirms:
- up to eleven SEC-1000 controllers can attach to one SEC-3xxx using the supplied DIN-rail connector;
- attached controllers receive supply through the backplane;
- communication is automatically established;
- attached modules are configured and diagnosed through the SEC-3xxx web management;
- the backplane nominal current limit is 6 A;
- the system prevents simultaneous operation of the connector locking mechanism.

The manufacturer also describes the SEC-3xxx as the server in load management, distributing adjusted settings to client charging controllers.

These statements confirm a managed cluster, not fully autonomous peer controllers. They do not state that clients retain full local authorisation, metering, configuration or session recovery if the server controller or backplane bus fails.

### 4.1 Conservative fault model

| Injected fault | Evidence-backed conclusion | VAZÃO acceptance requirement |
|---|---|---|
| One SEC-1000 client loses power/fails | No published guarantee found that other points remain unaffected | Test client removal/failure while other outputs charge; verify safe local state and no unintended trip |
| SEC-3xxx server fails/reboots | Server performs cluster web management and load-management distribution | Assume cluster supervisory functions are lost; verify every output's contactor drops/holds safely and define restart recovery |
| Backplane bus opens | Communication and supply are carried through the DIN-rail connector | Treat cluster as potentially affected; test breaks at both ends and between modules |
| One point meter fails | Manufacturer reports measuring-device communication error | Isolate measurement fault to that point; validate billing/charging policy and other points |
| RFID absent/fails | Manufacturer reports RFID reader error if reader is not connected or triggers error | BASE-PUBLIC must explicitly disable RFID dependency; RFID profiles need tested failure policy |
| One output contactor feedback/error | Controller enters an error state for contactor error | Lock out that output; verify other outputs remain safe and available |
| Backplane overload | Manufacturer warns electronics may be damaged above nominal 6 A | Never operate above limit; calculate worst-case configured demand with margin |

### 4.2 Independence definition

For VAZÃO, “independent output” means that each output has its own local charging controller function, CP/PP, switching/feedback, protective path, RCM/RCD strategy, measurement and fault state.

It does **not** mean that each output is immune to shared resources. In the proposed 1 × SEC-3xxx + 3 × SEC-1000 cluster, the DIN-rail bus, server controller and shared auxiliary supply are common dependencies. Until the fault-injection programme passes, the product must be described as **four locally controlled outputs in a shared controller cluster**, not four fully autonomous EVSEs.

If the required commercial availability target demands continued operation after server/bus failure, evaluate four standalone controllers or another topology with a demonstrably isolated supervisory layer. Do not bypass the manufacturer's bus design or improvise a parallel supply to obtain apparent redundancy.

## 5. 12 V and backplane power budget — calculation gate

The manufacturer specifies a nominal 6 A backplane limit and states that current consumption depends on connected I/O devices and configuration. The published standalone maximum current figures for individual controllers are not a measured cluster load and must not be summed or treated as a guaranteed cluster budget.

Create a separate load schedule for each configuration:
- controller modules and their actual operating consumption;
- lock actuators, including peak/inrush and permitted simultaneous operation;
- RFID readers;
- energy meters and RCM sensors;
- external I/O, relays, indicators and HMI;
- communications modules and antenna-related equipment;
- startup, transient and temperature derating margins.

For each load record nominal, peak, duty cycle, supply source, connector, branch fuse/current limit, conductor cross-section, voltage drop and failure consequence.

**Distribution rules:**
- Respect the manufacturer backplane topology and 6 A limit.
- Do not parallel external supplies or inject power into the bus without explicit manufacturer-approved instructions for the exact configuration.
- Where external 12 V loads are not intended to be powered from the backplane, use a separately engineered SELV/PELV supply with individually protected branches and controlled common reference/isolation as required by each interface.
- A short in an optional RFID/HMI/communications branch must not collapse the local safety controller supply or another output's safety functions.
- Validate worst-case voltage at the farthest module during permitted lock operation and simultaneous auxiliary loads.

No PSU rating or branch fuse is selected in M1.9 because the exact populated load schedule and manufacturer current data have not yet been closed.

## 6. Updated product-profile requirements

| Profile | Required verification before release |
|---|---|
| BASE-PUBLIC | Cold-start with RFID absent and RFID dependency disabled; local open-access policy; valid meter policy for declared use |
| BASE-METERED | Per-output meter detected, correctly addressed and attributable; loss-of-meter policy tested |
| RFID-LOCAL | Approved reader SKU; no-reader fault and recovery behaviour; offline credential policy |
| ETH-CONNECTED | Ethernet loss does not affect local electrical safety; load-management measurement still valid |
| LTE-CONNECTED | Cellular variant/approved modem and antenna verified; local charging survives loss of WAN |
| FULL-SERVICE | Combined peak power, thermal, EMC and fault isolation tests with every optional module fitted |

## 7. M1.9 evidence register

| Evidence | Source | Finding | Status |
|---|---|---|---|
| Controller connector overview | Phoenix Contact CHARX help — Overview of the charging controller | Meter and RFID RS-485 connector groups and signals | Confirmed functional groups; terminal-number schedule still open |
| Load management | Phoenix Contact CHARX help — Load management | Point meter F used for each charging point; server distributes current limits | Confirmed architecture principle; exact VAZÃO meter SKU/configuration open |
| Error codes | Phoenix Contact CHARX help — Error codes | RFID reader absent/error and meter communication errors are recognised faults | Confirmed; configured response requires bench test |
| Controller combination | Phoenix Contact CHARX help — Combination of SEC-3xxx and SEC-1000 | Cluster, automatic communications, backplane power, 6 A nominal limit | Confirmed grouping; failure independence not established |

Manufacturer sources (reviewed 2026-11-02):
1. https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Overview_of_the_charging_controller.htm
2. https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Load_management.htm
3. https://www.phoenixcontact.com/charx-help/Appendix/Error_codes.htm
4. https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Combination_of_CHARX_SEC-3xxx_and_-1000_charging_controllers.htm

## 8. Remaining gates / next engineering increment

1. Extract exact terminal numbers, connector positions, accessory SKUs, wire ranges, strip lengths and torque from current PDF manual and variant drawings.
2. Obtain written Phoenix Contact confirmation of SEC-3xxx server-loss and backplane-bus-loss behaviour, including client charging state and recovery.
3. Confirm exact four-output application configuration and whether each client can maintain local EVSE control safely without server communication.
4. Confirm supported meter SKUs, register map, Modbus addressing and MID variant for the intended billing use case.
5. Select and validate RFID reader SKU and determine whether a reader is required per output.
6. Complete 12 V/backplane and separately powered auxiliary load schedules for BASE-PUBLIC, RFID and FULL-SERVICE.
7. Build a low-voltage instrumented bench test for client/server/bus/RFID/meter faults before any mains-connected prototype.
8. Obtain qualified review of protective devices, RCM/RCD coordination, enclosure thermal/IP/IK, EMC and applicable EU/Portuguese conformity requirements.

**M1.9 status: PARTIAL — per-point metering principle and RFID absent-reader fault are now documented from manufacturer sources; full output independence, exact meter SKU, terminal schedule and power budget remain open.**

**Safety notice:** this is an engineering evidence review, not a construction drawing, conformity assessment, final BOM, installation instruction or permission to energise mains-connected equipment.

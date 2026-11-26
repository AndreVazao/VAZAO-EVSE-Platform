# VAZÃO EVSE Charger Hardware V1 — Repeatable Output Channel Architecture and Operating State Model (M1.28)

**Status:** FUNCTIONAL ARCHITECTURE / REQUIREMENTS BASELINE — NOT A RELEASED SCHEMATIC  
**Date:** 2026-11-26  
**Parent:** V1 requirements; electrical architecture; control and communications; M1.24 local load-management contract; M1.27 verification plan  
**Applies to:** Single, Dual, Quad, Wallbox 1/2-output and future MultiStation channel instances

## 1. Purpose and design decision

Define one repeatable AC charging-output channel (the **Output Cell**) that can be instantiated once, twice or four times in a charger. Product variants shall scale by replicating this cell and adding only the shared assemblies required by the selected feeder and communications topology.

The Output Cell owns its own EVSE safety state and power-permission decision. A shared product controller or energy manager may coordinate demand, authentication and user experience, but it must not bypass local safety checks or directly energise a channel power contactor.

This is a functional architecture. It does not select a controller, contactor, meter, residual-current device, connector, cable, terminal, fuse, PCB, protocol or exact electrical rating.

## 2. Product decomposition

### 2.1 Repeatable Output Cell

Each physical Type 2 outlet/cable is assigned a unique channel identity and contains, as applicable to the final certified design:

- Type 2 vehicle interface and PE continuity path;
- CP generation/measurement and PP/cable-current coding interface;
- local EVSE state machine and local current-limit enforcement;
- dedicated power-switching command path and contactor-state feedback;
- channel-specific protective-state inputs;
- attributable energy/current measurement for that output;
- temperature and other channel-local diagnostic inputs where required;
- isolated/appropriately protected interfaces to shared application and energy-management layers;
- unique serial/identity, firmware/configuration identity and event sequence.

The exact split between one MCU per cell and a multi-channel safety controller is OPEN. Any shared implementation must demonstrate fault containment: a fault in one channel cannot silently authorise another channel or disable its independent protective response.

### 2.2 Shared assemblies

The product may share the following assemblies, subject to electrical and safety validation:

- incoming isolation and feeder protection interface;
- distribution assembly and common-feeder measurement;
- local energy manager / master coordinator;
- application and communications processor;
- CPMS connection, local user interface and storage;
- auxiliary power generation and distribution;
- RFID/NFC, Ethernet, Wi-Fi, LTE, HMI and payment option bays;
- enclosure, thermal management and service interface.

Sharing an assembly does not merge the safety ownership of individual Output Cells.

### 2.3 Variant mapping

| Product | Output Cells | Shared elements |
|---|---:|---|
| Private Wallbox | 1 | Optional communications/authentication; local safety remains active |
| Managed Wallbox | 1 | Application/comms and optional managed-service modules |
| Dual Wallbox | 2 | Two independent cells; shared enclosure and optional local coordinator |
| Pedestal Single | 1 | Shared pedestal platform |
| Pedestal Dual | 2 | Two cells; common or independent feeder design remains selectable |
| Pedestal Quad | 4 | Four cells; cross layout preferred, lateral layout retained as an alternative |
| MultiStation | N | Site-level coordinator plus autonomous charger/channel safety boundaries |

A no-RFID, no-cloud and no-HMI configuration remains a valid basic product profile. Removing optional modules must not remove local safety, CP/PP, protective-state or safe-stop functions.

## 3. Authority and control hierarchy

The control hierarchy is:

1. **Electrical protective devices and validated hardware safety paths** — provide the independent protective functions required by the final design.
2. **Output Cell EVSE safety controller** — owns CP/PP interpretation, local current limit, contactor permission, feedback checks and safe termination.
3. **Local energy manager** — proposes/allocates a current budget; it cannot force a channel above its locally accepted limit.
4. **Application/communications processor** — handles authentication orchestration, CPMS, user interface, telemetry, updates and non-safety services.
5. **Remote CPMS/cloud** — commercial and supervisory services only; never a direct contactor authority.

A command flows downward as a request or bounded setpoint. Safety status, accepted limits, measured values and faults flow upward. A higher layer cannot clear a lower-layer safety fault merely by issuing a software command.

## 4. Output Cell operating states

The implementation shall expose a documented state machine. The following logical states are required; exact IEC 61851 CP electrical states, transition timing and normative behavior must be implemented against the applicable current standards and selected interface hardware.

| Logical state | Meaning | Power contactor policy |
|---|---|---|
| DISABLED | Channel administratively unavailable or not commissioned | Must not close |
| AVAILABLE | No vehicle detected; channel healthy and ready | Must not close |
| CONNECTED | Vehicle/cable presence detected; CP/PP evaluated | Must not close solely on presence |
| AUTH_PENDING | Authentication or local policy decision in progress | Must remain open |
| AUTHORISED | Session permitted, but charging conditions not yet complete | Must remain open until every local condition is satisfied |
| PREPARING | EV requests energy; limits and all safety permissions are checked | Close only through validated interlocks and sequence |
| CHARGING | Energy transfer permitted and monitored | Remain energised only while all permissions remain valid |
| SUSPENDED_EV | Vehicle requests temporary pause | Open/disable power path according to validated EVSE sequence |
| SUSPENDED_EVSE | EVSE pauses due to local limit, energy allocation or controlled service condition | Open/disable power path according to validated EVSE sequence |
| STOPPING | Session termination or transition out of energy transfer | Execute controlled opening and verify feedback |
| FAULT_LATCHED | Safety-critical fault or untrusted state requires intervention/recovery | Must not close |
| MAINTENANCE | Service lockout / controlled diagnostic mode | Must not close unless a separately approved test procedure explicitly governs a safe test fixture |

The state machine must separately represent session status, CP electrical state, authentication status, energy allocation status and protective status. A single generic charging flag is insufficient for safe diagnostics.

### 4.1 Entry conditions for PREPARING / CHARGING

Before permitting energy transfer, the Output Cell must confirm, as applicable to the selected design:

- CP/PP states and cable/current capability are valid;
- session authorisation is valid under the configured online/offline policy;
- local current limit is valid and not above the approved channel ceiling;
- energy-manager setpoint is current, accepted and within the local ceiling;
- protective devices and residual-current monitoring report a permitted state;
- contactor feedback and switching path are in the expected pre-energisation state;
- no latched safety fault, watchdog fault or invalid configuration is present;
- temperature and other monitored conditions are within approved limits;
- all required interlocks are satisfied.

The exact list, sequencing and diagnostic coverage must be reconciled with selected certified components and applicable standards before schematic release.

### 4.2 Stop and fault priority

A stop request or loss of a required safety permission takes priority over authentication, optimisation, user-interface and commercial operations. The channel must transition to a safe state using the validated hardware/software path.

A normal session stop, vehicle suspension, energy-budget reduction and safety fault are distinct causes and must remain distinguishable in event logs and reports.

## 5. Local current-limit contract

Each Output Cell shall enforce the minimum of all valid applicable limits, including:

- channel hardware/design ceiling;
- connector/cable capability;
- installation or feeder-derived channel ceiling;
- protective/thermal derating limit;
- operator/site configuration limit;
- locally accepted energy-manager allocation;
- any other lower limit required by the selected EVSE controller or vehicle interface.

An invalid, missing, expired, out-of-range or unacknowledged external setpoint must never increase the channel permitted current. The exact timeout and fallback behavior remain OPEN until exact controller evidence and risk assessment are available.

The energy manager shall allocate within the shared feeder budget, but each cell independently enforces its own accepted limit. If a channel cannot prove the currently accepted setpoint, the manager must not count an unconfirmed reduction as guaranteed demand relief.

## 6. Switching, feedback and protection boundary

The Output Cell shall expose distinct signals/states for:

- request to energise;
- actual contactor feedback (or validated switching-device feedback);
- protective-device status;
- residual-current / DC fault monitoring status as applicable;
- local controller health/watchdog;
- CP/PP state;
- current-limit and energy-manager setpoint status;
- channel fault and lockout reason.

A software command being issued is not evidence that the contactor physically changed state. The design must detect command/feedback disagreement and enter the approved fault response.

No generic architecture statement here approves a specific RCD/RCM arrangement, DC detection threshold, contactor pole arrangement, upstream protection, emergency-stop topology or safety integrity claim. These remain component- and standards-dependent engineering gates.

## 7. Measurement and transaction separation

Three measurement purposes must not be conflated:

1. **Feeder measurement:** aggregate phase current at the correct common-feeder or independent-feeder boundary for load management.
2. **Channel diagnostic measurement:** current/voltage values used for control diagnostics, protection coordination and service evidence.
3. **Revenue/transaction energy measurement:** attributable energy per charging output, using the meter and legal-metrology path approved for the intended market and billing model.

A meter suitable for one purpose is not automatically suitable for another. Each output energy record must be attributable to its own channel/session. A shared feeder meter alone cannot establish per-user delivered energy.

The channel event model shall link session ID, channel ID, meter identity, meter readings/records, authorisation reference, start/stop reason and monotonic event sequence. OCMF, MID, national metrology, fiscal and payment claims remain subject to their separate evidence and approval gates.

## 8. Fault containment and recovery

| Fault | Required channel-level behavior |
|---|---|
| CP/PP invalid or implausible | Do not start or continue energy transfer; record specific cause |
| Protective device / residual-current fault | Stop through validated safety path; latch or recover only as approved |
| Contactor command/feedback disagreement | Treat switching state as untrusted; prevent restart and record diagnostic |
| Channel controller watchdog/reset | Do not resume from stale permissive state; restart through conservative validation |
| Energy-manager communication loss | Apply the approved local timeout/fallback; never assume the last setpoint is valid indefinitely |
| Application CPU / CPMS loss | Local safety continues; apply the configured offline commercial policy |
| RFID/HMI/module failure | Do not affect local protective functions; apply the configured authentication policy |
| Channel meter unavailable | Apply the approved policy for measurement purpose affected; do not fabricate energy or billing data |
| Shared auxiliary supply fault | Determine affected domains; all affected channels enter their validated safe response |
| One Output Cell fault | Isolate/stop the affected channel; other channels may continue only if their independence and shared-resource margins are proven |

Recovery must identify the fault cause, validate sensors and protective states, reconcile contactor feedback, reload a valid configuration and re-establish any required energy-manager acknowledgement before a channel can return to AVAILABLE. Automatic retry limits and lockout policy remain to be specified from component behavior and risk analysis.

## 9. Modular option profiles

Optional modules are divided into two classes:

**Non-safety service modules:** RFID/NFC, Ethernet, Wi-Fi, LTE, HMI, payment terminal, printer/receipt interface, telemetry and remote-management services. Their absence or failure must not defeat local EVSE safety.

**Safety-relevant channel hardware:** CP/PP interface, local safety controller, switching/feedback, protective devices, required measurement and interlocks. These are not optional merely because a product is sold offline or without RFID.

The mechanical/electrical module interface must define power budget, isolation, connector keying, bus ownership, address assignment, hot-plug prohibition/permission, firmware compatibility and failure detection before an option board is selected. No hot-plug capability is assumed.

## 10. Required interfaces and evidence

Before detailed schematic/BOM release, freeze and verify:

- channel identity and addressing scheme;
- CP/PP electrical interface and applicable standard revision;
- local current-limit input, range, resolution, timeout and invalid-value response;
- contactor driver, coil supply, suppression, feedback and fault response;
- protective-device and residual-current interfaces;
- channel meter interface and transaction attribution;
- feeder meter / energy-manager interface and phase mapping;
- shared auxiliary supply domains and worst-case load budget;
- communication isolation, EMC, grounding and cable routing;
- offline authorisation, transaction integrity and recovery;
- firmware update, rollback and configuration integrity;
- service/test connector, safe isolation and diagnostic access.

Evidence must be tied to exact manufacturer order code, hardware revision, firmware version and controlled document revision. Family-level marketing descriptions are not enough to release a wiring schedule.

## 11. Variant-level verification matrix

| Verification | Single | Dual | Quad | Wallbox |
|---|---|---|---|---|
| Independent local safety state | Required | Per output | Per output | Per output |
| Channel identity and event attribution | One channel | Two distinct channels | Four distinct channels | One/two distinct channels |
| CP/PP and cable capability | Per output | Per output | Per output | Per output |
| Contactor command/feedback | Per output | Per output | Per output | Per output |
| Meter/session attribution | Per output | Per output | Per output | Per output |
| Local current ceiling | One channel | Each channel | Each channel | Each channel |
| Shared load allocation | Optional/site-dependent | If shared supply | Required where feeder budget is shared | If shared supply |
| Common/independent feeder validation | Applicable topology | Both design alternatives | Both design alternatives | Per installation design |
| Offline safety | Required | Required | Required | Required |
| Optional module failure isolation | Required | Required | Required | Required |

M1.27 supplies the load-management test campaign. The tests shall be instantiated per exact product profile; a test not applicable to a profile must be explicitly justified and must not be reported as a pass.

## 12. Open decisions — deliberately not frozen

- One safety MCU per output versus a validated multi-channel safety controller.
- Exact EVSE controller family and CP/PP interface.
- Exact contactor/switching architecture and feedback mechanism.
- Per-output meter and separate feeder meter models.
- Protective-device/RCM/DC detection architecture and exact coordination.
- Auxiliary supply segmentation and worst-case load budget.
- Local fieldbus, protocol, addressing and cybersecurity.
- Current-limit timeout, fallback and ramp-rate values.
- Offline authorisation and financial transaction design.
- Optional module connector/backplane and power budget.
- Enclosure thermal, EMC and environmental implementation.

These decisions require manufacturer evidence, engineering calculations, standards review and test evidence. No candidate is selected by M1.28.

## 13. Disposition and next milestone

M1.28 establishes the repeatable Output Cell and the authority/state model for the VAZÃO AC charger family. It is a functional design baseline only: no schematic, terminal schedule, component selection, cable size, protection rating, BOM release, prototype energisation or compliance approval is granted.

Next milestone M1.29 shall convert the Output Cell boundary into a requirements-to-interface matrix for the exact single-output V1 prototype, tracing every safety, measurement, power-switching, communications and service interface to a manufacturer-evidenced component or an explicitly open decision.
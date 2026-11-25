# VAZÃO EVSE Charger Hardware V1 — Supplier Technical Evidence Request (M1.26)

**Status:** INTERNAL RFI TEMPLATE — NOT SENT TO SUPPLIERS  
**Date:** 2026-11-25  
**Parent:** M1.25 Local Load Manager Candidate Evidence Matrix  
**Purpose:** obtain controlled technical evidence before any local load-management hardware or EVSE controller is selected.

## 1. Supplier / product identification

Complete one copy per supplier and exact product variant.

| Field | Supplier response |
|---|---|
| Manufacturer legal name | OPEN |
| Technical contact / role | OPEN |
| Product family and exact order code | OPEN |
| Hardware revision | OPEN |
| Firmware / software version | OPEN |
| Datasheet/manual revision and date | OPEN |
| Product lifecycle / last-time-buy status | OPEN |
| Support period and security update policy | OPEN |
| EU availability / lead time / distributor | OPEN |
| Written response date and reference | OPEN |

## 2. System topology and scale

1. How many individual AC charging outputs can one local manager coordinate simultaneously?
2. Are outputs addressed independently, or is only one aggregate power limit exposed?
3. Can the system coordinate two and four outputs in one enclosure?
4. Can multiple charger enclosures share one site meter and aggregate current budget?
5. Are mixed charger models/controllers supported? List exact validated models and firmware.
6. Is the manager compatible with both a common incoming feeder and independent incoming feeders?
7. Provide the supported single-line diagrams and maximum tested topology.

## 3. Measurement and feeder-limit enforcement

1. Which external meters and current transformers are supported? Provide exact order codes and wiring diagrams.
2. Is current measured independently on L1, L2 and L3? Provide accuracy, sampling rate and update period.
3. How are CT ratio, phase mapping, polarity, phase sequence and meter scaling configured and validated?
4. How does the manager distinguish charger current from other building/site loads?
5. What is the maximum feeder current range and measurement overload capability?
6. What is the maximum permitted aggregate current per phase, and how is it configured and protected against accidental change?
7. Does the manager account for single-phase vehicles and phase imbalance?

## 4. Per-output control interface

For every supported EVSE controller, provide:

- physical interface and protocol (e.g. RS-485/Modbus RTU, Ethernet/Modbus TCP, CAN or vendor bus);
- register/API map and version;
- current setpoint units, range, resolution and minimum value;
- update period, command timeout and acknowledgement mechanism;
- actual-current feedback and channel state;
- stale, duplicated, delayed or rejected command behavior;
- maximum number of clients and bus topology/termination requirements;
- authentication, access control and network security model.

A statement that the product supports Modbus is insufficient without the exact register map and EVSE control semantics.

## 5. Fault response and fail-safe evidence

Provide the documented response, detection time and recovery behavior for:

- meter/CT disconnected, shorted, reversed, saturated or implausible;
- loss of one or more phase measurements;
- local manager power loss, reboot or watchdog timeout;
- RS-485/Ethernet bus interruption or a single channel offline;
- EVSE controller restart, stale setpoint or rejected setpoint;
- invalid configuration, corrupt storage or unauthorized parameter change;
- CPMS/cloud loss and Internet outage;
- recovery after power restoration.

Confirm whether every EVSE channel enforces a local timeout fallback independently of the manager. State the exact fallback current or stop action and identify the source document. If no documented safe fallback exists, mark the item NOT SUPPORTED.

## 6. Electrical and environmental data

Provide rated supply voltage/current, inrush, internal dissipation, protective-device requirements, terminal conductor ranges, tightening torque, isolation boundaries, overvoltage category, pollution degree, operating temperature, humidity, IP rating, mounting orientation, dimensions, clearances and approved enclosure requirements.

No terminal or conductor value may be inferred from a marketing brochure.

## 7. Cybersecurity, maintenance and lifecycle

Provide:
- secure boot/update and signed firmware policy;
- credentials, role model, hardening and network service inventory;
- vulnerability reporting and security update lifetime;
- local logs, export and time synchronization;
- configuration backup/restore and audit trail;
- product lifecycle notice, successor compatibility and spare-part policy;
- licensing/subscription costs and operation if licence/backend is unavailable.

## 8. Evidence package required

A response is considered technically reviewable only when it includes, as applicable:

- controlled datasheet and installation manual with revision/date;
- exact terminal diagrams and single-line examples;
- meter/CT compatibility list and configuration/register maps;
- charger-controller protocol specification and setpoint examples;
- fault/degraded-mode documentation;
- firmware release notes and lifecycle/support statement;
- EU declarations/certificates and relevant test reports;
- written clarification of any discrepancies between product page, manual and application notes.

Record each received file's original filename, source URL, retrieval date, revision, file size and independently calculated SHA-256. Preserve original bytes; never overwrite a previous revision.

## 9. Candidate-specific questions

### Phoenix Contact CHARX SEC-3xxx
- Confirm which SEC-3xxx variants support multi-point local load management and maximum connected points.
- Provide the load-management application/manual section, meter profiles and current-limit register/API.
- Explain behavior on loss of meter, peer controller, internal application or LAN.
- Confirm whether SEC-1000 can act as a load manager or only as a charging-point controller in the proposed topology.
- Confirm exact differences between SEC-3000, SEC-3100 and other SEC-3xxx variants.

### Bender CC613
- Confirm exact order codes currently orderable and lifecycle/support status in writing.
- Provide current DLM manual, maximum Master/Slave count, supported external meter profiles and register maps.
- Explain the documented 30-second data collection/update cycle and whether faster current-limit response is supported.
- Provide sensor/bus/master failure behavior and exact fallback.

### Versinetic LinkRay
- Confirm exact supported charger protocol profiles and models, per-connector setpoint/acknowledgement semantics and maximum tested connector count.
- Provide the LinkRay installation/technical manual, meter profiles and local failure modes.
- Confirm whether all functions continue without Internet and which functions require SiteManager/licensing.

### aCharge TELECONTROL
- Confirm supported EVSE models, Modbus TCP register maps, meter profiles, phase measurement and multi-output support.
- Provide exact local fallback and sensor/communication failure behavior.
- Confirm supported maximum current, number of controlled outputs and product lifecycle.

## 10. Internal review record

| Gate | State | Evidence / reviewer |
|---|---|---|
| Exact product identity | OPEN | |
| Controlled manufacturer documents | OPEN | |
| Per-phase measurement evidence | OPEN | |
| Per-output setpoint and acknowledgement | OPEN | |
| Local autonomy without cloud | OPEN | |
| Sensor/controller/bus fail-safe | OPEN | |
| Cybersecurity and lifecycle | OPEN | |
| Compatibility with M1.24 | OPEN | |
| Bench validation plan | OPEN | |
| Independent engineering approval | OPEN | |

## 11. Disposition

This RFI template has **not** been sent. No supplier response is implied. No product is selected, purchased or approved. Responses must be archived and evaluated against M1.24 before a local load-management architecture is frozen.

The supplier's marketing claims, online feature list or generic protocol support are not sufficient evidence for safety-critical current-limit enforcement.

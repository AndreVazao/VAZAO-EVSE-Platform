# VAZÃO EVSE — Charger Hardware V1 — M1.16: meter architecture and bench acceptance

**Status:** PROPOSED TEST BASELINE — no production meter or electrical connection schedule approved.  
**Date:** 2026-11-10  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.13, M1.14 and M1.15.

## 1. Decision to carry into prototype

Use a two-track evaluation, not a premature single-meter selection:

- **Track A — EMH iML e-moc:** first OCMF/legal-metrology prototype candidate because Phoenix's current CHARX OCMF table names the exact meter firmware 1.09 and OCMF 1.4.1. Its direct 0.1–5(40) A rating is nominally compatible with the 32 A reference output, subject to continuous-load/thermal/protection verification and certificate scope.
- **Track B — Phoenix EEM-XM355 1674509:** point-meter/load-management alternative because current CHARX 1.9.1 configuration lists it as a selectable energy-meter type. It is not in the current CHARX OCMF list and must not be represented as the signed billing path.

EMH is the first bench candidate, not a production selection. If Phoenix cannot confirm four-point EMH operation or the certificate chain does not cover the intended use, the project returns to meter alternatives and legal review rather than silently substituting XM355.

## 2. Measurement boundary and product topology

Reference point: one AC Mode 3 Type 2 output, 400 V three-phase, configured up to 32 A/phase (nominal 22 kW).

Quad architecture:
- EVSE-01 ↔ MTR-01.
- EVSE-02 ↔ MTR-02.
- EVSE-03 ↔ MTR-03.
- EVSE-04 ↔ MTR-04.
- Optional MTR-GRID is a distinct upstream installation/load-management measurement and never replaces the four point meters.

Each output meter must measure only the energy assigned to that output. Meter identity, output mapping and transaction mapping must be unique and immutable within a session. Do not derive per-customer energy by subtracting a shared upstream meter or allocating a cluster total.

The final electrical position of each meter relative to the contactor, protective devices and connector must be established from the exact meter's approved wiring diagram and the certified measuring boundary. This document intentionally does not invent terminal numbers or a wiring schedule.

## 3. Electrical and mechanical acceptance constraints

### 3.1 EMH direct meter candidate

Before connection to any prototype:
- Obtain the complete iML e-moc installation manual and certificate package.
- Confirm direct 4-wire connection is permitted for the intended 400 V system and 32 A continuous load.
- Confirm manufacturer terminal current limits, conductor cross-sections, tightening torque, upstream fuse/MCB recommendations, short-circuit withstand and any thermal derating.
- Confirm ambient/enclosure conditions and ventilation; do not assume the headline 40 A maximum is valid in every enclosure.
- Confirm whether the meter requires 12 V auxiliary supply in the chosen operating mode and whether loss of that supply affects measurement, signature, timekeeping or record retention.
- Budget up to four meter auxiliary loads from actual manufacturer maximum/inrush data, not a nominal estimate.
- Reserve 4 HP / 72 mm DIN width per meter plus wiring bend radius, segregation, service clearance and access to seals/terminals.
- Verify IP/environmental protection is provided by the host enclosure; the meter itself is IP30.
- Confirm measurement-switching coordination settings with Phoenix/EMH. Do not change the CHARX legal-metrology setting without vendor instruction.

### 3.2 XM355 CT alternative

If Track B is tested:
- Use one CT per phase per output, with secondary exactly matching the meter (1 A or 5 A).
- Select CT primary rating, accuracy class, burden, thermal/short-time withstand and aperture from the approved meter/CT combination and actual conductor layout.
- Provide approved shorting/isolating CT terminals. Never open-circuit an energised CT secondary.
- Preserve polarity, phase mapping and output association; label CT and meter pairs.
- Do not use generic Modbus compatibility as evidence of OCMF billing support.

## 4. Bench test stages and acceptance criteria

Testing must be conducted by qualified personnel with suitable isolated/limited test equipment. Stage progression is gated; do not proceed to higher-energy testing until the previous stage passes.

### Stage 0 — document and configuration review

Required evidence:
- Exact meter SKU, hardware and firmware revision.
- Full installation manual, terminal schedule, certificate(s), declaration and approved configuration.
- Exact CHARX controller models, firmware and current supported-meter/OCMF table.
- Approved wiring diagram and supplier-confirmed four-point topology.
- CT certificates/datasheets if Track B.
- Signed test plan and risk assessment.

Pass only if all identifiers agree across meter label, certificates, manual and supplier confirmation. Any model/firmware mismatch is a fail/hold.

### Stage 1 — unpowered / SELV inspection

- Inspect meter, seals, terminals, DIN mounting and protective barriers.
- Verify low-voltage auxiliary polarity, isolation and fuse/protection against the manual.
- Verify RS-485 wiring, bus termination/biasing and unique addresses against vendor instructions.
- Verify point ID ↔ meter serial ↔ controller charging-point configuration.
- Export and hash the initial controller/meter configuration.

Pass only if no exposed hazardous conductor, no unidentified terminal and no mapping ambiguity exists.

### Stage 2 — isolated communication and signature

- Confirm meter identity, serial number, firmware, clock and configuration.
- Read the exact supported registers / OCMF payload.
- Verify signature and public-key/certificate chain using the documented verification process.
- Confirm OCMF version and meter firmware match the Phoenix compatibility table.
- Confirm the controller forwards the signed payload unchanged.
- Test invalid signature, wrong key, unknown meter, corrupted payload and wrong output mapping.

Pass only if valid records verify and every invalid/unknown condition is rejected or quarantined; no fallback to estimated energy is allowed.

### Stage 3 — isolated metrology comparison

Using an appropriate traceable reference:
- Compare voltage, current, active power and accumulated active energy at low, mid and reference operating points.
- Check all three phases independently and total energy.
- Check import/export sign convention and phase association.
- Check start/end register capture and charging-process reset/switching behaviour as specified.
- Record uncertainty, reference instrument identity/calibration and raw data.

Pass limits must be taken from the meter certificate, manufacturer specifications and the approved test uncertainty budget. Do not invent a generic percentage tolerance.

### Stage 4 — controller and contactor coordination

With a safe simulated output and no vehicle:
- Verify contactor open/closed states and the exact meter switching coordination prescribed by Phoenix/EMH.
- Test contactor feedback mismatch, welded-contact simulation, meter unavailable, meter auxiliary power loss and RS-485 loss.
- Confirm no charging session is declared billable without a valid meter identity and valid required record.
- Confirm a measurement fault cannot be mapped to another output's meter.
- Confirm local electrical safety shutdown remains independent of backend and payment services.

Pass only if the controller enters the documented safe fault state and the event is durably logged.

### Stage 5 — four-point cluster

Only after single-point acceptance:
- Configure four distinct meters and four unique charging points.
- Run independent and overlapping simulated sessions.
- Verify no cross-assignment of meter serial, OCMF payload, kWh, tariff, payment or output ID.
- Test duplicate addresses, bus/network congestion, one meter power loss, one meter communication loss, one controller loss and server/backplane interruption.
- Confirm failure of one measurement channel does not silently corrupt or bill the other three.
- Confirm the cluster's shared dependencies and recovery behaviour match the approved safety case.

Pass only if every output remains correctly attributed and all injected faults produce the defined state and durable event.

### Stage 6 — offline and recovery

- Disconnect backend/network during an authorised test session.
- Confirm local safety and charging control remain available according to the approved offline policy.
- Confirm transaction state and signed records persist across controller restart and power interruption.
- Fill the controller's documented offline queue under controlled test conditions; verify warning, full-capacity response and no silent deletion.
- Test idempotent upload, duplicate delivery, delayed delivery, signature verification and reconciliation.
- Confirm the documented CHARX limit of 100 stored charging processes and deletion behaviour against the exact firmware; do not rely on controller storage as the only archive.

Pass only if no transaction is silently lost, duplicated, misattributed or settled without verification. If the vendor's 100-record limit cannot be changed, define a backend/operator recovery mechanism and alert threshold before release.

## 5. Fault-to-response matrix

| Fault | Required response |
|---|---|
| Meter absent at boot | Output unavailable for paid operation; explicit diagnostic |
| Meter identity mismatch | Quarantine; do not authorise a billable session |
| Meter communication loss during session | Apply vendor-defined safe/controlled stop; preserve event and incomplete transaction |
| Invalid OCMF signature | Reject/quarantine record; no estimated billing |
| Wrong meter/output mapping | Block commissioning/session; never infer mapping |
| Meter auxiliary power loss | Enter defined fault; preserve controller safety and transaction state |
| One meter fails in quad | Isolate affected output; do not substitute another point's measurement |
| SEC-3xxx/server/backplane loss | Follow verified CHARX cluster safety behaviour; do not claim remaining outputs autonomous without test evidence |
| Backend/payment network loss | Apply explicit offline authorisation policy; never mark payment settled prematurely |
| Offline queue nearing capacity | Alert operator and prevent unsafe record overflow/deletion |
| Controller restart/power loss | Recover durable state and reconcile before final settlement |

## 6. Transaction record minimum

For each session preserve:
- Unique transaction/session ID and output ID.
- Meter manufacturer, model, serial, hardware and firmware.
- Meter certificate reference and configured measuring parameters.
- Signed OCMF payload, OCMF version, signature-verification result and key/certificate reference.
- Start/end energy registers, delivered kWh, direction and relevant timestamps.
- Controller identity, firmware, configuration hash and event log.
- Tariff/version snapshot and all disclosed price components.
- Authorisation mode (RFID/ad-hoc/contract/offline), payment provider reference and payment state.
- Upload/retry/reconciliation history and final settlement status.

Retain records according to the applicable fiscal, consumer, legal-metrology and data-protection requirements. This document does not set a statutory retention period.

## 7. Release gates

| Gate | Required evidence | Status |
|---|---|---|
| Exact EMH certificate and approved configuration | Manufacturer certificate package | OPEN |
| Continuous 32 A thermal/protection fit | EMH written confirmation + qualified design review | OPEN |
| CHARX four-point OCMF topology | Phoenix written confirmation | OPEN |
| OCMF signature verification | Bench test report + key handling | OPEN |
| Four-output attribution | Four-point bench report | OPEN |
| Offline 100-record handling | Vendor evidence + recovery test | OPEN |
| Portuguese legal-metrology approval | IPQ / qualified adviser written assessment | OPEN |
| AFIR public ad-hoc/payment/pricing | Operator process and compliance review | OPEN |
| Production meter selection | All above gates closed | NOT SELECTED |

## 8. Next execution package

The next practical step is to issue a controlled technical request to Phoenix Contact and EMH using the question sets in M1.15, request the exact certificates/manuals and obtain a four-unit quotation. Do not place a production purchase order until the supplier confirms firmware/topology and the certificate/legal review passes.

**Safety and compliance:** This is a bench acceptance plan only. It does not authorize fabrication, mains connection, energisation, installation, commercial billing or deployment.

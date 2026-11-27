# VAZÃO EVSE Charger Hardware V1 — Controller Evidence Request Matrix (M1.36)

**Status:** REQUEST MATRIX PREPARED / NO SUPPLIER CONTACT MADE  
**Date:** 2026-11-27  
**Candidate under evidence review only:** Phoenix Contact CHARX SEC-1000, item 1139034

## 1. Purpose

This matrix converts the unresolved M1.34/M1.35 evidence gates into precise document and technical questions that can be sent to the manufacturer or answered from controlled documentation.

No supplier contact, quotation, sample order, design approval or product selection is claimed. This is a ready-to-use request list.

## 2. Document request

| Request ID | Request | Why needed | Priority |
|---|---|---|---|
| REQ-D01 | Official latest user manual for SEC-1000 item 1139034, with document number, revision/date, firmware applicability and download source | Establish controlled source custody | P0 |
| REQ-D02 | Product-specific technical datasheet, if separate from catalog | Identify limits and technical conditions | P0 |
| REQ-D03 | Installation, wiring and commissioning instructions applicable to the exact controller | Interface and installation evidence | P0 |
| REQ-D04 | Hardware revision/change history and product lifecycle status | Baseline exact hardware and lifecycle | P0 |
| REQ-D05 | Official compatible peripheral/module list, manuals and accessory part numbers | Prevent unsupported module assumptions | P1 |
| REQ-D06 | Firmware release notes and configuration/parameter reference for applicable firmware | Understand version-dependent functions and limits | P1 |
| REQ-D07 | Manufacturer declarations/certificates relevant to controller product itself | Compliance-document traceability only; not charger assembly approval | P1 |

## 3. Technical questions — power and output loading

| Question ID | Manufacturer clarification requested | Design impact | Status |
|---|---|---|---|
| REQ-P01 | What exactly is included in “max. 2 A Stand-alone operation”? Conditions, peripherals, outputs, actuator loads, temperature and supply voltage? | Controller input-load envelope | OPEN |
| REQ-P02 | Is the <50 mA no-load figure defined at what operating state, with what peripherals excluded and what measurement conditions? | Standby/idle profile | OPEN |
| REQ-P03 | Provide startup, reset, transient and peak-current profile or test conditions, including duration where available. | Auxiliary PSU transient response | OPEN |
| REQ-P04 | Are the four 600 mA digital outputs rated individually, in aggregate, or both? What simultaneous loading restrictions apply? | External-load budget and interface selection | OPEN |
| REQ-P05 | What output protection, short-circuit behavior, thermal derating and recovery/reset behavior apply? | Fault containment and load-interface design | OPEN |
| REQ-P06 | Which output load types are permitted (resistive, inductive, capacitive, relay/coil)? Are suppression or external drivers required? | Coil/actuator interface | OPEN |
| REQ-P07 | Does the controller supply current consumption include any externally connected load powered through controller output interfaces? Clarify all exclusions. | Prevent double-counting or omitted loads | OPEN |
| REQ-P08 | Are limits affected by ambient temperature, mounting, simultaneous interface activity or firmware? | Budget derating and configuration | OPEN |

## 4. Contactor-control and switching interface

| Question ID | Manufacturer clarification requested | Design impact | Status |
|---|---|---|---|
| REQ-S01 | Confirm floating contact electrical ratings for AC and DC separately, with load type and utilization conditions. | Contactor selection compatibility | OPEN |
| REQ-S02 | Are published ratings applicable to inductive loads? State permitted suppression and maximum switching frequency/duty if specified. | Coil circuit and suppression | OPEN |
| REQ-S03 | What isolation rating, dielectric/creepage constraints and terminal wiring requirements apply to the contact interface? | Isolation and layout review | OPEN |
| REQ-S04 | Does the controller provide any coil supply? If not, confirm required external coil supply and interface circuit restrictions. | Auxiliary architecture | OPEN |
| REQ-S05 | Which contactor feedback methods are supported and recommended? Is feedback interpreted by an input or peripheral, and what are input requirements? | M1.32 feedback design | OPEN |
| REQ-S06 | What are the required fault responses for command/feedback mismatch, contactor stuck-on/off or feedback invalid? | Safety-state requirements | OPEN |

## 5. Peripheral and sensor interface evidence

| Question ID | Request / clarification | Budget row / gate | Status |
|---|---|---|---|
| REQ-I01 | Exact supported meter models and their supply sources/consumption | AUX-06 / AP-04 | OPEN |
| REQ-I02 | Exact RFID reader models, supply, idle/active/RF peak and interface limits | AUX-07 / AP-05 | OPEN |
| REQ-I03 | Exact supported residual-current detection devices, sensor supply budget, fault output semantics and required configuration | AUX-05 / AP-03 | OPEN |
| REQ-I04 | Temperature sensor wiring, supported Pt1000/PTC types, excitation/current, thresholds, failure handling | AUX-12 / AP-04 | OPEN |
| REQ-I05 | Locking actuator specifications, supply source, peak/holding or pulse requirements, release behavior and permitted hardware | AUX-09 / AP-04 | OPEN |
| REQ-I06 | System bus modules and their auxiliary load profiles; whether bus connector supplies power and limits | AUX-02 / AP-02 | OPEN |
| REQ-I07 | Communication/network features and any required external device power; confirm SEC-1000 itself has no integrated modem per catalog | AUX-08/AUX-09 | OPEN |

## 6. Integration and configuration questions

| Question ID | Request | Status |
|---|---|---|
| REQ-C01 | Recommended architecture for a single charger with one, two or four independent charge outputs; clarify controller role and supported client/server arrangement | OPEN |
| REQ-C02 | Is SEC-1000 supported as controller in a multi-output architecture, and what output-cell independence constraints exist? | OPEN |
| REQ-C03 | What is the controller's local safe behavior if communications, peripherals, sensor inputs or auxiliary supply fail? Provide state/fault documentation. | OPEN |
| REQ-C04 | Identify firmware features and configuration parameters required for offline local operation and external CPMS integration. | OPEN |
| REQ-C05 | Provide example/approved wiring diagrams for controller, meter, RFID, residual-current device, contactor and feedback, clearly marked for their intended use. | OPEN |

## 7. Evidence acceptance criteria

A supplier answer or file is not automatically accepted. It must be:
- From an identifiable manufacturer channel and date.
- Applicable to exact item/hardware and firmware version.
- Stored as original file or message with source context.
- Hash recorded for downloaded files.
- Mapped to the specific request and engineering claim.
- Reviewed for conflicts with existing catalog claims and system requirements.
- Classified and accepted only for the claim it supports.

Unanswered questions remain OPEN; no value is inferred.

## 8. Ready-to-send request text (draft, not sent)

Subject: Technical documentation and interface clarification — CHARX SEC-1000, item 1139034

We are evaluating the CHARX SEC-1000 (1139034) as a possible AC EVSE controller for a modular charger platform. Before any selection or design approval, we require the latest official technical documentation applicable to the exact product, including manual revision/date, hardware and firmware applicability, installation/wiring instructions, compatible peripherals and interface limits.

Please clarify the conditions and scope of the published 2 A stand-alone consumption and <50 mA no-load figures, including whether external loads/peripherals are included, and provide startup/transient information if available. Please also confirm the four digital outputs' per-channel and aggregate limits, simultaneous loading, protection, thermal derating, permitted load types and inductive-load/suppression restrictions.

For the floating contactor-control interface, please provide AC/DC load ratings and conditions, isolation constraints, inductive-load compatibility and suppression guidance, and feedback recommendations. Please identify exact supported meter, RFID and residual-current modules and provide their supply/load requirements. Finally, please provide the official document/download links and lifecycle/hardware revision information.

No contact has been made; this text is only a prepared draft.

## 9. Disposition

M1.36 is a structured request list and draft outreach text. It does not claim supplier communication or answers. No controller is selected, no M1.33 values are populated, no PSU/rail/fuse/conductor is sized, no schematic/BOM freeze, tests or energisation are claimed.

Next: if outreach is authorised and actually sent, record the date, channel, recipient, message, response and attachments as evidence. Until then, continue from official documentation retrieval and controlled evidence review.

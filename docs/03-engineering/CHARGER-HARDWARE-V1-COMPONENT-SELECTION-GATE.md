# VAZÃO EVSE Charger Hardware V1 — Component Selection Gate (M1.1)

**Status:** ENGINEERING SELECTION BASELINE — candidate classes only; no production part-number freeze  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Date:** 2026-10-14  
**Product:** single-output AC Mode 3, Type 2, up to 22 kW / 400 V AC / 32 A three-phase reference  
**Parent baseline:** merged Charger Hardware V1 documentation in `main`

## 1. Purpose

Move the conceptual architecture toward a traceable, component-level design. This gate defines what must be selected, the minimum evidence required, and the dependencies that prevent premature part-number freeze.

This document does **not** authorize construction, connection to mains, certification claims, or production.

## 2. Decisions retained from V1

- Local EVSE safety functions must not depend on CPMS/cloud connectivity.
- CP/PP must use a dedicated, protected EVSE interface stage; do not connect the Type 2 CP line directly to general-purpose MCU pins.
- The power contactor must have a verified coil-drive interface and auxiliary feedback (or a validated equivalent diagnostic method).
- Protective earth (PE) bonding is continuous and is never switched by the normal charging contactor.
- Commercial energy billing requires a meter and measurement chain appropriate to the legal-metrology and billing use case; a hobby current sensor is not a billing meter.
- Communications, RFID and user-interface faults must not defeat local electrical safety.
- Multi-output products replicate the per-output EVSE safety/measurement boundary; the Master allocates power but does not replace each output's local protections.

## 3. Candidate component classes

| Ref. | Function | Selection baseline | Evidence required before freeze |
|---|---|---|---|
| MCU1 | Local EVSE supervisor | Industrial MCU family; STM32G4 is a candidate for control/diagnostics, not by itself proof of compliant EVSE control | Exact MPN/package, lifecycle, watchdog behaviour, pin plan, toolchain and verified datasheet |
| EVSE1 | CP/PP and Mode 3 interface | Dedicated EVSE controller/interface or fully engineered CP/PP front-end with independent protection | Supported IEC 61851 behaviour, CP generation/measurement limits, PP handling, fault response, isolation and reference design |
| KM1 | Main power switching | AC-rated contactor sized from duty, poles, inrush/fault coordination and enclosure thermal design | Datasheet, utilization category, coil voltage, electrical life, short-circuit coordination and auxiliary feedback |
| KMD1 | Contactor driver | Protected driver matched to KM1 coil; suppression chosen with release-time constraints | Coil current, transient clamp, failure mode and MCU-independent de-energization analysis |
| EM1 | Energy measurement | Commercially suitable meter with documented accuracy and interface; MID/legal-metrology suitability assessed for intended billing model | Exact MPN, accuracy, current range, MID status/scope where applicable, wiring, protocol and calibration/replacement policy |
| RCD1 / RDC-DD | Residual-current protection | Choose a standards-compliant protection arrangement based on the EVSE's DC residual-current detection design and installation requirements | Device standards, Type A/B selection rationale, 6 mA DC detection evidence if relied upon, coordination and local installation review |
| QF1 | Overcurrent/short-circuit protection | Select from prospective fault current, cable, contactor and installation coordination study | Breaking capacity, curve/rating, conductor coordination and manufacturer tables |
| SPD1 | Surge protection | Optional/required status and type determined by installation risk/design | Earthing system, upstream protection, coordination and manufacturer instructions |
| PS1 | SELV power supply | Industrial isolated supply for control, with sufficient derating and fault behaviour | Input range, isolation, EMC, temperature derating, overload behaviour and peak load calculation |
| COM1 | Network interface | Modular Ethernet first; Wi-Fi/LTE optional by product variant | Cybersecurity lifecycle, isolation, antenna/regulatory approvals, offline behaviour and support horizon |
| RFID1 | User authentication | Secure credential reader/module; credential identifies account, not an unprotected money balance | Supported credential security, key management, anti-replay, interface and offline policy |
| TEMP1 | Thermal monitoring | Sensors at defined hot spots and near power switching/terminals as required | Range, accuracy, mounting, trip thresholds derived from component limits and validation plan |
| ENC1 / DIN1 | Enclosure and mounting | Enclosure/plate/DIN arrangement sized after thermal, IP/IK, clearance and service-access review | Dimensions, material, IP/IK evidence, corrosion, thermal model and service clearances |
| X1 | Vehicle connector | Type 2 socket or tethered cable selected per product SKU | Applicable connector standard, current/temperature rating, cable strain relief, CP/PP pin mapping and supplier evidence |
| TB1 / PE1 | Terminals and protective bonding | Rated terminals, PE bar and chassis bonding hardware | Current/voltage rating, conductor range, torque, fault withstand, bonding continuity and assembly instructions |

## 4. Protection-coordination gate

Do not assign final fuse/breaker ratings, RCD topology, conductor cross-sections, or contactor part numbers from the nominal 32 A rating alone.

Before selection freeze, record:

1. Intended supply system and earthing arrangement for the target installation.
2. Prospective short-circuit current and upstream protective-device data.
3. Cable length, installation method, ambient temperature and grouping/derating assumptions.
4. Required residual-current protection and the exact DC residual-current detection strategy.
5. Fault coordination between upstream protection, branch protection, contactor, terminals and connector.
6. PE continuity/bonding strategy and verification method.
7. Enclosure IP/IK, thermal limits, creepage/clearance and EMC constraints.
8. Whether the product is private/unmetered, commercial/billed, or intended for regulated public charging; these use cases can change metering and compliance requirements.

**HOLD:** no protection values are frozen until these inputs and manufacturer coordination data are documented.

## 5. CP/PP and local safety gate

The selected CP/PP stage must explicitly support and validate the required states, limits and fault handling for the applicable edition of IEC 61851-1 and connector implementation.

Required local interlocks before KM1 can close:

- controller startup/self-test completed;
- CP state is valid and charging is permitted;
- PP/cable coding is valid for the selected connector/cable arrangement;
- no latched critical fault;
- contactor feedback is consistent with the requested state;
- current/thermal/protection inputs are in valid ranges;
- watchdog and hardware de-energization path are healthy.

The final schematic must show the actual electrical paths, component values, protective elements, isolation boundaries, connector pins and feedback signals. A block diagram does not satisfy this gate.

## 6. Measurement and billing gate

- Separate diagnostic sensing from the legal/commercial energy-metering function.
- Define whether metering is per output, per device, or per installation before selecting EM1.
- Record accuracy requirements, calibration/replacement procedure, data retention and session reconciliation.
- The CPMS must reconcile meter/session records; it must not be the only mechanism keeping the EVSE electrically safe.
- Any claim of MID compliance or suitability for public billing must be supported by the exact device certification and intended application, not merely by a product-family name.

## 7. Communications and credential security

- Ethernet is the preferred baseline for fixed installations; Wi-Fi/LTE remain optional modules.
- Loss of Internet must not disable local protection or leave the contactor energized after a critical fault.
- RFID/NFC is an identity/authentication mechanism. Never store the authoritative monetary balance as a writable value on a basic RFID card.
- Offline authorization requires a documented secure token/allowance policy, limits, anti-replay protection, local audit log and reconciliation on reconnection.
- Define secure provisioning, firmware update, credential-key handling and support lifecycle before release.

## 8. Required engineering artefacts before M1.1 can be closed

- [ ] Exact supply/installation assumptions recorded.
- [ ] Candidate datasheets linked and revision/date recorded.
- [ ] Exact CP/PP implementation selected and independently reviewed.
- [ ] Protection coordination note completed.
- [ ] Contactor/driver/feedback arrangement validated.
- [ ] Metering use case and legal-metrology requirement established.
- [ ] Enclosure dimensions and thermal budget estimated.
- [ ] Terminal and connector pin map cross-checked against supplier documents.
- [ ] Risk analysis and verification plan updated.
- [ ] BOM separates prototype/NRE costs from production unit costs.
- [ ] VAZÃO EVSE TestStation interface and safe test points defined.

## 9. Next sequence

1. Gather manufacturer datasheets for candidate parts.
2. Resolve the protection-coordination inputs and select the RCD/DC residual-current architecture.
3. Freeze the CP/PP interface and contactor drive/feedback concept.
4. Produce the component-level schematic and terminal schedule.
5. Update the internal mounting-plate drawing with actual dimensions.
6. Publish a costed BOM with supplier, part number, quantity, alternatives, lifecycle status and price date.
7. Review integration with the VAZÃO EVSE TestStation before declaring the prototype bench-ready.

## 10. Safety and release classification

**M1.1 = component-selection gate, not a frozen production design.**

The design remains **NOT AUTHORIZED** for mains energization, fabrication release or commercial deployment until qualified electrical review, applicable compliance assessment and the defined validation gates are complete.

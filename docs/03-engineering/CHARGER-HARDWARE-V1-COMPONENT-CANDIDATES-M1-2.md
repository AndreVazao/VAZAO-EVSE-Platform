# VAZÃO EVSE Charger Hardware V1 — Evidence-backed component candidates (M1.2)

**Status:** CANDIDATE SHORTLIST — not a purchasing release or production freeze  
**Reviewed:** 2026-10-30  
**Reference design:** single-output AC Mode 3, Type 2, up to 22 kW, three-phase  
**Parent:** [Component Selection Gate](CHARGER-HARDWARE-V1-COMPONENT-SELECTION-GATE.md)

## 1. Executive selection

The strongest current approach is to use a purpose-built EVSE charge controller for the first prototype rather than designing CP/PP and the complete IEC 61851 control implementation from scratch.

| Function | Candidate | Current decision | Why / remaining gate |
|---|---|---|---|
| EVSE controller, single output | Phoenix Contact CHARX control advanced EM-CP-PP-ETH, order no. 2902802 | **Primary candidate for single-output evaluation** | Manufacturer describes Type 2, Mode 3, Case B+C, three-phase and stand-alone/client modes. Obtain full manual, I/O list, contactor feedback support, residual-current strategy, firmware/OCPP options and exact wiring before acceptance. |
| EVSE controller, multi-point / load management | Bender CC613 family | **Primary candidate for multi-output architecture study** | Manufacturer documents IEC 61851 Mode 3, configurable master/slave, dynamic load management, external Type A RCD requirement with integrated residual DC monitoring module, and OCPP 1.5/1.6. Verify exact variant, number of outputs per controller, local availability, licensing and interface requirements. |
| Energy meter, direct 3-phase | Carlo Gavazzi EM340DINAV23XS1PFB | **Candidate for per-output metering** | Manufacturer lists 5(65) A, 230/400 V, RS485 Modbus RTU and MID (Europe). Confirm exact MID certificate/variant and suitability for the intended Portuguese billing arrangement. |
| Energy meter, Ethernet alternative | Carlo Gavazzi EM24DINAV23XE1PFA | **Alternative pending detailed review** | Manufacturer lists 10(65) A, 230/400 V, Modbus TCP/IP and MID. Verify exact order code, measurement configuration and certification documents before selection. |

No prices are frozen in this document. Manufacturer pages and distributor prices can vary by region, variant, options and date. Request a written quotation from the manufacturer/distributor before costed BOM release.

## 2. EVSE controller comparison

### 2.1 Phoenix Contact CHARX control advanced — 2902802

Official product page: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802

Manufacturer-published attributes include:
- AC charging controller for IEC 61851-1 Mode 3;
- Type 2;
- Mode 3 Case B + C;
- three-phase AC;
- one charging point;
- stand-alone and client operating modes;
- Ethernet indicated by the product variant.

**Evaluation:** suitable candidate to reduce custom CP/PP implementation risk for the first single-output proof-of-concept. It is not yet accepted as the final VAZÃO controller. Confirm the exact output/contactor interface, welded-contact detection, residual-current detection integration, firmware update process, protocol support and safety documentation.

### 2.2 Bender CC613

Official product page: https://www.bender.de/en/products/charge-controller/cc613-charge-controller/  
Manufacturer manual: https://www.bender.es/fileadmin/content/Products/m/e/CC613_D00381_M_XXEN.pdf

Manufacturer-published features include:
- IEC 61851-1 Mode 3 charge control;
- configurable master/slave operation;
- dynamic load management across charging points;
- residual DC current monitoring module, with external Type A RCD required according to the documented arrangement;
- OCPP 1.5 and OCPP 1.6 support;
- Ethernet and optional modem variants documented across the product family.

**Evaluation:** particularly relevant to VAZÃO's future dual/quad and MultiStation architecture. Do not assume one CC613 controls four independent outputs: confirm the exact master/slave topology, controller count, communication wiring and supported point count with Bender before designing the quad variant.

## 3. Metering candidates

### 3.1 Carlo Gavazzi EM340DINAV23XS1PFB

Official product page: https://www.gavazziautomation.com/pt-pt/produto/EM340DINAV23XS1PFB

Published specifications:
- three-phase meter;
- 230/400 V system support;
- direct current measurement 5(65) A;
- RS485 Modbus RTU;
- MID (Europe) approval indicated by manufacturer.

**Engineering fit:** nominal 32 A per output is within the published 65 A direct-current range. This is a preliminary electrical-range match only; it does not establish installation suitability, protection coordination, metrological compliance for a specific business model, or permission to bill customers.

### 3.2 Carlo Gavazzi EM24DINAV23XE1PFA

Official product page: https://www.gavazziautomation.com/en-gb/product/EM24DINAV23XE1PFA

Published specifications:
- three-phase 230/400 V;
- 10(65) A direct connection;
- Modbus TCP/IP Ethernet;
- MID (Europe) approval indicated by manufacturer.

**Engineering fit:** useful Ethernet alternative where network topology favours Modbus TCP. Compare physical dimensions, wiring, protocol implementation, certificate scope and actual price against EM340 before choosing.

### 3.3 Metering architecture decision still open

For a single-output charger, one meter per output is straightforward. For a dual/quad pedestal, retain per-output energy attribution as the default architecture unless a documented metering design proves an alternative can attribute each session accurately and withstand audit.

The exact meter certificate, firmware/parameter configuration, sealing requirements and Portuguese legal-metrology obligations must be reviewed before commercial billing. A product page stating MID is not a substitute for checking the certificate for the exact order code and intended use.

## 4. What is deliberately not selected yet

The following are held open because a responsible selection depends on installation and system-level data:

- QF1 breaker/fuse ratings and breaking capacity;
- RCD type/topology and residual-DC detection coordination;
- KM1 contactor MPN, utilization category, coil voltage and short-circuit coordination;
- conductor cross-sections, terminal ratings and torque values;
- SPD type and coordination;
- SELV PSU model and power rating;
- enclosure IP/IK, thermal design and mounting dimensions;
- Type 2 socket/tethered cable exact MPN;
- RFID secure element/reader and credential-key management.

Do not infer these values from 22 kW or 32 A alone.

## 5. Recommended prototype architecture

**Prototype A — single output:** evaluate Phoenix Contact 2902802 as the integrated EVSE controller candidate, with a separately selected contactor/protection/metering chain. Evaluate the EM340 Modbus RTU variant for energy metering. The controller's own documentation must determine how contactor drive, feedback, RCD/DC detection and emergency stop are wired.

**Architecture B — dual/quad:** evaluate Bender CC613 master/slave for local dynamic load management. Each charging point must retain the required local control and protection boundary. Do not use a central Master as a substitute for per-output safety functions.

**Important:** do not mix controller wiring assumptions between Phoenix Contact and Bender. Each candidate requires its own manufacturer-specific schematic and review.

## 6. Supplier evidence checklist

Before purchasing any candidate:
- [ ] Request current full datasheet, installation manual and wiring diagram.
- [ ] Confirm exact order code and hardware/firmware revision.
- [ ] Obtain declarations/certificates relevant to intended EU application.
- [ ] Confirm supply voltage, I/O ratings, relay/contact ratings and isolation.
- [ ] Confirm residual-current protection requirements and external devices.
- [ ] Confirm OCPP version, licensing and backend integration conditions.
- [ ] Confirm lifecycle, lead time, warranty and technical support in Portugal/EU.
- [ ] Obtain written unit pricing for prototype quantity and production quantity.
- [ ] Record supplier, quotation date, currency, VAT and shipping separately.

## 7. Sources

1. Phoenix Contact — EM-CP-PP-ETH, order no. 2902802: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802
2. Bender — CC613 product page: https://www.bender.de/en/products/charge-controller/cc613-charge-controller/
3. Bender — CC613 operating manual: https://www.bender.es/fileadmin/content/Products/m/e/CC613_D00381_M_XXEN.pdf
4. Carlo Gavazzi — EM340DINAV23XS1PFB: https://www.gavazziautomation.com/pt-pt/produto/EM340DINAV23XS1PFB
5. Carlo Gavazzi — EM24DINAV23XE1PFA: https://www.gavazziautomation.com/en-gb/product/EM24DINAV23XE1PFA

## 8. Release status

**M1.2 shortlist only.** This document supports supplier enquiry and detailed engineering evaluation. It is not a final BOM, wiring instruction, certification, installation approval or authorization to energize mains.

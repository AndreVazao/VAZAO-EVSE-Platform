# VAZÃO EVSE — Charger Hardware V1 — M1.14: OCMF meter alternatives review

**Status:** PARTIAL — EMH iML e-moc is the strongest current CHARX-listed OCMF candidate found; Portuguese deployment approval and four-point validation remain open.  
**Date:** 2026-11-10  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.12 and M1.13.

## 1. Executive result

M1.13 identified a gap between MID product claims, CHARX point-meter profiles and CHARX legal-metrology/OCMF compatibility. M1.14 evaluates the current OCMF-listed alternatives.

**EMH iML e-moc** is the strongest candidate to investigate first:
- Phoenix Contact's current CHARX legal-metrology page lists EMH iML e-moc, firmware 1.09, OCMF 1.4.1 as compatible.
- EMH's current product page describes it as a bidirectional e-mobility meter with MID and national approval, Modbus RTU with OCMF data tuple or SML, and charging-process signature.
- Its published datasheet specifies direct 4-wire measurement, 3 × 220/380 V to 3 × 230/400 V AC, 0.1–5(40) A, class B EN 50470-3, RS-485 Modbus/SML/OCMF and 12 V DC auxiliary supply for standby/RS485 functionality.
- The 40 A maximum is above the 32 A reference output current, but leaves limited headroom; protection coordination, thermal conditions and meter overload limits must be checked.

**Important boundary:** German MID/national approval and CHARX OCMF compatibility do not automatically establish legal suitability for commercial billing in Portugal. The Portuguese legal/metrology/fiscal route must be confirmed before any billing claim.

The BAUER BSM-WS36A-Y is also listed by CHARX for OCMF, but the public manual located in this review is for a different model designation (BSM-WS36A-H01-1311-0000). Its specifications must not be transferred to the Y variant. No procurement decision is made.

## 2. EMH iML e-moc evidence

Manufacturer product page:  
https://emh-metering.com/en/products/e-mobility/iml-e-moc-for-compact-e-mobility-solutions/

Manufacturer datasheet (DAB-E 1.07, April 2025):  
https://emh-metering.com/wp-content/uploads/2025/04/iML-e-moc-DAB-E-1.07.pdf

### 2.1 Product and measurement properties

Extracted from the manufacturer datasheet:
- Electronic direct-connected 4-wire meter.
- Voltage: 3 × 220/380 V to 3 × 230/400 V AC; single-phase 220/230 V option.
- Current: 0.1–5(40) A.
- Active energy accuracy class B under EN 50470-3.
- Bidirectional active energy registers (+A import / -A export).
- Separate registers for compensated line losses and resettable registers for charging-process energy.
- Charging-process duration register and measurement-switching coordination.
- EEPROM data preservation, stated at least 20 years.
- One potential-free Opto-MOSFET output, max 250 V AC/DC, max 0.1 A.
- One potential-free input, max 265 V AC.
- RS-485 interface supports Modbus or SML/OCMF/OBUS; 9600 to 115200 baud.
- 12 V DC nominal auxiliary supply, +8 to +13.2 V DC, less than 100 mA, required for standby power/RS485 functionality as described in the datasheet.
- Typical voltage-circuit power consumption 0.8 W per phase.
- Mechanical environment M2 and electromagnetic environment E2 under the Measuring Instruments Directive.
- DIN rail mounting, 4 HP, 72 × 90 × 63 mm; IP30.
- Operating range -30…+75 °C.
- Charging-specific functions include signed records, customer ID attributes, ad-hoc pricing display and transparency-software verification.

The manufacturer page describes MID and national approval and an OCMF data tuple. The datasheet itself contains German approval markings and class B measurement data. Exact certificate numbers, scope, firmware and approved configuration must be obtained from EMH before selection.

### 2.2 CHARX compatibility

Phoenix Contact current legal-metrology page:  
https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Legal_metrology.htm

The current CHARX OCMF table lists:
- Manufacturer: EMH
- Model: iML e-moc
- Version: 1.09
- OCMF version: 1.4.1
- Configuration: protocol set to Modbus; baud rate 38400 or 115200; internal measurement-switching coordination deactivated.

This is materially stronger integration evidence than a generic Modbus-compatible meter. The listed meter firmware and configuration must be matched exactly; do not substitute another EMH model or firmware without confirmation.

The current CHARX page says signed OCMF records are sent via OCPP. It also states that only OCPP release mode makes OCMF records available; continuous charging release mode does not provide downloadable OCMF records. Offline charging records are temporarily stored on the controller, with a documented limit of 100 charging processes before older records are deleted. This limit is a product/operations requirement and must be addressed before promising offline billing.

## 3. Fit against VAZÃO EVSE reference output

Reference: 400 V three-phase, 32 A per phase, up to 22 kW AC.

| Requirement | iML e-moc evidence | Assessment |
|---|---|---|
| 3-phase 400 V | 3 × 230/400 V AC | Nominal voltage matches |
| Direct measurement | 0.1–5(40) A | 32 A below 40 A maximum; detailed thermal/protection check required |
| Bidirectional energy | +A / -A registers | Supported |
| MID | Manufacturer states MID and national approval | Certificate scope to verify |
| CHARX OCMF | Listed by CHARX, firmware 1.09 / OCMF 1.4.1 | Strong manufacturer compatibility evidence |
| Communication | RS-485 Modbus / OCMF | CHARX-specific baud/configuration required |
| Standby/RS485 supply | 12 V DC, <100 mA | Must be included in PWR-AUX budget |
| Mechanical | 4 HP, 72 × 90 × 63 mm, IP30 | Panel space and enclosure protection required |
| Four-output cluster | No four-point bench evidence yet | Open |

The 40 A rating is not a blanket approval for continuous 32 A service in the final enclosure. Check manufacturer derating, ambient temperature, terminal ratings, conductor cross-section, upstream protective device, short-circuit conditions and enclosure thermal design. Meter supply and auxiliary power must be calculated for four devices, with suitable protection and isolation.

## 4. BAUER BSM-WS36A-Y — evidence gap

CHARX current legal-metrology page lists BAUER BSM-WS36A-Y, firmware V60, OCMF 1.4.0. The configuration notes require internal measurement-switching coordination and an additional infrared probe (e.g. BAUER BSM-IRM).

A public BAUER manual retrieved during this review is titled **BSM-WS36A-H01-1311-0000**, not BSM-WS36A-Y. It describes a directly connected 4-wire meter, 0.25–5(60) A, RS-485 Modbus RTU, signed charging data and measurement-switching coordination. These details are evidence for the H01 variant only and **must not be attributed to the Y variant**.

Required before any comparison or selection:
- Exact BSM-WS36A-Y datasheet and manual.
- Confirmation of current product lifecycle and orderable item number.
- Exact V60 firmware and OCMF 1.4.0 scope.
- Infrared probe model, mounting, alignment and compatibility.
- Current transformer/direct measurement topology and electrical ratings for the Y variant.
- Written Phoenix Contact/BAUER confirmation for the intended CHARX firmware.

No BAUER part is approved.

## 5. Candidate comparison

| Meter | CHARX point-meter profile | CHARX OCMF list | Measurement topology | Current assessment |
|---|---|---|---|---|
| EMH iML e-moc | Not the generic XM profile; OCMF-specific supported path | Yes, v1.09 / OCMF 1.4.1 | Direct, 0.1–5(40) A | First candidate for legal-metrology prototype |
| BAUER BSM-WS36A-Y | OCMF-compatible path | Yes, V60 / OCMF 1.4.0 | Exact Y topology not yet evidenced | Hold pending exact variant documentation |
| Phoenix EEM-XM355 1674509 | Yes, selectable in current CHARX point-meter configuration | Not listed | CT 1 A/5 A | Point metering/load management candidate; no OCMF evidence |
| Phoenix EEM-XM375 1674510 | Not listed in current CHARX point-meter configuration | Not listed | CT 1 A/5 A, Ethernet | Do not assume CHARX integration |

## 6. Critical Portuguese compliance boundary

The EMH page's MID and national approval statements, and CHARX's OCMF integration, are not a complete Portuguese legal opinion. Before using a meter for customer billing or AFIR ad-hoc charging, obtain a documented review covering:
- Whether the meter's EU type-examination/MID certificate and national approval are recognised for the exact Portuguese use case.
- Whether the complete measuring chain, firmware, sealing, installation, configuration and OCMF backend process fall within the certificate scope.
- Applicable Portuguese metrology authority requirements, including DGEG/competent authority interpretation.
- Fiscal invoicing, tariff display, transaction evidence and consumer transparency.
- AFIR ad-hoc payment/price disclosure and the operator/EMSP responsibilities.
- GDPR and retention/access controls for signed transaction data and customer attributes.

Do not advertise the product as “Eichrecht compliant”, “Portuguese MID billing compliant” or legally certified based only on this research.

## 7. Required validation and procurement gates

1. Obtain EMH's complete type-examination/MID and national approval certificates, firmware release notes and installation instructions.
2. Obtain written EMH confirmation of continuous 32 A operation at the intended ambient/enclosure conditions and the required upstream protection.
3. Obtain Phoenix Contact confirmation of the exact SEC-3xxx/SEC-1000 topology and supported OCMF configuration for four iML e-moc meters.
4. Verify that the SEC-3xxx version in the intended cluster supports the required OCPP release mode and OCMF version.
5. Validate meter serial identity, public-key retrieval, signature verification and end-to-end OCMF packet preservation at the backend.
6. Test one meter first, then four independent outputs; include wrong meter identity, missing meter, communication loss, power loss, restart, clock drift, counter persistence and output-to-transaction attribution.
7. Test offline storage limit behaviour and alert/operator recovery before the 100-record deletion boundary.
8. Obtain Portuguese legal/metrology/fiscal review and supplier quotation/availability before BOM approval.

Bench tests must use appropriate isolated equipment and a qualified test procedure. No mains energisation or vehicle charging is authorised by this document.

## 8. Gate status

| Gate | Status |
|---|---|
| CHARX lists EMH iML e-moc for OCMF | CONFIRMED in current manufacturer help |
| EMH product supports MID/national approval and OCMF | CONFIRMED at manufacturer product-page level |
| Published electrical fit for 400 V / 32 A reference | PLAUSIBLE; 40 A max, thermal/protection checks open |
| Exact certificate scope and firmware | OPEN |
| Four-output CHARX cluster validation | OPEN |
| OCMF signature/public-key/backend verification | OPEN |
| Offline 100-transaction retention process | OPEN |
| Portuguese legal/fiscal suitability | OPEN |
| Approved production meter | NOT SELECTED |

## 9. Next actions

1. Prioritise a technical enquiry to EMH and Phoenix Contact for the iML e-moc / CHARX four-point OCMF configuration.
2. Request the exact certificates, firmware, approved wiring/protection, current lifecycle and commercial quotation.
3. Compare EMH's direct 40 A meter with the CT-based XM355 point-meter candidate against actual billing and load-management needs.
4. Keep BAUER BSM-WS36A-Y on hold until the exact Y variant documentation is received.
5. Start Portuguese compliance review before making any commercial billing claim.

**Safety and compliance:** M1.14 is a candidate evaluation only. No meter, protection device, wiring, installation or billing workflow is approved. No fabrication or energisation release.

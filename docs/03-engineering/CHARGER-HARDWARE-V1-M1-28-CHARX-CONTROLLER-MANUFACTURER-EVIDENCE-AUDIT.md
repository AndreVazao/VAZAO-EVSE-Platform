# VAZÃO EVSE — Charger Hardware V1
## M1.28 — CHARX controller manufacturer evidence audit

**Status:** PRIMARY-SOURCE DESK REVIEW COMPLETE; CONFIGURATION AND HARDWARE VALIDATION OPEN  
**Date:** 2026-11-17  
**Scope:** Phoenix Contact CHARX control modular SEC-1000 / SEC-3xxx family only.  
**Depends on:** M1.7–M1.13, M1.17–M1.19, M1.25–M1.27.

## 1. Purpose and evidence boundary

This milestone re-checks the controller-family identity, official order numbers, documented interfaces and cluster constraints against current Phoenix Contact product/help pages. It corrects the project candidate register where exact product identity was previously expressed only as a family/class.

This is a manufacturer-source desk review, not a supplier confirmation, product sample inspection, wiring approval, firmware test, bench test or safety certification of the VAZÃO EVSE design. The online product pages are not archived evidence files in this repository; no source-file SHA-256 is claimed. The cited manufacturer pages are the authoritative references to retrieve and archive under the M1.25 source-control rules before design release.

## 2. Exact product identity and roles

| Role | Manufacturer product | Order number | Manufacturer-described capability | VAZÃO EVSE status |
|---|---|---:|---|---|
| Per-output charging controller | CHARX SEC-1000 | 1139034 | IEC 61851-1; stand-alone/client; CHARX backplane bus; connectable meter, RFID and DC residual-current sensor; DIN rail | Leading local output-controller study candidate; not selected |
| Cluster/server controller | CHARX SEC-3000 | 1139022 | IEC 61851-1; Embedded Linux; stand-alone/client/server; 2× Ethernet; USB-C; OCPP 1.6J, Modbus/TCP, MQTT; backplane bus | Leading cluster/server study candidate; not selected |
| Cellular cluster controller | CHARX SEC-3100 | 1139012 | SEC-3000 class plus 4G/2G cellular interface | Optional communications alternative; not selected |
| ISO 15118-capable controller | CHARX SEC-3050 | 1139018 | SEC-3000 class plus ISO/IEC 15118 | Vehicle-communications alternative; not selected |
| Cellular + ISO 15118 | CHARX SEC-3150 | 1138965 | SEC-3100 class plus ISO/IEC 15118 | Optional high-capability alternative; not selected |

Manufacturer ordering data identifies SEC-1000 as 1139034, SEC-3000 as 1139022, SEC-3050 as 1139018, SEC-3100 as 1139012 and SEC-3150 as 1138965. The product-family overview separates the feature sets: embedded Linux, web management, OCPP and load management are SEC-3xxx functions; cellular is SEC-31xx; ISO/IEC 15118 is SEC-3x50. Do not treat all SEC-3xxx variants as having LTE or ISO 15118.

The current manufacturer user-manual index identifies UM EN CHARX SEC, Revision 06, firmware 1.9.1 for the above exact order numbers. Firmware/document revision must still be recorded against the physical sample and actual configuration before a prototype is wired.

## 3. Cluster topology and backplane constraints

Manufacturer help states:

- Up to 11 CHARX SEC-1000 controllers can be attached to one CHARX SEC-3xxx using the supplied DIN-rail connector.
- The connected controllers receive their supply via the DIN-rail connector.
- Supply may be fed through the SEC-3xxx or one of the attached SEC-1000 units.
- Communication between the SEC-3xxx and attached SEC-1000 controllers is established automatically.
- Attached modules are configured and diagnosed through the SEC-3xxx web-based management.
- The nominal current capacity of the backplane bus is 6 A. Phoenix explicitly requires the complete configuration's maximum current consumption to be determined, including attached I/O devices; the system prevents simultaneous operation of the connector-locking mechanism as a protective measure against bus overload.

**Impact on the VAZÃO quad study:** 1 × SEC-3000 (1139022) + 3 × SEC-1000 (1139034) is within the manufacturer's stated module-count limit. That does NOT prove the four-controller configuration fits the 6 A budget. No current budget can be closed from the nominal idle figures alone. Controller consumption depends on attached I/O and configuration. Every RFID, RCM, meter, lock actuator and other powered load must be included using the exact manual values and worst-case operating concurrency.

The backplane is a shared dependency. Loss of the SEC-3xxx, bus power, DIN connector or common supply can affect multiple outputs. The manufacturer's automatic communications and shared management do not establish independent safe operation under every cluster fault. VAZÃO must retain a per-output safe-state analysis and prove the response through controlled bench fault injection before relying on this architecture.

## 4. Per-output interface evidence

The manufacturer's controller overview documents these functional groups:

| Functional group | Documented interface | Design implication / restriction |
|---|---|---|
| Supply and RFID | 12 V/GND and RS-485 A+/B- for RFID | Reader supply and bus load belong in the 12 V budget; verify exact reader model and addressing |
| Digital outputs | OUT1–OUT4, configurable high-side 12 V or low-side 0 V | Do not assume they can drive a contactor coil or arbitrary external load; respect exact electrical limits |
| Digital inputs | IN1–IN4, 0–12 V | Define input protection, signal common and fail-state in the actual design |
| Temperature | PTC chain or Pt1000 | Confirm sensor type, wiring, threshold and fault response for each thermal zone |
| Meter | 12 V/GND and RS-485 A+/B- | Meter is a serial peripheral; exact supported meter profile and per-output attribution remain separate acceptance gates |
| RCM | 12 V supply, ER1/ER2 status, TST and NC terminals | Exact sensor variant, logic polarity, test/reset and fault response must match manual; RCM does not replace final protective disconnection design |
| Socket / vehicle | CP, PP, LO-/LO+, LD1/LD2 | CP/PP and lock actuator are local output interfaces; validate cable/actuator and safe release behaviour |
| Backplane | DIN-rail bus connector | Shared power and communication dependency; 6 A nominal limit |
| SEC-3xxx network | 2× Ethernet RJ45, USB-C, microSD; cellular antenna/SIM on SEC-31xx | Network, commissioning and cellular hardware are variant-specific |

The manufacturer documentation identifies CP as IEC 61851-1 control pilot and PP as proximity detection; locking control is ±12 V with lock feedback. The controller has a documented integrated release function for the locking actuator on mains failure. The exact mechanical actuator, cable, socket and installation must still be validated.

## 5. Contactor interface — important variant distinction

The manufacturer documentation distinguishes the contactor interface by controller type:

- **SEC-1000:** C1/C2 floating switch contact; the other positions shown as NC are not connected.
- **SEC-3xxx:** C1/L is the mains-phase input for the floating contactor switch and zero-cross detection use case; C2/L* is the switching output; N terminals are provided for zero-cross detection associated with ISO/IEC 15118 communications.

For the SEC-3000 product page, the published contactor interface is a floating switch contact rated up to 250 V AC / 30 V DC, 2 A rated current, maximum interrupting rating 1500 VA. The SEC-1000 page also identifies a floating switch contact with the same published limits.

**Engineering restriction:** these ratings do not by themselves prove compatibility with the selected contactor coil. Coil inrush, holding VA, suppression, switching category, phase reference, fault behaviour, contact life and required external interface must be checked against the exact contactor and the complete manual. Do not connect a coil directly merely because its steady-state current appears below 2 A. The VAZÃO design must retain independent contactor feedback and safe de-energisation; the manufacturer's floating contact is not proof of welded-contact detection.

## 6. Published technical values — not a closed design budget

| Parameter | SEC-1000 1139034 | SEC-3000 1139022 | Use in VAZÃO |
|---|---:|---:|---|
| Supply | 12 V DC ±5% | 12 V DC ±5% | Common supply tolerance to be respected |
| Maximum current consumption, stand-alone | 2 A | 2 A | Not a substitute for clustered worst-case calculation |
| No-load consumption, without external loads | <50 mA | <200 mA | Baseline only; external loads and active functions increase consumption |
| Digital inputs | 4 | 4 | Configure and protect per design |
| Digital outputs | 4, max 600 mA, low-side | 4, max 600 mA, low-side | Do not use as assumed contactor-coil driver |
| Meter interface | RS-485 | RS-485 | Meter profiles/OCMF are separate gates |
| RFID interface | RS-485 | RS-485 | Optional module; secure offline policy remains VAZÃO responsibility |
| Temperature | Pt1000 / PTC | Pt1000 / PTC | Exact sensor wiring and trip configuration required |
| Width × height × depth | 18.8 × 121 × 85 mm | 37.6 × 121 × 85 mm | Manufacturer product dimensions; M1.25 record still needs source archive, revision, datum and review |
| Protection | IP20 | IP20 | Must be installed in a suitable enclosure |
| Operating temperature | -25 °C to +65 °C | -25 °C to +65 °C | Does not replace enclosure thermal calculation |

These values are manufacturer-published for the exact order numbers reviewed. They are not a complete 12 V load budget and do not close the panel thermal calculation.

## 7. Configuration implications

1. The SEC-1000 is a real candidate for a local per-output control module; the SEC-3000 is a real candidate for the cluster/server role.
2. The quad topology remains 1 × SEC-3000 (1139022) + 3 × SEC-1000 (1139034) for evaluation, not an approved architecture.
3. SEC-3150 (1138965) is not the generic SEC-3000: it adds cellular and ISO/IEC 15118 capabilities. Choose it only if those functions are required and its additional power, antenna, SIM, security and lifecycle implications are accepted.
4. The product family supports a single SEC-1000 stand-alone point, but when configured as a client under SEC-3xxx, higher-level charging authorisation is processed through the SEC-3xxx application. Stand-alone SEC-1000 charging authorisation requires explicit Event Actions configuration. This behaviour must be included in offline and cluster-loss acceptance tests.
5. A four-point cluster does not satisfy the VAZÃO requirement for independent safe outputs until failure injection proves each output's safe response to SEC-3xxx loss, bus interruption, supply loss, communication loss, meter failure, RCM fault, controller restart and recovery.
6. The manufacturer's pages currently indicate that the product family is being prepared for EU Cyber Resilience Act requirements expected from 11 December 2027. This is a manufacturer status note, not evidence of completed CRA conformity. VAZÃO must obtain the applicable security/support statement and product lifecycle commitment before commercial selection.

## 8. Primary manufacturer references

All references below are Phoenix Contact primary sources, accessed 2026-11-17:

1. Product page — CHARX SEC-1000, item 1139034: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034
2. Product page — CHARX SEC-3000, item 1139022: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-3000-1139022
3. Product-family ordering data: https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Ordering_data.htm
4. Product-family interface/terminal overview: https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Overview_of_the_charging_controller.htm
5. SEC-3xxx + SEC-1000 combination and 6 A backplane limit: https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Combination_of_CHARX_SEC-3xxx_and_-1000_charging_controllers.htm
6. Current user manual index, UM EN CHARX SEC Revision 06 / firmware 1.9.1: https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm
7. SEC-1000 stand-alone/client configuration and Event Actions: https://www.phoenixcontact.com/charx-help/ctrl/ac/um/Section05/Sec_5_en.htm

## 9. Open gates and next actions

| Gate | Required evidence | State |
|---|---|---|
| C28-1 | Confirm exact sample order numbers and hardware revisions | OPEN |
| C28-2 | Archive manufacturer product pages, manual and terminal drawings under M1.25 source/hash rules | OPEN |
| C28-3 | Extract exact current consumption for every controller/peripheral and calculate worst-case 1/2/4-point 12 V budget | OPEN |
| C28-4 | Resolve supply injection location, conductor protection and backplane current monitoring/derating | OPEN |
| C28-5 | Verify SEC-1000 versus SEC-3xxx contactor terminal wiring against full manual and exact contactor coil | OPEN |
| C28-6 | Prove per-output isolation and safe states under cluster, bus, power and server failure | NOT STARTED |
| C28-7 | Verify meter, RFID and RCM exact variants and simultaneous peripheral loading | OPEN |
| C28-8 | Confirm firmware 1.9.1 or later supported release, update/security lifecycle and offline authorisation | OPEN |
| C28-9 | Independent electrical review of the controller/contactor/RCM integration | OPEN |
| C28-10 | Controlled low-voltage bench validation; no mains energisation until qualified review and separate approval | NOT STARTED |

## 10. Conclusion

The manufacturer source audit supports a more precise study topology: SEC-3000 1139022 as the cluster/server controller with SEC-1000 1139034 as per-output controllers. It confirms a maximum of 11 SEC-1000 modules per SEC-3xxx and the hard 6 A nominal backplane limit. It also confirms that SEC-1000 and SEC-3xxx contactor terminals are not interchangeable.

The topology remains a candidate only. The 6 A load budget, exact terminal wiring, contactor-coil compatibility, cluster fault containment, offline authorisation and four-output peripheral loading must be proven before design freeze. No component is approved for production and no wiring, fabrication, energisation or installation is released.

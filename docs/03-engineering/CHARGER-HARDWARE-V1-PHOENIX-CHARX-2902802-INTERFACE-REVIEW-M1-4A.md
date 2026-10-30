# VAZÃO EVSE Charger Hardware V1 — Phoenix CHARX 2902802 Interface Review (M1.4A)

**Status:** PARTIAL DOCUMENTARY EXTRACTION — NOT APPROVED FOR WIRING  
**Reviewed:** 2026-10-30  
**Exact catalogue item:** Phoenix Contact EM-CP-PP-ETH, item 2902802  
**Official source:** https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802

## 1. Scope and evidence quality

This review extracts the manufacturer-published product data currently available on the official product page. The installation/operating manual with the definitive terminal diagram and application wiring was not retrieved in this review. Therefore, no terminal numbers, CP/PP pin mapping, contactor-coil wiring, safety-input wiring or commissioning sequence is asserted here.

The product page is authoritative for the published catalogue data below, but it explicitly directs users to the complete user documentation for complete data. M1.4A remains open until that documentation is obtained and reviewed.

## 2. Confirmed manufacturer data

| Item | Published data | Engineering implication |
|---|---|---|
| Product | EM-CP-PP-ETH, 2902802; CHARX control advanced | Exact catalogue reference identified |
| Charging | AC three-phase; Type 2; Mode 3, Case B + C | Matches the broad V1 AC Mode 3 use case |
| Charging points | 1 | Treat as one controller per output unless manufacturer documents another arrangement |
| Operating modes | Stand-alone and client | Does not itself prove multi-controller master/load-management behaviour |
| Modem | No modem present | External communications path required if cellular is needed |
| Supply | 230 V nominal; 110–240 V AC nominal range; 95–264 V AC published operating range; 45–65 Hz | Design a protected supply only after installation manual review |
| Consumption | Maximum 40 mA; nominal power below 1 W at no load | Confirm actual power budget and protective arrangement from manual |
| Digital inputs | 4; nominal 24 V; OFF −3…5 V; ON 15…30 V; input current ≤8 mA | Potential integration points; functions and isolation must be verified in manual |
| Digital outputs | 4; maximum 30 V; 0.2 A total with internal supply; up to 0.6 A/channel with external supply | Do not use to drive a contactor coil without a documented compatible interface/driver |
| Relay V1.2 | Maximum 250 V AC, 2 A | Rating alone does not identify its intended function or establish suitability for a particular coil |
| Relay C1.2 | Maximum 250 V AC external supply, 2 A; minimum switching power 1500 VA | Confirm load type, inrush, duty and terminal function in manual |
| Relay R1.3 and R2.4 | Maximum 30 V AC/DC external supply, 2 A; minimum switching power 180 VA | Do not infer a safety function from relay naming |
| Ethernet | 1 × RJ45, 10/100 Mbps, Modbus/TCP, maximum 100 m with shielded twisted pair | Useful for local integration; network security and protocol role remain to be checked |
| RS-485 | 2-wire, one interface, one supported device, 2.4–19.2 kbit/s adjustable | Published device count is one; verify supported meter models/register maps |
| Dimensions | 71.6 × 90 × 61 mm | Preliminary DIN-rail space estimate only; reserve wiring/clearance after mechanical drawing |
| Protection/environment | IP20; −25…60 °C operating; 30–95% RH non-condensing | Must be installed inside a suitably protected enclosure |
| Mounting | DIN rail; any mounting position published | Verify ventilation and spacing in manual |
| Standards listed | IEC 61851-1 | Not, by itself, a complete product conformity or installation approval |

Source: official Phoenix Contact product page, technical-data sections. The catalogue page was inspected on 2026-10-30.

## 3. Interfaces that remain unverified

The following are hard blockers for a controller-specific schematic:

- [ ] Manual revision and exact hardware/firmware compatibility.
- [ ] Terminal-by-terminal diagram and connector identifiers.
- [ ] CP signal generation, measurement, state handling, duty-cycle limits and fault response.
- [ ] PP measurement method, supported cable coding and connector wiring.
- [ ] Exact function of each of the four digital inputs and all relay/digital outputs.
- [ ] Whether the relay output intended for contactor control is V1.2, C1.2 or another documented arrangement.
- [ ] Output isolation, permissible coil load, inrush, suppression and external-driver requirements.
- [ ] Contactor auxiliary feedback mapping and response to welded contacts.
- [ ] RCD type, 6 mA DC detection arrangement, external protection requirements and trip path.
- [ ] Hardwired emergency stop/external inhibit behaviour and de-energisation path.
- [ ] Meter model compatibility, Modbus register map, polling and communications-loss behaviour.
- [ ] Local operation, authorisation and session behaviour during Ethernet/CPMS outage.
- [ ] Access control, password management, firmware update and cybersecurity support policy.
- [ ] Terminal torque, conductor preparation, strip length, ferrule rules and clearances.

## 4. V1 architectural fit

**Positive:** one charging point per controller is a clean fit for a modular per-output architecture. Ethernet and RS-485 are available, and the published DIN footprint is compact.

**Constraints:** there is no integrated modem; only one RS-485 device is listed; and the published relay ratings must not be treated as proof of direct compatibility with the selected contactor coil. The product data do not establish multi-point load balancing or the required local safety interfaces.

**Provisional disposition:** retain as a strong single-output study candidate, not yet selected. For dual/quad products, use one independently validated local controller per output unless Phoenix documents and validates a different topology.

## 5. Supplier questions required to close M1.4A

1. Please provide the current installation/operating manual and terminal assignment for item 2902802, including revision and firmware applicability.
2. Which terminals and electrical ratings are intended for contactor command and auxiliary feedback? Is an interposing relay/driver mandatory?
3. How are CP and PP connected and what are the electrical limits and fault responses?
4. What exact external RCD/DC residual-current protection arrangement is required?
5. Is there a documented hardwired emergency-stop or external inhibit input, and what is its guaranteed response?
6. Which energy meters and Modbus maps are supported over RS-485/TCP?
7. What functions remain local during loss of Ethernet/backend, including authorisation and transaction storage?
8. What are the security/update lifecycle and product availability/support commitments?

## 6. Safety boundary

This document is not a wiring instruction. No contactor, RCD, breaker, cable, terminal, conductor cross-section or torque is selected by this review. PE remains continuous and unswitched. The final design must be checked against the current applicable standards and reviewed by suitably qualified electrical engineering personnel before any mains connection or energisation.

## 7. Exit status

**M1.4A: OPEN.** Product-page extraction is complete; manual/terminal-level evidence and supplier answers are outstanding.

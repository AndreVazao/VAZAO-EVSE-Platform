# VAZÃO EVSE Charger Hardware V1 — Modular Controller Architecture Review (M1.5)

**Status:** ACTIVE ARCHITECTURE CANDIDATE — NOT SELECTED / NOT RELEASED FOR WIRING  
**Reviewed:** 2026-11-02  
**Primary source family:** Phoenix Contact CHARX control modular AC  
**Scope:** common controller architecture for single, dual and quad AC Mode 3 Type 2 products, with future MultiStation expansion.

## 1. Executive finding

The Phoenix Contact CHARX control modular family is now the strongest documented candidate for the VAZÃO EVSE controller architecture study. Unlike the legacy CHARX control advanced 2902802 (one charging point), the modular family explicitly describes a compact per-point controller class and an intelligent Linux/server class, with a published architecture scaling to 48 charging points.

The manufacturer's Portuguese family page describes:
- compact class 1000, 18.8 mm wide;
- intelligent class 3000, 37.6 mm wide;
- autonomous/client operation on class 1000;
- autonomous/client/server operation on class 3000, including management up to 48 charging points;
- integration of socket/cable, contactor, RFID, energy meter, residual-current monitoring, mains-failure unlocking and configurable I/O;
- Linux, web management, dynamic load management, Ethernet, USB-C, OCPP 1.6J, Modbus/TCP, MQTT, REST and OpenVPN on class 3000;
- optional ISO 15118 and optional cellular variants.

Official family page: https://www.phoenixcontact.com/pt-pt/produtos/controladores-de-carregamento-ac

This is a materially better fit for a reusable VAZÃO product family than treating the one-point 2902802 as the sole controller candidate. It remains a candidate, not an approved selection.

## 2. Published system topology — 48 charging points

Phoenix Contact's official product-family material gives a concrete 48-point example:
- one class-3000 controller plus eleven class-1000 controllers form a 12-point cluster using DIN-rail bus connectors;
- the class-3000 controller manages three additional clusters of the same structure;
- total: 48 charging points.

Official source: https://www.phoenixcontact.com/pt-pt/produtos/controladores-de-carregamento-ac  
Manufacturer family overview (PDF): https://www.phoenixcontact.com/assets/2e018b99-3e8a-434f-9728-e02df91e4d29/epaper/1640987_ES_Uebersicht_E-Mobili.pdf

**Interpretation boundary:** this proves the manufacturer's published system-level scaling example. It does not mean one controller alone directly drives 48 outlets. The architecture uses per-point class-1000 controllers and class-3000 cluster/master controller(s). Exact licensing, firmware, bus limits, redundancy, failure isolation and power-allocation behaviour still require the current manual and application review.

## 3. Identified controller references

| Class / item | Manufacturer reference | Published role | Current status |
|---|---|---|---|
| Class 3000 intelligent | CHARX SEC-3150, 1138965 | Linux, server-capable, Ethernet/4G, OCPP 1.6J, Modbus/TCP, MQTT; supports energy meter, RFID and residual-current detection peripherals | Primary master/gateway candidate for evaluation |
| Class 3000 intelligent | CHARX SEC-3100, 1139012 | Similar intelligent controller with cellular communication | Alternative gateway candidate |
| Class 3000 intelligent | CHARX SEC-3050, 1139018 | Intelligent controller without integrated cellular modem | Alternative wired gateway |
| Class 3000 intelligent | CHARX SEC-3000, 1139022 | Intelligent controller, server-capable | Candidate for cluster controller |
| Class 1000 compact | CHARX SEC-1000, 1139034 | Compact per-point controller; autonomous/client operation; bus connector | Candidate local controller per charging point |

Official product-family page: https://www.phoenixcontact.com/pt-pt/produtos/controladores-de-carregamento-ac  
SEC-3150 product page: https://www.phoenixcontact.com/en-us/products/ac-charging-controller-charx-sec-3150-1138965

Do not mix item-number data or assume all options are identical across SEC-3000/3050/3100/3150 variants.

## 4. SEC-3150 published technical data — preliminary extraction

From the manufacturer's product page for item 1138965:
- supply: 12 V DC ±5%, 11.4–12.6 V;
- maximum current: 2 A in stand-alone operation; less than 200 mA no-load without external loads;
- 4 digital inputs, nominal 12 V;
- 4 low-side digital outputs, up to 12 V and 600 mA maximum;
- two Ethernet interfaces, WAN/LAN or LAN/LAN;
- cellular 4G/2G, Micro-SIM, LTE CAT1, antenna socket;
- protocols listed: OCPP 1.6J, Modbus/TCP, MQTT, HTTP, HTTPS;
- RS-485 energy-meter interface;
- separate RS-485 RFID interface;
- CHARX modular system bus via DIN-rail bus connector;
- vehicle interface: IEC 61851-1, ISO 15118 and GB/T 18487;
- residual-current detection interface;
- temperature monitoring: Pt1000 or PTC chain;
- contactor-control interface: floating switch contact, up to 250 V AC / 30 V DC, rated 2 A, interrupting rating up to 1500 VA;
- dimensions: 37.6 × 121 × 85 mm;
- IP20, operating temperature −25…65 °C.

Source: https://www.phoenixcontact.com/en-us/products/ac-charging-controller-charx-sec-3150-1138965

**Caution:** these are product-page ratings, not terminal instructions. They do not establish that the contactor output can directly drive the final selected coil. Confirm load category, inrush, switching life, suppression, isolation, feedback and safety behaviour in the manual and with Phoenix.

## 5. Current manual found

Phoenix Contact publishes the current online user manual:
- Title: *Installing and starting up the charging controller with firmware version 1.9.1*.
- Document: UM EN CHARX SEC, revision 06.
- Applicable listed items: SEC-3150 (1138965), SEC-3100 (1139012), SEC-3050 (1139018), SEC-3000 (1139022), SEC-1000 (1139034).
- Official online manual: https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm
- Manufacturer PDF listed for SEC-3150: um_en_charx_sec_109999_en_09.pdf, revision 09, firmware 1.9.1, SHA-256 753e7579ab961b85245c4b9cde7a1d4e2741cec7205616fa3d370bfeec0eae7a.
- Product drawing listed: pxc_1138965_13_01_CHARX-SEC-3150_2D.pdf, revision/date 2026-09-21, SHA-256 1c3bc226d12ef8633f0867c22e9ac255daa1d6a9b1defec553c068742700e462.

Manual landing page: https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm  
SEC-3150 download/product page: https://www.phoenixcontact.com/en-in/products/ac-charging-controller-charx-sec-3150-1138965

The detailed terminal schedule and full safety review are not yet closed by this summary. Manual sections and drawings must be mapped to each exact item before design freeze.

## 6. Implications for VAZÃO product family

### Single-output wallbox / pedestal
Study one SEC-1000 as the local per-point controller. Decide whether the product requires a separate SEC-3000 class device for local backend, OCPP, advanced load management or gateway duties, or whether SEC-1000 stand-alone/client functions are sufficient.

### Dual-output wallbox / pedestal
Study two independent SEC-1000 controllers for two outputs, coordinated by one class-3000 controller only where required by the product's commercial/connectivity/load-management specification. Verify bus topology and whether the manufacturer's reference architecture supports this exact compact deployment.

### Quad-output pedestal
Study four SEC-1000 local controllers with one class-3000 controller where the chosen functions require it. Do not assume the 48-point example means the four-point assembly can omit local controllers or protection per output.

### MultiStation / charging park
The 48-point cluster architecture is a strong candidate for future site-level expansion. VAZÃO's site controller/CPMS remains responsible for commercial and fleet orchestration; local EVSE controllers retain local charging and safety functions.

## 7. Comparison with earlier candidates

| Candidate | Advantages | Constraints / unresolved |
|---|---|---|
| Phoenix CHARX control advanced 2902802 | Purpose-built, one point, compact, simple single-output study | Legacy one-point design; no modem; one RS-485 device; no demonstrated 48-point architecture in this model |
| Phoenix CHARX control modular SEC-1000 + SEC-3000 family | Explicit per-point + master architecture; 48-point example; OCPP/Modbus/MQTT; RFID/meter/RCM integration options | Higher system complexity; exact cluster rules, BOM, software licensing, terminal-level safety and local offline behaviour need review |
| Bender CC613 | Strong historical DLM, weld-check, PE monitoring, OCPP/PLC feature set | Manufacturer currently marks CC613 discontinued; blocked for new procurement pending supported successor |

## 8. Mandatory evidence gates before M1.5 selection

- [ ] Download and review current revision 1.9.1 manual for exact SEC-1000 and chosen SEC-3000 variant.
- [ ] Map CP/PP, socket lock, contactor command, contactor feedback/weld-check, PE monitoring and RCM connections with page/figure references.
- [ ] Confirm if SEC-1000 alone provides all required local safety responses and which protections remain external.
- [ ] Confirm exact class-3000 master-to-cluster topology, bus connector part numbers, maximum bus length and termination.
- [ ] Confirm master loss, bus failure, network loss and cluster isolation behaviour.
- [ ] Confirm meter models and per-output MID attribution.
- [ ] Confirm RFID interface and secure credential handling.
- [ ] Confirm offline authorisation, local transaction buffering and restart recovery.
- [ ] Confirm firmware update signing, security support lifecycle and CRA statement for each exact item.
- [ ] Obtain Phoenix Contact Portugal quotation, lead time, warranty and product lifecycle confirmation.
- [ ] Compare full installed BOM and cost against other current manufacturers.

## 9. Current disposition

**M1.5: OPEN — preferred architecture candidate identified, not selected.**

The CHARX control modular family is promoted to the leading architecture candidate for detailed study because its published modular topology maps directly to VAZÃO's single/dual/quad roadmap and future charging parks. The 2902802 remains a simpler one-point alternative. CC613 remains blocked from procurement.

No production part numbers, protection ratings, cable sizes, final terminal schedule or wiring are frozen. This document is not an installation instruction and does not authorize fabrication, mains connection or energisation.

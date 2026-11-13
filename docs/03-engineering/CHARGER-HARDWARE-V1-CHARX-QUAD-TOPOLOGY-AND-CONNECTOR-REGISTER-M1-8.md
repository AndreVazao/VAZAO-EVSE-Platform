# VAZÃO EVSE — CHARX Quad Topology and Connector Register (M1.8)

**Status:** DRAFT / MANUFACTURER EVIDENCE REVIEW — NOT A RELEASED WIRING DESIGN  
**Reviewed:** 2026-11-02  
**Scope:** 1-, 2- and 4-output AC EVSE; modular wallbox/pedestal  
**Controller family:** Phoenix Contact CHARX control modular, under evaluation

## 1. Confirmed four-output controller topology

The current Phoenix Contact manufacturer help page states that up to eleven CHARX SEC-1000 controllers can be attached to one CHARX SEC-3xxx controller using the DIN-rail connector supplied with the SEC-3xxx. The attached controllers receive their supply through this connector; the supply may be fed through the SEC-3xxx or one of the attached SEC-1000 controllers. Communication is automatically established and attached controllers are configured/diagnosed through the SEC-3xxx web management.

**Consequent four-output study configuration:**
- 1 × SEC-3xxx (one charging controller plus cluster/server role);
- 3 × SEC-1000 (three additional charging controllers);
- 4 independently configured charging points in one manufacturer-supported cluster arrangement.

This is a manufacturer-supported *controller grouping pattern*, not yet a VAZÃO released electrical design. Confirm that the selected firmware, operating profile, application and local authorisation behaviour support the exact four-output use case before freezing it.

### 1.1 Candidate cluster configurations

| Output count | Controller grouping study | Status |
|---|---|---|
| 1 | 1 × SEC-1000 standalone, or 1 × SEC-3xxx where server/communications functions are required | Candidate; validate no-backend public-access profile |
| 2 | 1 × SEC-3xxx + 1 × SEC-1000 | Supported grouping principle; application/failure validation open |
| 4 | 1 × SEC-3xxx + 3 × SEC-1000 | Directly within published maximum of 11 SEC-1000 attached to one SEC-3xxx |
| 12 | 1 × SEC-3xxx + 11 × SEC-1000 | Manufacturer's maximum single cluster grouping |

Do not interpret the 12-controller limit as a VAZÃO power, protection or thermal approval. It is only the stated controller grouping limit.

### 1.2 Selecting the SEC-3xxx variant

- SEC-3000 (1139022): Ethernet x2, no integrated modem.
- SEC-3100 (1139012): cellular variant.
- SEC-3050 (1139018): ISO/IEC 15118 variant.
- SEC-3150 (1138965): cellular + ISO/IEC 15118 variant.

The base public/no-network configuration should not automatically include cellular hardware. Select SEC-3000 where its validated local/server functions are sufficient. Select a cellular or ISO 15118 variant only where the ordered product profile requires it. Confirm lifecycle, firmware and supplier availability at procurement.

## 2. Bus connector and power-distribution evidence

The manufacturer help page confirms:
- the DIN-rail connector is supplied with the SEC-3xxx;
- up to 11 SEC-1000 modules attach to one SEC-3xxx;
- controller-to-controller communication is established automatically;
- attached modules are powered through the DIN-rail connector;
- the 6 A nominal backplane-bus current limit must not be exceeded;
- controller and connected I/O device current consumption depends on configuration and must be calculated;
- the system prevents simultaneous operation of the connector locking mechanism to avoid overloading the backplane supply.

**Design consequence:** do not add an arbitrary 12 V bus injection point, parallel power source or additional DIN-rail bus connector to the assembly. Follow the exact manufacturer supply-feed arrangement and verify whether any external supply feed is permitted for the selected variant and topology.

The 6 A figure is a hard nominal bus limit, not a recommended operating target. VAZÃO must calculate worst-case demand and margin for the actual mix of SEC-3xxx, SEC-1000, locks and connected I/O. The SEC-1000 and SEC-3000 individual product pages each state up to 2 A in standalone operation; these maxima cannot simply be added as though they were measured cluster consumption, but they demonstrate why a proper worst-case calculation is mandatory.

## 3. Connector group register — manufacturer designations

The official controller overview page identifies these connection groups and signals. This is a functional register, **not a terminal-numbered wiring schedule**. Exact physical terminal numbering, connector positions and mating parts must be transcribed from the current PDF manual and variant-specific drawings.

| Group | Manufacturer designations | Function | VAZÃO treatment |
|---|---|---|---|
| Supply + RFID | 12 V, GND, 12 V, GND, A+, B− | Controller supply and RS-485 RFID reader connection | Reader is optional; supply and RS-485 branch protected and labelled |
| Output | OUT1…OUT4; 12 V supply pins | Digital outputs, high-side or low-side mode | Allocate only after load and fault-state review |
| Input | IN1…IN4; PTC | Digital/analog inputs (0–12 V) and temperature sensor chain | Inputs reserved; unused channels safely terminated/configured |
| Meter | 12 V, GND, A+, B−, RxD, TxD | RS-485 energy meter; RxD/TxD reserved for future use | Meter SKU and per-output attribution must be verified |
| RCM | 12 V, GND, ER1, ER2, TST, NC | Residual-current sensor interface | Sensor selection and RCD coordination remain mandatory design gates |
| Socket | CP, PP, LO−, LO+, LD1, LD2 | Vehicle pilot/proximity, lock actuator and feedback | Dedicated per-output connection; do not connect raw MCU GPIO |
| Contactor — SEC-1000 | C1, C2, NC (2x) | Floating contact for contactor control | Use SEC-1000-specific diagram only |
| Contactor — SEC-3xxx | C1/L, C2/L*, N (2x) | Floating contact; zero-cross detection supply for ISO 15118 variants | Use SEC-3xxx-specific diagram only; never transpose SEC-1000 C1/C2 |
| Ethernet — SEC-3xxx | ETH0, ETH1 (RJ45) | WAN/LAN or LAN/LAN | Optional network wiring; no network needed for local safety |
| USB — SEC-3xxx | USB-C | Configuration/diagnostics; WLAN dongle may be used for app setup | Service/configuration interface; not a permanent network requirement |
| Cellular — SEC-31xx | ANT (SMA), SIM (micro-SIM) | Cellular antenna and SIM | Only populate on cellular variant |
| Local indicators | PWR, APP, LNK, BUS, ERR, CON, CHG | System, application, network, bus and charging state | Map to commissioning/service diagnostics |

## 4. Optional RFID and configuration WLAN — important distinction

The SEC-1000 and SEC-3xxx product pages identify an RS-485 interface for an RFID reader. The physical reader is a connectable peripheral, not a mandatory component. For BASE-PUBLIC, leave the reader and its antenna out, safely terminate/protect the reserved interface and configure the local public-access policy.

Phoenix Contact's free configuration app documentation states:
- the app supports SEC-3000/3050/3100/3150;
- SEC-1000 is supported in combination with one of those controllers;
- the app configures authentication, release modes and load management;
- smartphone connection can use an ad-hoc WLAN adapter, specifically SparkLAN WUBT-239ACN(BT), plugged into the controller USB-C, or an existing WLAN network to which the controller is connected via LAN or WLAN.

**Correction to product terminology:** this documents a WLAN adapter used for commissioning/configuration. It does not prove that CHARX SEC-3000 has an integrated Wi-Fi radio for permanent customer connectivity. Do not list native Wi-Fi as an integrated controller feature. If VAZÃO offers permanent Wi-Fi, evaluate it as a separate optional, approved communications module with its own RF, EMC, power, cybersecurity and enclosure checks.

## 5. Per-output versus shared functions

The manufacturer connector overview shows vehicle/socket, contactor, meter, RCM and RFID interface groups. It does not by itself prove that every one of those interfaces is independently duplicated for each point on every controller variant or that a single RFID reader can serve all outputs.

VAZÃO design rule until further manufacturer confirmation:
- each output has a clearly attributable local CP/PP, contactor control/feedback, protective path and charging state;
- meter measurement is attributable to the correct output and session;
- shared RFID is allowed only after its multi-point authorisation behaviour and offline failure mode are demonstrated;
- a shared SEC-3xxx failure or bus interruption is treated as a potential cluster-level fault until isolation tests prove otherwise.

## 6. Four-output mechanical module layout requirements

The four-output enclosure shall reserve:
1. one controller cluster zone for 1 × SEC-3xxx + 3 × SEC-1000, with the required continuous DIN-rail arrangement;
2. a separate protected power distribution zone;
3. four repeated output power/safety cells;
4. individually labelled meter and RCM interface locations as required by the validated design;
5. optional RFID reader mounting and cable route, left blanked when absent;
6. optional Ethernet/LTE/Wi-Fi equipment zones, blanked when absent;
7. optional HMI/payment mounting and protected harness routes;
8. segregated mains, SELV/PELV and communications ducts;
9. service access for USB-C/configuration and controller indicators;
10. adequate thermal clearance and airflow based on maximum populated configuration.

The SEC-1000 is 18.8 mm wide; SEC-3xxx is 37.6 mm wide; both are 121 mm high and 85 mm deep according to the published product data. These dimensions support a preliminary DIN-rail envelope only; wiring bend radii, accessories, heat dissipation and service clearance still determine the actual panel dimensions.

## 7. Failure containment — mandatory verification before architecture freeze

| Failure injection | Conservative assumption | Required evidence before independence claim |
|---|---|---|
| One SEC-1000 loses supply or fails | Its output may be unavailable; cluster effects unknown | Test one client failure while other points are charging |
| SEC-3xxx loses power/reboots | Treat all cluster points as potentially unavailable | Test all outputs, contactors and recovery |
| DIN-rail bus opens | Treat affected cluster as potentially unavailable | Interrupt bus at defined positions; verify deterministic safe states |
| Backplane overload | Potential damage/unstable behaviour | Worst-case load calculation and protected bench validation |
| RFID reader absent/fails | Policy depends on configured release mode | Test public mode and RFID mode separately |
| Ethernet/LTE absent | Remote functions unavailable; local safety remains | Network-disconnect and cold-start tests |
| One meter loses communication | That point's energy/billing data invalid | Verify fault reporting and no fabricated values |
| Optional module branch short | No propagation into safety core or other outputs | Branch-protected fault injection |
| Shared auxiliary supply fails | Dependent modules/outputs may stop | Branch isolation and restart tests |

## 8. M1.9 closure work

- Obtain manufacturer confirmation of exact four-output controller/firmware application topology and failure behaviour.
- Extract terminal numbers, connector positions, accessory numbers, conductor ranges, strip lengths and torque from current revision 09 PDF (firmware 1.9.1) and variant drawings.
- Confirm exact DIN-rail bus connector is included with the SEC-3xxx and whether any additional accessory is required for the planned rail/cluster.
- Obtain current load data for lock actuators, RFID reader, meter, RCM sensor and optional I/O.
- Calculate 12 V power distribution and 6 A backplane budget for BASE-PUBLIC, RFID and FULL-SERVICE configurations.
- Confirm whether one RFID reader can authorise multiple charging points and how reader loss affects each point.
- Verify per-output meter architecture and register mapping.
- Run failure-injection tests on an instrumented low-voltage bench before any mains-connected prototype.
- Review enclosure, thermal, EMC, IP/IK and electrical protection design with qualified engineering personnel.

## 9. Manufacturer sources

1. Combination of SEC-3xxx and SEC-1000 controllers: https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Combination_of_CHARX_SEC-3xxx_and_-1000_charging_controllers.htm
2. Overview of controller connections and operating indicators: https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Overview_of_the_charging_controller.htm
3. SEC-1000 item 1139034: https://www.phoenixcontact.com/en-pc/products/ac-charging-controller-charx-sec-1000-1139034
4. SEC-3000 item 1139022: https://www.phoenixcontact.com/en-pc/products/ac-charging-controller-charx-sec-3000-1139022
5. Configuration app and WLAN adapter FAQ: https://www.phoenixcontact.com/en-pc/products/ac-charging-controllers/charx-control-modular-app
6. Current manual, firmware 1.9.1, product ID 109999, PDF revision c09 as exposed on SEC-1000 product downloads: https://www.phoenixcontact.com/en-pc/products/ac-charging-controller-charx-sec-1000-1139034#downloads-link-target

## 10. Release status

M1.8 establishes a manufacturer-documented cluster arrangement and connector-group functional register. It does not close exact terminal numbering, connector accessory numbers, electrical protection, 12 V supply design, per-output meter architecture, shared RFID behaviour or fault containment. No final BOM, production wiring, conformity assessment or energisation approval is issued.

**M1.8: PARTIAL — quad controller grouping is documented; VAZÃO electrical implementation and failure isolation remain open.**

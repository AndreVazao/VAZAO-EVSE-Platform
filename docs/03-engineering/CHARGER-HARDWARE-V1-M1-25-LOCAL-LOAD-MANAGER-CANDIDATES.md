# VAZÃO EVSE Charger Hardware V1 — Local Load Manager Candidate Evidence Matrix (M1.25)

**Status:** MARKET / MANUFACTURER EVIDENCE REVIEW — NO SELECTION  
**Date:** 2026-11-25  
**Parent:** M1.24 Local Load Management Interface and Fail-Safe Contract  
**Purpose:** identify credible local energy-manager and multi-output EVSE-control candidates for a dual/quad VAZÃO charger.

## 1. Decision boundary

M1.25 is a shortlist and evidence comparison only. It does not select a controller, meter, CT, protocol, supplier or architecture. Manufacturer feature descriptions are not proof of compatibility with the VAZÃO electrical safety design.

The product must keep three layers separate:
1. **Electrical protection and per-output EVSE safety:** local, deterministic and independent of cloud.
2. **Local energy allocation:** measures site/charger current and sends validated current budgets to each output.
3. **CPMS / commercial management:** user identity, tariffs, billing, remote monitoring and fleet management.

A product that offers OCPP or cloud balancing alone is not automatically acceptable as the local feeder-limit controller.

## 2. Candidate register

| Candidate | Manufacturer evidence found | Local multi-output capability indicated | Main open questions | M1.25 disposition |
|---|---|---|---|---|
| Phoenix Contact CHARX SEC-3000 / SEC-3100 (SEC-3xxx family) | Manufacturer overview lists embedded Linux, load management, connected charging points, Modbus/TCP, MQTT and REST API; SEC-3100 also lists 4G | Yes, product-family documentation explicitly lists load management for connected charging points | Exact supported point count/topology, local meter profiles, fail-safe on sensor/bus loss, current-setpoint limits, licensing/firmware, terminal and safety boundaries | Priority manufacturer clarification candidate |
| Bender CC613 family | Manufacturer DLM documentation describes a designated charging station as DLM Master, external meter via Modbus/Ethernet, and current allocation; current product page lists CC613 variants and external Modbus | Yes, documented DLM Master concept | Exact current order code/lifecycle, supported point count, meter compatibility, update period (docs describe 30 s data), failure/default behavior, licensing, successor status | Technical candidate for evidence review; procurement remains blocked until written lifecycle confirmation |
| Versinetic LinkRay | Manufacturer page describes local controller, external Modbus meter over RS-485/TCP, support for up to 16 connectors and multiple charger makes | Yes, cross-vendor local load balancing is claimed | Exact charger protocol/API compatibility, per-output setpoint semantics, response/fallback timing, certified installation requirements, product variants and commercial licensing | Strong independent-controller candidate; request technical pack |
| aCharge TELECONTROL | Manufacturer page describes local dynamic load management between meter and charge points using Modbus TCP; operates locally without Internet | Yes, local single-stage controller is described | Supported EVSE models/protocol profiles, dual/quad output representation, phase-level algorithm, failure behavior, maximum devices and documentation | Candidate for compact local controller study |
| ABB Terra AC local load-management architecture | ABB manual describes local dynamic multi-charger management through an external local controller and Modbus RS-485/TCP variants, depending on charger variant | Yes, but in ABB Terra ecosystem and specific model/firmware variants | Not evidence of compatibility with VAZÃO controllers; exact controller requirements and local fallback need vendor confirmation | Reference architecture only, not a VAZÃO component selection |

## 3. Source register

### Phoenix Contact — CHARX control modular
- Product family overview: https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Product_overview_of_the_product_family.htm
- Ordering data: https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Ordering_data.htm
- SEC-1000 product page: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034
- Manufacturer documentation separates SEC-1000 from SEC-3xxx: the SEC-1000 is a configurable controller with modular system bus/peripherals; the SEC-3xxx adds embedded Linux and higher-level application functions including load management. Do not infer SEC-3xxx load management from SEC-1000 alone.
- This is a different family from the legacy CHARX control advanced 2902802 reviewed in M1.4A.

### Bender — Dynamic Load Management / CC613
- DLM documentation: https://www.bender.de/docs/charge-controller/Load-Management/DLM/
- CC613 product/variant page: https://www.benderinc.com/products/charge-controller/cc613-charge-controller/
- Manufacturer documentation describes a DLM Master role and external meter interface. A current product page lists CC613 order variants, but this alone does not establish supply continuity, support lifetime or suitability of a particular order code. Keep written lifecycle confirmation as a procurement gate.

### Versinetic — LinkRay
- Product page: https://www.versinetic.com/load-balancing/linkray-controller
- Manufacturer describes local dynamic balancing from an external Modbus meter, with RS-485 or Modbus TCP, up to 16 connectors per LinkRay and multi-unit SiteManager coordination. These are vendor claims to validate in a controlled technical pack and demonstration; they are not VAZÃO acceptance evidence.

### aCharge — TELECONTROL
- Product page: https://www.acharge.de/en/products/acharge-telecontrol/
- Manufacturer describes a local controller that measures building demand and allocates spare capacity to chargers using Modbus TCP without relying on cloud connectivity. Exact supported EVSE models and safety fallback details remain to be obtained.

### ABB — Terra AC load-management reference
- Manufacturer manual: https://library.e.abb.com/public/85a255cf09a04f7b8eaba24bb521eec5/9AKK108466A2151%20Load%20management%20Documentation_Manual_A4_20220906_DIGITAL.pdf
- The manual illustrates local controller + external meter topologies for multiple chargers, including RS-485 and TCP/IP variants, and explicitly notes that the exact setup depends on the technical properties of the controller and charger. Treat as architecture reference only.

## 4. Mandatory technical questionnaire for suppliers

For each candidate, request written answers and controlled documentation for:

1. Number of charging outputs/connectors supported by one local manager.
2. Exact charger-controller models, firmware and communication profiles supported.
3. Whether current limits are sent per output or only as a global aggregate.
4. Setpoint units, range, resolution, update period, acknowledgement and timeout.
5. Whether the manager measures all three phases and handles phase asymmetry.
6. Supported external meters, CT ratios, wiring and Modbus register maps.
7. Behavior when a meter/CT is missing, reversed, saturated or reports implausible values.
8. Behavior on local manager reboot, watchdog timeout and loss of charger communications.
9. Whether each EVSE locally enforces a setpoint and rejects stale commands.
10. Whether the local current limit continues without Internet/CPMS.
11. How a newly connected EV is admitted without overshooting the feeder limit.
12. How the system handles one-phase and three-phase vehicles, output priority and minimum current.
13. Event logs, configuration backup, secure update, access control and cybersecurity maintenance.
14. Product lifecycle, support period, availability, licensing and spare parts.
15. Test evidence, certifications and reference installations for the exact hardware/firmware combination.

## 5. Evaluation scoring model

Score each candidate from 0 to 5 only after evidence is received; use **N/E (not evidenced)** rather than guessing.

- Local autonomy / no-cloud operation — 20%
- Explicit per-output current setpoint and acknowledgement — 15%
- Three-phase measurement and phase-asymmetry handling — 15%
- Defined fail-safe behavior for sensor, controller and bus faults — 20%
- Multi-output scalability and mixed-vendor compatibility — 10%
- Cybersecurity, update and access-control evidence — 5%
- Lifecycle, support and supply continuity — 5%
- Integration effort, serviceability and total cost — 10%

No weighted score is calculated in this revision because the evidence packs are incomplete. A candidate must not pass by compensating for a missing safety-critical capability with a high commercial score.

## 6. VAZÃO architecture implications

- A local manager may be a dedicated DIN-rail device, an energy-management function inside a suitable EVSE controller, or a validated embedded controller in the charger.
- A dedicated manager can preserve controller independence and cross-vendor flexibility, but creates an additional component, communication interface and failure boundary.
- An integrated DLM controller can reduce hardware count, but must prove multi-output coordination, meter integration and degraded-mode behavior.
- The selected architecture must still allow a common incoming feeder or independent feeders as defined in M1.23.
- Each output retains independent electrical protection and local EVSE state control. Load management only allocates available current; it is not a protective device.

## 7. Explicit compatibility warning

The legacy Phoenix Contact EM-CP-PP-ETH 2902802 (CHARX control advanced) from M1.4A is **not demonstrated** to provide multi-output dynamic load management. Do not confuse it with the newer CHARX control modular SEC-3xxx family. The Bender CC613 historical lifecycle uncertainty also remains unresolved despite current online product documentation.

## 8. Disposition and next gate

**M1.25 remains OPEN — supplier evidence gathering.**

No controller or supplier is selected. No meter, CT, protocol, cable, protection, BOM or wiring is released. The next step is to request the technical packs and written answers for Phoenix SEC-3xxx, Bender CC613, Versinetic LinkRay and aCharge TELECONTROL, then build an evidence-backed comparison against M1.24.

The final choice must be proven with a local bench setup and fault-injection tests before the local load-management function can be used to justify a reduced common-feeder design current.

# VAZÃO EVSE Charger Hardware V1 — Modular Auxiliary Distribution Architecture Review (M1.39)

**Status:** ARCHITECTURE REVIEW / NO PSU, RAIL OR DISTRIBUTION TOPOLOGY SELECTED  
**Date:** 2026-11-28  
**Scope:** Auxiliary-power and controller interconnection architecture for Single, Dual, Quad and future MultiStation AC chargers  
**Parent:** M1.33 Auxiliary Power Budget Evidence Matrix; M1.35 Controller Catalog Claims Review; M1.38 Official Manual Source Verification

## 1. Purpose

M1.39 converts the existing auxiliary-load inventory into an architecture comparison using manufacturer-published CHARX control modular information. It identifies what a modular controller/backplane arrangement can and cannot establish for VAZÃO EVSE.

This is an evidence-led architecture review only. It does not select Phoenix Contact hardware, a power supply, rail voltage, fuse, conductor, contactor, protection device or final distribution topology. It does not release wiring or authorize energisation.

## 2. New manufacturer evidence reviewed

The following Phoenix Contact sources were reviewed on 2026-11-28:

| Source ID | Official source | Relevant published information |
|---|---|---|
| M39-S01 | [Connecting and wiring the hardware](https://www.phoenixcontact.com/charx-help/ctrl/ac/um/Section04/4_Connecting_and_wiring_the_hardware.htm) | +12 V DC ±0.6 V controller supply; attached controllers can receive supply through the DIN-rail connector; one controller supply feed can supply attached devices; backplane nominal current 6 A; supply sizing must include connected controllers and I/O devices; load-contactor control and auxiliary-contact monitoring instructions |
| M39-S02 | [Combination of CHARX SEC-3xxx and SEC-1000 controllers](https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Combination_of_CHARX_SEC-3xxx_and_-1000_charging_controllers.htm) | Up to 11 SEC-1000 controllers can be attached to one SEC-3xxx through the DIN-rail connector; attached controllers are supplied through the backplane; nominal backplane current 6 A |
| M39-S03 | [Application overview](https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Application_overview.htm) | Distinguishes stand-alone controllers, SEC-3xxx plus SEC-1000 backplane groups, multiple SEC-3xxx controllers linked over Ethernet, and park-level arrangements |
| M39-S04 | [SEC-1000 product page, item 1139034](https://www.phoenixcontact.com/en-pc/products/ac-charging-controller-charx-sec-1000-1139034) | Catalog: 12 V DC ±5% (11.4–12.6 V), maximum 2 A in stand-alone operation, below 50 mA no-load without external loads, four digital outputs with catalog maximum 600 mA each |
| M39-S05 | [Controller connection overview](https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Overview_of_the_charging_controller.htm) | Controller terminal/interface groups for supply, RFID, outputs, inputs, meter, residual-current detection, vehicle interface and contactor |

These are manufacturer web sources, not a locally archived controlled manual binary. M1.38 remains the record for the unresolved original-PDF custody, checksum and Revision 06 versus Version 09 discrepancy. Page-level statements in M1.39 must be rechecked against the exact controlled manual before schematic release.

## 3. Bounded interpretation of the backplane architecture

The manufacturer describes a modular group in which one controller can feed the attached controllers through the DIN-rail backplane connector. The documented arrangement permits up to 11 SEC-1000 controllers attached to one SEC-3xxx controller. The backplane's stated nominal current-carrying capacity is 6 A.

This supports the existence of a manufacturer-defined shared controller/backplane power domain. It does **not** establish that the same domain is the correct VAZÃO EVSE architecture, or that it can supply every proposed accessory and actuator.

The following restrictions apply:

1. The 6 A value is the nominal current capacity of the specified CHARX backplane bus. It is not a general-purpose 12 V distribution rating for the whole charger.
2. The 6 A value must not be interpreted as available load current after an assumed controller consumption; actual connected device and I/O loads must be totalled from exact source data.
3. The SEC-1000 catalog's maximum 2 A applies to stand-alone operation. It must not be multiplied by the number of controllers to estimate the modular-group demand.
4. The catalog no-load value below 50 mA excludes external loads and is not a representative configured operating current.
5. The four digital outputs' 600 mA maximum is a per-output catalog limit; no aggregate simultaneous-load capability is inferred.
6. The manufacturer's system-side interlock of simultaneous connector-locking actuation is specific to its system. It does not establish that other VAZÃO EVSE loads are mutually exclusive.
7. A backplane communication/power arrangement does not replace independent protection, contactor feedback, residual-current protection, safe-state handling or local output-channel safety boundaries.
8. The up-to-11-controller arrangement is a vendor topology capability, not a VAZÃO EVSE product-count decision and not proof that one SEC-3xxx is suitable as the master for our product.

## 4. Auxiliary distribution architecture alternatives

The following are design alternatives for investigation, not approved designs.

### A — Central auxiliary source with one shared distribution domain

A central auxiliary source feeds a shared distribution assembly for the controller group and shared services. Individual branches serve controller/backplane feeds and selected shared accessories.

**Potential advantages**
- Fewer independent sources and potentially simpler service inventory.
- Shared monitoring and source-level diagnostics.
- May suit a compact Single or a carefully partitioned shared-services compartment.

**Risks and evidence required**
- A single source or distribution fault may disable multiple outputs.
- Branch protection and fault containment must prevent one accessory fault from collapsing safety-critical control power.
- Controller/backplane limits and all external loads must be calculated independently.
- Any accessory not explicitly permitted on the vendor backplane must remain outside it.
- Shared-source failure must lead every affected output to a defined safe state without unintended restart.

### B — Independent auxiliary source per Output Cell

Each Output Cell receives a separately protected auxiliary source or separately isolated auxiliary domain, with shared services supplied by a distinct source.

**Potential advantages**
- Better fault containment between output channels.
- Easier isolation and service of one output without necessarily disabling the others.
- More direct mapping between per-cell safety loads and per-cell protection.

**Risks and evidence required**
- Increased component count, heat, cost, space and maintenance.
- Interactions between sources, protective earth, communications and signal references need engineering review.
- Shared services still require a separately defined supply and fault response.
- No source count or output voltage is selected by this alternative.

### C — Hybrid grouped architecture

A shared source supplies a controller/backplane group or common services, while selected per-cell loads are supplied through independently protected branches or separate auxiliary domains.

**Potential advantages**
- Can balance modularity, serviceability and fault containment.
- Allows common communications/HMI loads to be separated from per-output safety-critical loads.
- May scale from Dual to Quad without forcing every load into one common domain.

**Risks and evidence required**
- More complex allocation, grounding, protection and interface documentation.
- Must explicitly identify which loads are shared, per-cell, redundant or optional.
- Requires a fault-propagation matrix and verification of common-cause failures.

No alternative is preferred at this stage. The architecture decision must follow measured/controlled load evidence and safety analysis, not convenience or the existence of a vendor backplane.

## 5. Product-family allocation model

| Product | Controller/control grouping question | Auxiliary allocation questions still open |
|---|---|---|
| Single / Wallbox 1 | Stand-alone controller or modular controller arrangement | Which loads are per-cell and which are shared? Is a local application/communications module required? |
| Dual / Wallbox 2 | Two independent output controllers or a validated controller group | Does a shared source create an unacceptable common failure? Which services may be shared? |
| Quad pedestal | Four repeatable Output Cells with explicit shared-services boundary | Can the selected controller topology meet all channel requirements? How are auxiliary faults isolated between four outputs? |
| MultiStation / park | Charger-level controllers plus a park-level supervisor | Which loads belong to each charger and which belong to site infrastructure? What happens on loss of park communications or master controller? |

The AC feeder topology (independent feeders or common trunk with protected branches) is independent of the DC auxiliary distribution decision. One must not be inferred from the other.

## 6. Contactor control implications

The manufacturer describes the SEC-1000 contactor interface as a floating switch contact. The controller's contact is a control interface; it is not evidence that the controller supplies the contactor coil power.

The manufacturer wiring instructions describe an externally supplied control voltage and an auxiliary contact routed to a digital input for contactor malfunction monitoring. They also state a same-phase condition between the 12 V supply and contactor control when contactor control is taken from the AC grid, and require the power supply to be dimensioned for the applicable standard-related surge-voltage discharge.

For VAZÃO EVSE this means:

- Keep contactor coil/actuator demand as a separate AUX load, not hidden inside the controller's nominal consumption.
- Record coil voltage, pickup/inrush, holding current, duty, suppression and feedback contact data only after an exact contactor candidate is selected.
- Do not infer the final contactor control voltage or wiring from this generic review.
- Review the isolation boundary, phase relationship, transient/surge conditions and applicable protective requirements before any schematic is released.
- Preserve independent feedback and welded/stuck-contact fault handling for each output channel.

## 7. Fault-containment questions required before selecting a topology

| Fault/event | Required design question |
|---|---|
| Shared auxiliary source failure | Which outputs stop, what state is guaranteed, and how is restart inhibited until checks pass? |
| One Output Cell branch short | Can the fault be isolated without collapsing other channels or the shared controller domain? |
| Backplane overload | How is overload prevented/detected, and what is the documented behavior of every attached controller? |
| Accessory short or inrush | Can RFID, modem, HMI, payment or printer activity disturb safety-critical control power? |
| Contactor coil short/stall | Is the actuator branch protected and can feedback identify failure to operate? |
| Loss of controller/backplane communications | Does each Output Cell independently transition to its defined safe state? |
| Loss of park/master controller | Do charger-level local safety functions remain deterministic and independent? |
| Brownout / source recovery | Is unintended contactor re-energisation prevented? Are controller reset and recovery states defined? |

These are open engineering questions, not claims that a selected device already implements the required response.

## 8. Required evidence to progress to numerical budgeting

The M1.33 AP-01–AP-10 gates remain the governing evidence list. M1.39 adds the following concrete records:

- Exact controller model, hardware revision, firmware and supported backplane topology.
- Controlled manual PDF, internal revision, applicability and local SHA-256 verification.
- Per-controller configured current profile, including external I/O and all attached modules.
- Exact backplane device count and the maximum credible simultaneous load.
- Exact peripheral models and supply profiles for meter, residual-current sensor, RFID, Ethernet/switch, LTE, HMI, payment and printer.
- Contactor coil pickup, holding, inrush and suppression data for each Output Cell.
- Branch protection, isolation and fault-current evidence for each proposed auxiliary domain.
- Operating-mode simultaneity matrix: startup, standby, charging, communications transmit, payment, switching, fault response, service and recovery.
- Thermal/derating data for the final enclosure and source mounting arrangement.
- Qualified review of fault propagation and safe-state behavior.

No numerical source rating or conductor size can be calculated responsibly until these inputs are controlled.

## 9. Design disposition

| Item | M1.39 disposition |
|---|---|
| Shared controller/backplane supply concept | Manufacturer capability documented; VAZÃO applicability not approved |
| Backplane nominal current | 6 A manufacturer-stated limit for the named CHARX backplane only |
| SEC-3xxx + SEC-1000 group size | Up to 11 SEC-1000 attached to one SEC-3xxx per manufacturer documentation |
| Central auxiliary distribution | Alternative A — OPEN |
| Per-Output-Cell auxiliary distribution | Alternative B — OPEN |
| Hybrid distribution | Alternative C — OPEN |
| 12 V auxiliary PSU selection | NOT SELECTED |
| Rail, fuse, conductor and branch sizing | NOT SELECTED |
| Controller selection | OPEN |
| Contactor and coil selection | OPEN |
| Schematic/BOM release | NOT AUTHORISED |
| Bench/mains testing or energisation | NOT CLAIMED / NOT AUTHORISED BY THIS DOCUMENT |

## 10. Next milestone

M1.40 should convert the three alternatives into a traceable decision matrix with explicit per-cell/shared load ownership, fault-containment requirements and evidence status for Single, Dual and Quad. It must not score an option as preferred until the exact controller and peripheral loads, safety boundaries and operating modes are supported by controlled evidence.

No supplier contact, component procurement, physical test, mains test, certification or compliance approval is claimed.

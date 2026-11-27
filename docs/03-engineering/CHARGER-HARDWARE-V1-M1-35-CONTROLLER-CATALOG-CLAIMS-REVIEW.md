# VAZÃO EVSE Charger Hardware V1 — Controller Catalog Claims Review (M1.35)

**Status:** CATALOG CLAIM REVIEW / CONTROLLED MANUAL AND DESIGN VALIDATION OPEN  
**Date:** 2026-11-27  
**Product under review:** Phoenix Contact CHARX SEC-1000, item 1139034  
**Source:** Manufacturer product page: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034

## 1. Purpose

This review separates the published catalog claims into individually bounded statements. It prevents unrelated ratings from being combined into a fictitious controller capacity, and identifies the information needed before these claims may inform the charger architecture or M1.33 auxiliary budget.

This is not a controller selection, design approval, complete datasheet review or permission to energise.

## 2. Catalog claims — bounded interpretation

| Claim ID | Published catalog claim | Interpretation allowed at this stage | Interpretation explicitly NOT allowed | Status |
|---|---|---|---|---|
| CC-01 | Supply 12 V DC ±5%; range 11.4–12.6 V | Catalog supply envelope for the controller | PSU design, rail tolerance under load, transient or brownout acceptance not established | CATALOG ONLY |
| CC-02 | Maximum current consumption 2 A, Stand-alone operation | Published maximum consumption statement for stated operating mode | Cannot be treated as measured profile, steady-only current, or total charger auxiliary load | CATALOG ONLY |
| CC-03 | <50 mA no-load without external loads | Published no-load statement with external-load exclusion | Not a complete standby/idle profile with installed peripherals | CATALOG ONLY |
| CC-04 | Four digital outputs; max 600 mA | Per-output catalog claim requiring conditions and limitations verification | Do not assume 4 × 600 mA simultaneously available, nor that output loads are included/excluded from controller input current | CATALOG ONLY / INTERPRETATION OPEN |
| CC-05 | Contactor control: floating switch contact; catalog voltage/current and interrupting ratings | Contact interface has published switching limits | Does not establish compatibility with any chosen contactor coil, DC inductive switching, suppression, duty, life or isolation design | CATALOG ONLY |
| CC-06 | RS-485 interfaces for energy meter and RFID | Interfaces exist for compatible devices | Does not identify exact compatible peripherals or their supply/load requirements | CATALOG ONLY |
| CC-07 | Residual-current detection interface, 12 V sensor supply | Interface-level catalog statement | Does not select a detection device or establish detection performance, safety integrity or protection architecture | CATALOG ONLY |
| CC-08 | Temperature monitoring, Pt1000/PTC chain | Catalog-supported sensor interface types | Thresholds, wiring, fault handling, sensor compatibility and thermal safety behavior remain unverified | CATALOG ONLY |
| CC-09 | Vehicle interface / locking actuator control, ±12 V statement | Published interface detail | Does not establish plug/socket, lock actuator or output-cell architecture suitability | CATALOG ONLY |
| CC-10 | IP20 and ambient temperature -25 °C to +65 °C | Catalog environmental claims for controller | Does not establish enclosure environmental rating or assembled charger thermal performance | CATALOG ONLY |
| CC-11 | IEC 61851-1 shown in product catalog | Manufacturer catalog association | Does not prove conformity of VAZÃO charger or complete assembly | CATALOG ONLY |

## 3. Auxiliary budget implications

### 3.1 Controller consumption and external loads

The catalog's 2 A maximum and <50 mA no-load statement are recorded as two separate operating-condition claims. The catalog excerpt does not provide a complete time profile, measurement method, peripheral load allocation or simultaneity envelope.

M1.33 must therefore retain:
- Controller input demand as **OPEN pending controlled manual evidence**.
- External peripheral loads as separate inventory rows unless the manual explicitly provides a complete combined consumption profile and states which loads are included.
- Startup/inrush and transient demand as OPEN.
- Rail tolerance, source transient response and reset behavior as OPEN.

### 3.2 Digital output rating

The four-output / 600 mA maximum-per-output catalog statement is not a complete output power budget. Required evidence includes:
- Whether rating is per channel, aggregate, or both, and simultaneous-use limits.
- Thermal derating and ambient conditions.
- Protection against short circuit/overload and behavior after a fault.
- Whether external loads contribute to the stated 2 A controller supply figure.
- Maximum voltage, polarity and permitted load types.
- Whether inductive loads are permitted and the manufacturer's suppression requirements.

Until these conditions are verified, no external load may be assigned a current allowance based solely on the 600 mA catalog line.

### 3.3 Contactor-control interface

The floating contact is not a coil-power source. The controller's contact rating cannot be directly converted into a selected contactor coil rating without controlled manual conditions, load type, DC/AC switching limits, inductive-load rules, external protection and qualified review.

No coil voltage, contactor model, suppression circuit, feedback arrangement or wiring has been selected.

## 4. Claim-to-evidence closure table

| Claim | Required source | Evidence page/section | Status |
|---|---|---|---|
| CC-01 supply envelope | Official controlled manual revision applicable to item 1139034 | OPEN | OPEN |
| CC-02/03 consumption profiles | Official manual, operating conditions, peripherals and profiles | OPEN | OPEN |
| CC-04 output loading | Official manual, channel/aggregate limits, derating and protection | OPEN | OPEN |
| CC-05 contactor switching | Official manual and relevant interface specifications | OPEN | OPEN |
| CC-06 peripheral compatibility | Official compatibility/module documentation | OPEN | OPEN |
| CC-07 residual-current interface | Official interface manual plus selected-device evidence later | OPEN | OPEN |
| CC-08 thermal sensors | Official configuration/wiring/fault documentation | OPEN | OPEN |
| CC-09 locking actuator | Official vehicle-interface documentation and selected hardware evidence | OPEN | OPEN |
| CC-10 environmental | Official manual, installation requirements and assembled enclosure study | OPEN | OPEN |
| CC-11 standards association | Controlled compliance declarations and project applicability review | OPEN | OPEN |

## 5. Design decision gates — intentionally not closed

- **G-CC1:** Exact controller hardware revision and firmware baseline identified.
- **G-CC2:** Official controlled manual obtained, archived and SHA-256 verified.
- **G-CC3:** Consumption figures and operating conditions independently extracted and reviewed.
- **G-CC4:** Output aggregate/per-channel restrictions and fault behavior verified.
- **G-CC5:** Peripheral compatibility and module load evidence complete.
- **G-CC6:** Contactor interface compatibility assessed against chosen coil and protection, when candidates exist.
- **G-CC7:** Qualified review confirms claims are appropriately applied to VAZÃO design.

All gates remain OPEN. No candidate is selected by this review.

## 6. Disposition

M1.35 provides a conservative interpretation of the current manufacturer catalog evidence and a claim-level closure plan. It does not update M1.33 with invented numeric loads, choose the controller, size the auxiliary supply, define rail/fuse/conductor values, freeze a schematic/BOM, or claim tests or energisation.

Next action: obtain the manufacturer controlled manual from the official download channel, retain and hash the original file, and close claims one by one with page/section references. Only then update the auxiliary budget and architecture decision records.

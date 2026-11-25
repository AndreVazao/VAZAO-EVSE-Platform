# VAZÃO EVSE — CHARX Control Modular Manual Interface Extraction (M1.5A)

**Status:** RECOVERED MANUFACTURER-MANUAL EXTRACTION — PARTIAL / DESIGN REVIEW REQUIRED  
**Original review:** 2026-11-02  
**Recovery and reconciliation:** 2026-11-25  
**Manual:** UM EN CHARX SEC, revision 06 / firmware 1.9.1  
**Covered items:** SEC-3150 1138965, SEC-3100 1139012, SEC-3050 1139018, SEC-3000 1139022, SEC-1000 1139034  
**Official manual:** https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm

## 1. Important distinction

This review concerns the newer CHARX control modular family. It does not revise or imply equivalent terminal assignments for the older CHARX control advanced EM-CP-PP-ETH item 2902802.

The official manual landing page identifies revision 06 and firmware 1.9.1 for the listed modular-family items. The manufacturer evidence audit also identifies the exact order codes: SEC-1000 1139034; SEC-3000 1139022; SEC-3050 1139018; SEC-3100 1139012; SEC-3150 1138965. The product-family page and item-specific technical pages must still be checked for exact hardware options and item-specific exceptions. The controlled PDF itself has not yet been archived and independently hashed in the VAZÃO repository; record the exact downloaded file, manufacturer checksum if supplied, retrieval date, applicable hardware revision and firmware before design freeze.

## 2. Per-point interfaces shown in the manufacturer's connection overview

The manufacturer's online manual's "Overview of the charging controller" and "Connecting and wiring the hardware" sections identify the following interfaces:

### Socket / vehicle interface
- CP: Control Pilot according to IEC 61851-1 Annex A.
- PP: Proximity detection according to IEC 61851-1 Annex B.
- LO− / LO+: connector locking actuator control, ±12 V.
- LD1 / LD2: locking feedback signals.

### Contactor interface — SEC-1000
- C1: input for the control voltage.
- C2: switched output to contactor control input.
- The manual describes a floating switch contact arrangement.
- For SEC-1000 and SEC-3x00 installations without ISO 15118 communication, the contactor may be controlled with DC below 30 V or mains voltage below 250 V AC, following the manual's circuit.
- The manual explicitly requires correct phase coordination when using mains voltage for contactor control: the 12 V supply and contactor-control supply must be connected to the same phase.
- The control supply must be dimensioned for the surge voltages required by the applicable standards.

### Contactor interface — SEC-3xxx
- C1/L1: input for contactor-control voltage.
- C2/L1*: switched output to contactor control input.
- For SEC-3x50 variants using ISO 15118 communication, the manual describes mains-voltage contactor control to enable zero-cross detection.
- N terminal is used as shown in the variant-specific manual drawing.

**Do not transpose the SEC-1000 C1/C2 terminal arrangement onto SEC-3xxx C1/L1 and C2/L1*.**

## 3. Contactor monitoring

The manual describes monitoring a load contactor using an auxiliary switch:
- connect a 12 V potential to a free digital input through the auxiliary contact;
- configure the selected input in web management;
- configure whether the auxiliary contact is normally open or normally closed.

The manual's monitoring/event-action material includes "Contactor Failure Detected" and "No Contactor Failure Detected". This is controller diagnostic functionality; the final safety architecture must still verify the required de-energisation path and contactor fault response for the exact configuration.

## 4. Residual-current monitoring connector

The manual overview identifies RCM signals:
- 12 V sensor supply;
- GND;
- ER1 trigger signal, active high (0 V = no error), with internal pull-up to 12 V;
- ER2 trigger signal, 12 V active low (12 V = no error);
- TST test/reset signal (+12 V);
- NC not connected.

The selected residual-current sensor/module and its compatibility must be established from the manufacturer's approved accessory list and exact manual. These signals do not by themselves establish the complete RCD/DC protection arrangement required by the installation.

## 5. DIN-rail system bus and supply

The manual states:
- multiple controllers can be connected using the DIN-rail connector;
- only one charging controller needs to be supplied directly; connected devices are supplied through the DIN-rail connector;
- the backplane bus nominal current limit is 6 A;
- station power-supply sizing must account for the connected controllers and powered I/O devices;
- the maximum current-carrying capacity of the backplane bus must not be exceeded.

This is a key design constraint for dual/quad products: calculate total bus current for the exact module mix and loads; do not size the PSU from the no-load figure alone.

## 6. Charging socket and PE

The manual requires:
- CP and PP to be connected to the controller's Socket connector;
- the charging socket/connector protective conductor to be connected to the controller DIN rail as specified by the manufacturer;
- socket lock and feedback signals to be configured for the exact socket type in web-based management;
- for 3-position locking actuators, the manual specifies a protective circuit for the Lock Detection input (1 kΩ resistor and 3 V Zener diode) as shown in its figure.

The exact manufacturer's drawing and connector variant must be followed. The PE path in the VAZÃO power assembly remains continuous and must not be switched by the normal charging contactor.

## 7. Offline and local operation observations

The manual's configuration section states that SEC-1000 can be configured via a SEC-3xxx controller and then disconnected for separate operation, or configured using a USB CAN adapter and software tool.

For stand-alone SEC-1000, charging release must be configured through Event Actions. When configured with SEC-3xxx, two Event Actions must be created. The manual also documents charging-point states with backend offline but the point remaining available in relevant OCPP operating profiles.

This is evidence that offline operation can be configured in some profiles; it is not proof that every VAZÃO offline authorisation, credential cache, transaction persistence or restart-recovery requirement is met. Those behaviours require explicit tests and configuration review.

## 8. Evidence references

Official manufacturer sources:
1. User manual landing page (revision 06 / firmware 1.9.1): https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm
2. Overview of the charging controller: https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Overview_of_the_charging_controller.htm
3. Connecting and wiring the hardware: https://www.phoenixcontact.com/charx-help/ctrl/ac/um/Section04/4_Connecting_and_wiring_the_hardware.htm
4. Starting up the charging controller: https://www.phoenixcontact.com/charx-help/ctrl/ac/um/Section05/Sec_5_en.htm
5. SEC-3150 product data and drawing: https://www.phoenixcontact.com/en-us/products/ac-charging-controller-charx-sec-3150-1138965
6. SEC-1000 product data and drawing: https://www.phoenixcontact.com/en-us/products/ac-charging-controller-charx-sec-1000-1139034

The online manual sections should be archived/referenced with the released PDF revision in the engineering record before production design freeze. The above references are live manufacturer documentation and may change.

## 9. Open items — not resolved by this extraction

- [ ] Exact terminal numbers/connector positions transcribed from current revision PDF for the exact selected item.
- [ ] Approved contactor types, coil loads, switching category, inrush and suppression.
- [ ] Whether auxiliary contact monitoring provides all required welded-contactor detection for the selected design.
- [ ] Exact RCM accessory and complete external RCD coordination.
- [ ] Exact 12 V PSU sizing for SEC-1000 + SEC-3xxx + RFID + meter + RCM + lock actuator.
- [ ] Backplane bus topology, connector part number, length/cluster rules and current budget for 4-point and 12-point configurations.
- [ ] Master/controller/bus failure behaviour and local point isolation.
- [ ] Firmware configuration, security lifecycle and update policy for each item.
- [ ] Offline authorisation cache, transaction storage and restart recovery tested end-to-end.
- [ ] Exact meter model/register map and MID attribution for each output.

## 10. Safety and release status

This is an engineering evidence extraction, not a wiring release. No protection ratings, cable sizes, contactor MPN, RCD topology or final BOM are selected. The controller's floating contact rating must be checked against the chosen coil and switching duty. The complete installation design and tests must be reviewed by qualified electrical engineering personnel before mains connection or energisation.

**M1.5A: PARTIAL — useful manual evidence obtained; variant-specific design validation remains open.**

## 11. Cluster topology and variant boundaries — reconciliation checkpoint

The manufacturer-family evidence reviewed in the later CHARX SEC audit identifies the following roles and exact order codes:

| Role under study | Exact item | Manufacturer order code | VAZÃO status |
|---|---|---:|---|
| Per-output controller | CHARX SEC-1000 | 1139034 | Local output-controller study candidate |
| Cluster/server controller | CHARX SEC-3000 | 1139022 | Cluster/server study candidate |
| Cluster/server with ISO 15118 | CHARX SEC-3050 | 1139018 | Variant alternative; not selected |
| Cluster/server with cellular | CHARX SEC-3100 | 1139012 | Variant alternative; not selected |
| Cluster/server with cellular + ISO 15118 | CHARX SEC-3150 | 1138965 | Variant alternative; not selected |

The manufacturer help material states that up to 11 SEC-1000 controllers can be connected to one SEC-3xxx using the DIN-rail connector, with a nominal 6 A backplane-bus current limit. This is a manufacturer topology limit, not a VAZÃO-approved configuration. A proposed 4-output cluster (one SEC-3xxx plus three SEC-1000) is within the module-count ceiling but is not proven to fit the 6 A budget once all powered peripherals and simultaneous loads are included.

The shared backplane and server controller are common dependencies. The manufacturer topology does not prove that every output remains independently safe if the SEC-3xxx, bus, common supply or communications fail. The VAZÃO design must define and test safe response for each output under these faults before adopting the cluster.

### 11.1 Contactor interface variant distinction

- SEC-1000 uses C1/C2 as its documented floating contactor-control switch interface.
- SEC-3xxx uses C1/L1 and C2/L1* in the documented arrangement; the N connection shown in the manual is associated with the relevant zero-cross detection arrangement.
- For SEC-3x50 variants with ISO 15118, the manual describes mains-voltage contactor control for zero-cross detection.
- Do not transpose terminal designations or assumptions between SEC-1000 and SEC-3xxx, and do not transpose either onto legacy CHARX control advanced 2902802.

The manufacturer's published floating-contact limits do not establish compatibility with a selected coil. Coil inrush, holding VA, switching category, suppression, phase reference, contact life and fault response remain to be checked against the exact manual and contactor data.

## 12. VAZÃO acceptance gates

- [ ] Archive the exact official UM EN CHARX SEC revision 06 PDF and verify its manufacturer checksum, if published.
- [ ] Confirm physical sample order code, hardware revision and firmware against the manual applicability.
- [ ] Capture exact connector/pin drawings for each selected SEC-1000/SEC-3xxx variant.
- [ ] Calculate worst-case 12 V load budget for controllers, RFID, meter, RCM, locks and all powered I/O.
- [ ] Calculate simultaneous backplane current against the 6 A nominal limit with manufacturer-approved derating and protective arrangements.
- [ ] Validate the SEC-1000 and SEC-3xxx contactor interfaces separately against exact contactor coil data.
- [ ] Define per-output safe state for SEC-3xxx loss, bus interruption, common-supply loss, communications loss, controller restart and recovery.
- [ ] Validate exact RCM accessory, signal polarity, test/reset behavior and complete external RCD coordination.
- [ ] Test offline authorization, transaction persistence and restart recovery with the selected configuration.
- [ ] Confirm firmware/security support lifecycle and product availability in writing.
- [ ] Complete independent electrical review and controlled low-voltage bench validation before any mains-connected test.

## 13. Relationship to later CHARX SEC evidence

M1.5A is an early manual-interface extraction. The later historical document `CHARGER-HARDWARE-V1-M1-28-CHARX-CONTROLLER-MANUFACTURER-EVIDENCE-AUDIT.md` contains a broader manufacturer-source audit of the SEC family, exact variants, published electrical values and further cluster constraints. That later audit depends on intervening milestones and is not being imported or treated as approved by this PR.

M1.5A remains a partial engineering evidence document. It does not supersede the later audit, close the 6 A load budget, establish fault containment, or authorize a controller choice, wiring release, procurement, fabrication or energisation.

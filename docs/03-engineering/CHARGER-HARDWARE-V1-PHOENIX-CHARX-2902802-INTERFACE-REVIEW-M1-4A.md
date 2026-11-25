# VAZÃO EVSE Charger Hardware V1 — Phoenix CHARX 2902802 Interface Review (M1.4A)

**Status:** MANUFACTURER-DOCUMENT REVIEW — PARTIAL / NOT APPROVED FOR WIRING  
**Original review:** 2026-10-30  
**Recovery and evidence refresh:** 2026-11-25  
**Exact catalogue item:** Phoenix Contact EM-CP-PP-ETH, item 2902802  
**Product family:** CHARX control advanced  
**Official product page:** https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802

## 1. Scope and architecture boundary

This milestone reviews only the legacy **CHARX control advanced EM-CP-PP-ETH (2902802)**. It must not be confused with the newer **CHARX control modular SEC family** (SEC-1000 / SEC-3xxx), whose terminals, supply architecture, bus, firmware and cluster behavior are different.

The 2902802 is a one-point AC Mode 3 Type 2 controller. It remains a study candidate for a single output only. This review does not select it for VAZÃO production and does not establish that multiple 2902802 units can form a coordinated dual/quad cluster.

The purpose is to establish the exact manufacturer documents, capture useful interface evidence, expose data conflicts, and list what remains necessary before a controller-specific schematic can be released.

## 2. Controlled manufacturer source register

The official Phoenix Contact product page currently lists the following English manual:

| Field | Manufacturer-published value |
|---|---|
| File | `um_en_ev_charge_control_104924_en_05.pdf` |
| Document/article reference | 104924 |
| Title | UM EN EV CHARGE CONTROL |
| Revision | 05 |
| Applicability stated by manufacturer | EV Charge Control from device revision 10 or higher |
| Language | English |
| Listed file size | 2.4 MB |
| Manufacturer-listed SHA-256 | `6940a22e6bc8cfedacd246a792475bb1ee9d230201b24ac18537964c77a585da` |

The manufacturer also lists the German C05 manual, earlier C03/C04 manuals, application note revision 03, 2D/3D drawings and an EU Declaration of Conformity. The English C05 manual is the reference selected for this review because its stated applicability covers device revision 10 or higher.

**Evidence custody limitation:** the manufacturer download listing and its SHA-256 were checked on 2026-11-25. The PDF itself has not yet been downloaded into the repository's controlled evidence archive and independently hashed by this project. Therefore, the manufacturer checksum is recorded as a source reference, not as a project-verified file hash. Before design freeze, download the file directly from the official Phoenix page, verify the hash, preserve the original bytes, and record retrieval date and device revision.

## 3. Manufacturer-published product data

The current official product page identifies:

| Parameter | Published value | VAZÃO interpretation |
|---|---|---|
| Product | EM-CP-PP-ETH, 2902802 | Exact catalogue item |
| Family | CHARX control advanced | Not the modular SEC family |
| Charging | AC three-phase, Type 2, Mode 3, Case B + C | Broadly matches the V1 AC use case |
| Charging points | 1 | One controller per output unless manufacturer confirms otherwise |
| Operating modes | Stand-alone and client | Does not prove multi-output master/load management |
| Integrated modem | No | Cellular needs a separate communications path |
| Supply | 230 V nominal; 110–240 V AC nominal range; 95–264 V AC operating range | Protected supply design remains open |
| Frequency | 45–65 Hz | Verify exact manual requirements |
| Current consumption | Maximum 40 mA on current product page | Conflicts with values in manual Rev. 05; see Section 6 |
| No-load power | Below 1 W | Do not use alone for PSU sizing |
| Digital inputs | 4; 24 V nominal; OFF −3…5 V; ON 15…30 V; ≤8 mA | Functional assignment and isolation need manual/configuration review |
| Digital outputs | 4; maximum 30 V; 0.2 A total with internal supply; up to 0.6 A/channel with external supply | Not a contactor-coil driver by assumption |
| Relay V1.2 | Maximum 250 V AC / 2 A | Exact intended function and load suitability must be checked |
| Relay C1.2 | Maximum 250 V AC external supply / 2 A; published minimum switching power 1500 VA | Do not infer coil compatibility from the current rating alone |
| Relays R1.3 and R2.4 | Maximum 30 V AC/DC external supply / 2 A; published minimum switching power 180 VA | Function and load type must follow manual |
| Ethernet | 1 × RJ45, 10/100 Mbps, Modbus/TCP; max. 100 m with shielded twisted-pair cable | Local communications option; security and network design remain open |
| RS-485 | 2-wire; one supported device; 2.4–19.2 kbit/s adjustable | Only one serial peripheral is listed |
| Dimensions | 71.6 × 90 × 61 mm (W × H × D) | Confirm against current mechanical drawing and mounting orientation |
| Protection | IP20 | Requires suitable enclosure |
| Operating ambient | −25 °C to +60 °C | Enclosure thermal calculation remains open |
| Mounting | DIN rail | Panel spacing and wiring access remain open |
| Listed standard | IEC 61851-1 | Not a complete VAZÃO product conformity or installation approval |

The product page also lists the optional EM-EV-CLR-12V locking-release module, item 2903246, for release in the event of mains failure. Compatibility, wiring and behavior must be checked in the relevant accessory documentation before any design use.

## 4. Manual Rev. 05 — terminal and functional evidence

The English manual C05 is identified by Phoenix as applicable to device revision 10 or higher. The terminal overview is in Section 3.1 (printed page 14). The following are **manufacturer terminal labels/function groups recorded for further schematic mapping**, not a released VAZÃO terminal schedule:

- Controller supply and reference labels shown in the terminal overview include LD, EN, 24V, ML, XR, GND, ER, LR, VR, GND, CR, 24Va, A, B, PE, N and L.
- The manual separately identifies the PX and CP interface.
- Locking relay outputs are identified as R1–R4.
- Ventilation outputs are identified as V1/V2.
- The contactor relay interface is identified as C1/C2.

The exact connector orientation, pin order, wire entry, electrical domains, isolation boundaries and permissible conductor details must be transcribed directly from the controlled C05 PDF before creating a schematic. This text deliberately does not infer pin numbering from the label list.

### 4.1 Published interface limits from manual C05

- The controller's 24 V output is stated as maximum 100 mA.
- 24Va is used as the supply reference for outputs over the stated 7.5–30 V DC range.
- RS-485 A/B is used for Modbus RTU to an external energy/power meter; the product page lists one supported RS-485 device.
- C1/C2 is the relay interface used to switch the vehicle supply through an external contactor. The manual's relay limit must be compared with the exact contactor coil's inrush, holding VA, switching category and suppression. A generic 2 A rating is not proof of suitability.
- Digital inputs are stated as four 24 V nominal inputs, 8 mA; OFF −3…5 V and ON 15…30 V.
- Four programmable digital outputs are stated up to 30 V and 0.6 A maximum per channel when externally supplied; internal supply total is limited to 0.2 A.
- Relay output groups have different voltage and switching-power limits. Do not treat V1/V2, C1/C2 and R1–R4 as interchangeable.

### 4.2 Contactor feedback example

Manual Section 7.10 (printed page 47) describes monitoring a contactor using an NC auxiliary contact and configurable input XR. The example references Modbus register 390 value 3, register 519 with a 500 ms default delay, and LR configured for the contactor-failure event (register 328 value 35).

This is a manufacturer configuration example, not proof that the VAZÃO design has adequate welded-contactor detection, independent disconnection or a safety-rated feedback chain. The exact circuit and response must be reviewed against the controlled manual and the selected contactor.

### 4.3 Residual-current integration examples

Manual Sections 7.11–7.12 (printed pages 48–49) describe external RCD remote triggering and EV-RCM residual-current monitor integration.

This does not, by itself, define or approve the complete VAZÃO protective architecture. The required RCD type, DC residual-current detection, trip path, coordination, fault response and installation requirements must be selected and reviewed as a complete system. No protection device is selected by M1.4A.

## 5. Interface suitability for the VAZÃO modular charger

| VAZÃO requirement | 2902802 evidence | Current disposition |
|---|---|---|
| Local control of one AC output | One charging point, Type 2 Mode 3 | Plausible single-output study candidate |
| Dual/quad local control | One point per controller; no proven multi-point master function | Not established |
| Master/slave load management | Stand-alone/client modes only in current product data | Not established; do not assume |
| CP/PP | Dedicated PX/CP interface in manual | Detailed electrical mapping still requires controlled PDF review |
| Contactor command | C1/C2 relay interface | Coil compatibility and fault behavior open |
| Contactor feedback | XR + NC auxiliary example | VAZÃO safety response not approved |
| RCD/DC protection | External RCD/EV-RCM examples | Complete protection coordination open |
| Metering | One RS-485 device; Modbus RTU | Exact meter profile/register map and MID needs open |
| CPMS/network | Ethernet Modbus/TCP; no modem | CPMS/OCPP capability is not established by these data |
| Offline authorization | Stand-alone mode exists | Credential, transaction, restart and fault behavior not proven |
| RFID/HMI/payment | No evidence of integrated modules in this product review | External architecture required; no compatibility assumed |
| TestStation | Interfaces can inform a future test adapter | Test method and acceptance limits must be developed separately |

**Important architecture distinction:** do not carry forward any CHARX SEC-1000/SEC-3xxx assumptions into this 2902802 review. In particular, do not assume the modular SEC backplane, 12 V architecture, controller cluster count, terminal designations or server/client behavior apply to CHARX control advanced.

## 6. Unresolved manufacturer-data discrepancy

The current Phoenix Contact product page lists maximum current consumption as **40 mA**. The C05 manual reviewed in the earlier document extraction lists **70 mA at 230 V** and **140 mA at 110 V**.

These values are materially different. The product page may reflect a changed measurement basis, device revision or updated technical data, but no explanation is established here.

**Gate:** do not select a PSU, fuse, branch protection or thermal budget using either value until Phoenix Contact confirms in writing:
1. the exact device revision to which each value applies;
2. whether the values are maximum, typical, startup or steady-state;
3. the required external supply protection and inrush assumptions;
4. which value is valid for the current orderable 2902802.

## 7. Supplier clarification request

Request a written response from Phoenix Contact for exact item 2902802 and the physical device revision under consideration:

1. Confirm that manual 104924 C05 applies to the supplied device revision and provide the controlled installation manual/terminal drawing.
2. Reconcile the product-page 40 mA maximum with the C05 manual's 70 mA at 230 V / 140 mA at 110 V.
3. Confirm C1/C2 relay switching limits, permissible contactor coil inrush/holding load, suppression requirements and whether an interposing relay/driver is required.
4. Confirm the exact XR contactor-feedback circuit and the documented response to welded contactor or unexpected auxiliary feedback.
5. Confirm the supported RCD remote-trip and EV-RCM accessory variants, including the complete required protective arrangement.
6. Confirm supported meter models/configuration files and Modbus register maps over RS-485.
7. Confirm stand-alone/client behavior during network loss, including local authorization and transaction persistence.
8. Confirm product lifecycle, availability, firmware maintenance and security-support commitments.

## 8. Open acceptance checklist

- [ ] Obtain the exact physical sample order number, hardware revision and firmware/configuration.
- [ ] Download the official English C05 PDF directly from Phoenix Contact.
- [ ] Verify the downloaded PDF SHA-256 against the manufacturer-listed value above.
- [ ] Archive the original PDF, product page snapshot, 2D drawing and application note under the M1.25 evidence-custody rules.
- [ ] Transcribe the complete terminal map and connector views with manual page references.
- [ ] Resolve the 40 mA versus 70/140 mA supply-current discrepancy in writing.
- [ ] Validate contactor coil compatibility and contactor-feedback behavior for the exact selected parts.
- [ ] Validate the complete RCD/DC residual-current protection and trip architecture.
- [ ] Confirm meter model, register map, measurement accuracy and MID requirements where billing applies.
- [ ] Define offline authorization, transaction persistence and restart-recovery tests.
- [ ] Perform an independent engineering review before any controller-specific schematic.
- [ ] Perform controlled low-voltage bench verification before any mains-connected prototype test.

## 9. Disposition and exit status

**M1.4A remains OPEN — documentary extraction only.**

The 2902802 remains a candidate for further single-output study, not a selected VAZÃO controller. Its product-page data and manual C05 provide useful interface evidence, but the supply-current discrepancy, controlled-PDF custody, exact terminal map, coil compatibility, residual-current protection and offline behavior remain open.

This milestone does not authorize procurement, production, wiring, fabrication, mains connection, energisation, installation or certification.


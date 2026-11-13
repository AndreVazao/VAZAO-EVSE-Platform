# VAZÃO EVSE Charger Hardware V1 — Controller Interface Review (M1.3)

**Status:** ENGINEERING REVIEW MATRIX — no controller selected or wiring released  
**Date:** 2026-10-30  
**Scope:** single-output AC Mode 3 Type 2 reference prototype; comparison of Phoenix Contact CHARX 2902802 and Bender CC613 family  
**Parent:** [M1.1 Component Selection Gate](CHARGER-HARDWARE-V1-COMPONENT-SELECTION-GATE.md) and [M1.2 Candidate Shortlist](CHARGER-HARDWARE-V1-COMPONENT-CANDIDATES-M1-2.md)

## 1. Decision at this gate

No final controller choice is made in M1.3. The available product-family descriptions establish that both are credible EVSE-controller candidates, but they do not, by themselves, provide enough verified terminal-level information to release a schematic or mounting plate.

The single-output prototype should be evaluated first against the Phoenix Contact 2902802. The Bender CC613 remains a parallel architecture candidate for multi-point products and load management. This is a prioritisation for evidence gathering, not a technical acceptance.

## 2. Candidate comparison

| Review item | Phoenix Contact CHARX 2902802 | Bender CC613 family | M1.3 disposition |
|---|---|---|---|
| Intended use | Manufacturer describes a one-point AC Mode 3 Type 2 controller | Manufacturer describes AC Mode 3 charge control | Both remain candidates |
| Single-output prototype fit | Directly aligned to one charging point | Must confirm exact variant and deployment topology | Phoenix first for detailed single-point study |
| Multi-point / Master-Slave | Do not assume this model provides a multi-point master | Manufacturer documents configurable Master/Slave and dynamic load management | CC613 is the current multi-point study candidate |
| CP / PP implementation | Obtain exact terminal diagram, supported states, limits and fault behaviour | Obtain exact terminal diagram, supported states, limits and fault behaviour | No CP/PP wiring can be inferred from product page |
| Contactor control | Confirm output type, voltage/current ratings, suppression and whether an external driver is required | Confirm output type, voltage/current ratings, suppression and whether an external driver is required | Open — must match selected contactor coil |
| Contactor feedback | Confirm dedicated input, electrical levels, diagnostics and welded-contact response | Confirm dedicated input, electrical levels, diagnostics and welded-contact response | Mandatory evidence before schematic freeze |
| RCD / DC residual-current | Confirm supported external protection arrangement and required detection device | Manufacturer documentation describes residual DC monitoring arrangement and external Type A RCD requirement for the relevant configuration | Do not transfer Bender protection assumptions to Phoenix |
| Emergency stop / hardwired inhibit | Confirm documented input and de-energisation behaviour; otherwise define independent safety chain | Confirm documented input and de-energisation behaviour; otherwise define independent safety chain | Must be validated in the exact manual |
| Meter interface | Confirm supported meter protocol and integration options | Confirm supported meter protocol and integration options | EM340 Modbus RTU remains a candidate, not yet validated against either controller |
| CPMS / OCPP | Confirm supported protocol versions, licensing, firmware and backend limitations | Manufacturer family information lists OCPP 1.5/1.6; verify exact variant and licensing | No OCPP compatibility claim until exact variant evidence |
| Offline behaviour | Confirm local charging behaviour, authorisation cache and fault handling during network loss | Confirm local charging behaviour, authorisation cache and fault handling during network loss | Local safety must remain independent of cloud |
| Firmware / cybersecurity | Obtain update, signing, access-control and vulnerability-support policy | Obtain update, signing, access-control and vulnerability-support policy | Supplier evidence required |
| Mechanical | Obtain dimensions, mounting orientation, terminal access and clearances | Obtain dimensions, mounting orientation, terminal access and clearances | No physical panel dimensions frozen |

## 3. Manufacturer evidence register

The following documents must be retrieved and archived with revision/date before acceptance:

### Phoenix Contact CHARX control advanced EM-CP-PP-ETH, 2902802
- Official product page: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802
- Required: current installation manual, data sheet, terminal assignment, application note/reference schematic, firmware/protocol statement, declaration/certificates and mechanical drawing.
- Confirm: exact CP/PP behaviour; contactor output ratings; feedback inputs; residual-current protection interface; hardwired inhibit; supply requirements; Ethernet/protocol support; offline modes.

### Bender CC613
- Official product page: https://www.bender.de/en/products/charge-controller/cc613-charge-controller/
- Manufacturer manual: https://www.bender.es/fileadmin/content/Products/m/e/CC613_D00381_M_XXEN.pdf
- Required: exact order code and option matrix, current manual revision, terminal assignment, Master/Slave wiring, point-count limits, meter interface, protection topology, mechanical drawing and firmware/licensing details.
- Confirm: whether one controller maps to one output or supports another topology; number of controllers required for dual/quad; master communications; failure behaviour if the master or bus fails.

## 4. Mandatory terminal-level acceptance checklist

Do not create a production or energisation wiring schedule until every applicable item has a document reference and page/section:

- [ ] Controller exact order code and hardware revision.
- [ ] Supply voltage, tolerance, power and protective requirements.
- [ ] CP output waveform/voltage limits and CP measurement input characteristics.
- [ ] PP/cable coding measurement range and connector implementation.
- [ ] Contactor command output electrical type, ratings and isolation.
- [ ] Contactor auxiliary feedback input type, thresholds and diagnostic behaviour.
- [ ] Response to welded contactor / unexpected feedback.
- [ ] RCD and DC residual-current detection architecture and external-device requirements.
- [ ] Emergency stop / external inhibit input and de-energisation path.
- [ ] Temperature inputs, sensor type and fault response if used.
- [ ] Meter protocol, addressing, update rate and failure behaviour.
- [ ] Ethernet/network isolation, protocols, certificates and update security.
- [ ] Offline authorisation and local transaction storage limits.
- [ ] Terminal torque, conductor range, strip length and permitted ferrules.
- [ ] Environmental limits, mounting orientation, dimensions and clearances.

## 5. Prototype architecture — provisional interface boundary

The following is a functional boundary only. It deliberately does not assign terminal numbers, voltage levels, conductor sizes or component ratings.

1. **Mains power domain:** incoming supply → coordinated protective devices → power switching element → energy meter → Type 2 output. The final order and protective topology must follow the selected design and applicable requirements.
2. **Local EVSE domain:** controller → CP/PP interface → vehicle state evaluation → charge-permission logic.
3. **Switching control domain:** controller command → correctly rated/isolated coil driver if required → contactor coil; auxiliary contact/diagnostic feedback returns to the controller as documented by the manufacturer.
4. **Residual-current domain:** RCD and DC residual-current detection are selected as one coordinated protective architecture; no generic controller input is assumed to replace a required protective device.
5. **Measurement domain:** per-output meter → local controller or communications gateway → session record/CPMS. Metering failure must have a defined safe and commercial response.
6. **Communications domain:** Ethernet/Wi-Fi/LTE and CPMS are outside the primary local electrical safety chain.

## 6. Design rules retained

- PE remains continuous and is never switched by the normal charging contactor.
- CP/PP must not connect directly to general-purpose MCU GPIO.
- Cloud connectivity, RFID reader and HMI faults must not defeat local electrical protection.
- The Master may allocate available power but must not replace per-output local EVSE safety.
- Do not parallel or combine Phoenix and Bender terminal assumptions.
- Do not infer contactor coil voltage, relay capacity, RCD topology, breaker rating, conductor size or terminal torque from a nominal 32 A output.
- Any final mains-connected assembly and verification must be performed/reviewed by suitably qualified personnel.

## 7. M1.3 exit criteria

M1.3 can close only when:
1. The exact controller variants are confirmed.
2. Current manufacturer manuals and terminal drawings are archived.
3. Every mandatory interface above is mapped to a cited manual page/section.
4. Controller-specific single-line and control schematics are reviewed.
5. Protection coordination and contactor feedback/de-energisation paths are independently reviewed.
6. The selected controller's physical dimensions and clearances are known.

Until then, M1.3 remains **OPEN — evidence gathering**.

## 8. Next engineering sequence

- M1.4A: Phoenix-specific terminal and interface extraction.
- M1.4B: Bender-specific terminal and Master/Slave extraction.
- M1.5: compare completed evidence matrices and select the preferred V1 prototype controller.
- M1.6: produce controller-specific schematic, terminal schedule and dimensioned DIN-rail layout.
- M1.7: update BOM with exact order codes, quantities, alternatives and supplier quotations.

# VAZÃO EVSE Charger Hardware V1 — Bender CC613 Interface Review (M1.4B)

**Status:** HISTORICAL TECHNICAL EXTRACTION — NOT A CURRENT PROCUREMENT RECOMMENDATION  
**Reviewed:** 2026-10-30  
**Document:** Bender CC613 operating manual, D00381_07_M_XXEN/02.2023  
**Official manual:** https://www.bender.es/fileadmin/content/Products/m/e/CC613_D00381_M_XXEN.pdf  
**Official product page:** https://www.bender.de/en/products/charge-controller/cc613-charge-controller/

## 1. Procurement status — critical finding

The manufacturer's current CC613 product page displays a notice that the requested device refers to a discontinued product. This changes the M1.2 shortlist status: **CC613 is removed from the active procurement shortlist pending written confirmation of stock, support, warranty/spares and a manufacturer-designated successor.**

The manual remains valuable as a technical reference for architecture and interface requirements. Its specifications must not be transferred to another Bender model or successor without a fresh variant-specific review.

## 2. Manual identity and scope

- Manual title: CC613 charge controller.
- Document identifier/revision: D00381_07_M_XXEN/02.2023.
- The manual states it is intended for qualified electrical engineering/electronics personnel (printed page 4, section 1.1).
- It covers variants with different options; multiple features and I/O are explicitly variant-dependent.

## 3. Confirmed functions and topology

| Subject | Manual evidence | Engineering interpretation |
|---|---|---|
| Mode 3 | Section 2.2, printed page 8 | Controller designed for IEC 61851-1 Mode 3 |
| Master/Slave | Section 2.2, printed page 8 | Configurable master/slave operation exists, but exact topology is variant/configuration dependent |
| Two-point example | Section 2.2, printed page 8 | Manual describes a charging station with two points: one gateway controller with 4G and one slave without 4G |
| Dynamic load management | Section 2.2, printed page 8 | Available power is distributed across charging points and signalled to vehicles |
| Residual DC monitoring | Section 2.2, printed page 8 | The documented RDC-M arrangement requires an external Type A RCD |
| Current rating envelope | Section 2.2, printed page 8 | Manual says single- or three-phase systems up to 80 A; this is not a substitute for installation/protection design |
| OCPP | Section 2.2, printed page 8 | OCPP 1.5 and 1.6 JSON/SOAP are listed; confirm exact variant, firmware and backend compatibility |
| Metering | Section 2.2, printed page 8 | Modbus TCP and RTU meter interfaces are listed, including external Modbus interface for a second meter |
| Connectivity | Section 2.2, printed pages 8–9 | Ethernet and modem options; 4G/3G/2G listed for integrated modem variants |
| CP/PP | Section 2.2, printed page 8 | Control Pilot and Proximity Pilot communication supported |
| Temperature | Section 2.2, printed page 9 | Internal temperature sensor can reduce charging current depending on ambient temperature |
| ISO 15118 PLC | Section 2.2, printed page 9 | PLC features listed; exact option and use case require variant confirmation |

**Important topology limit:** the manual's explicit example is a two-point arrangement using two controllers. It does not prove that one CC613 directly controls four independent outputs. A quad design must not be based on an assumed four-point capability.

## 4. Safety and commissioning observations

- The manual warns that default local access credentials must be changed (section 2, printed page 8). Any surviving deployment would require secure commissioning and credential lifecycle controls.
- The manual instructs users to de-energise the system before installation or work on connections (section 1.9, printed page 7).
- The RDC-M is not described as a universal replacement for the installation's RCD: the manual explicitly notes an external Type A RCD is required for the documented arrangement (section 2.2, printed page 8).
- The controller's emergency opener is described for actuator control (locking/unlocking) and monitoring of 12 V supply; do not misinterpret it as the station's emergency-stop safety chain.
- Local safety and contactor de-energisation must remain effective independently of backend connectivity.

## 5. Terminal/interface evidence map

The manual's table of contents identifies the detailed sections below. The exact wiring diagrams must be transcribed only against the selected order-code variant; no generic terminal schedule is released by this document.

| Manual section | Printed page(s) | Evidence to extract in a later variant-specific design |
|---|---:|---|
| 4.1 Connection plug connections | 13 | Connector identities and pin numbering |
| 4.2 Wiring diagram | 14–16 | Variant-specific full connection diagram |
| 4.3.1 Master/Slave connection | 17 | Bus wiring, addressing, termination and topology |
| 4.3.2 Interfaces | 17 | Ethernet/USB/serial interface details |
| 4.3.3 Power contactor connection | 17–18 | Coil command, ratings and feedback wiring |
| 4.3.4 PE monitoring | 19 | PE monitor connection and fault response |
| 4.3.5 CP and PP connections | 20 | CP/PP wiring and limits |
| 4.3.6 I/O extension | 21 | Variant-dependent additional I/O |
| 4.3.7 Emergency opener | 21 | Lock actuator connection and behaviour |
| 4.3.8 RDC-M | 21 | DC residual current module connection |
| 4.3.9 Modbus meters | 21 | Meter connection and supported interface |
| 4.3.10 Gateway variants with modem | 21 | Gateway/modem variant details |

## 6. Selected electrical data — variant-dependent

The manufacturer's technical-data document D00381_05_D_XXEN/03.2023 lists the following. These values must be checked against the exact variant and its manual before any design use:

- Supply at terminal B (0CV, +12CV): nominal 12 V DC; operating range 11.4–12.6 V; maximum nominal current 750 mA (400 mA without USB load).
- Optocoupler input at terminal J: 11.4–25.2 V DC; 2.3–6.4 mA.
- Weld-check input at terminal H: 180–277 V AC; 0.6–1.3 mA.
- Relay at terminal J (13/14): 24 V DC rated operational voltage, 1 A rated operational current.
- Contactor switching relay at terminal H (23/24): 230 V AC rated operational voltage, 4 A rated operational current.
- Operating temperature: −30…70 °C.
- IP20; DIN rail IEC 60715.
- Terminal blocks B/J: push-wire; 0.2–1.5 mm² rigid/flexible; ferrule ranges differ; 10 mm strip length.

These are transcribed from the manufacturer technical-data PDF surfaced on the official product page. They are not a terminal wiring instruction. In particular, the 230 V AC relay rating must not be interpreted as approval to drive any arbitrary contactor coil.

## 7. VAZÃO EVSE disposition

- **Architecture learning:** retain the manual as a reference for two-point Master/Slave, dynamic load management, Modbus metering and the RDC-M + external Type A RCD concept.
- **Procurement:** blocked because the manufacturer marks CC613 discontinued.
- **Design freeze:** prohibited until exact order code, variant-specific diagrams and successor/support status are confirmed.
- **Quad output:** no claim that one controller supports four independent charging points.

## 8. Supplier clarification / successor request

Request from Bender:
1. Official successor product and migration guide for CC613.
2. Written confirmation of end-of-sale, end-of-support, spares and warranty dates.
3. Whether the successor supports two or more independently controlled Type 2 outputs, with exact maximum point count.
4. Current manual, data sheet, order-code/variant matrix and terminal diagrams.
5. Updated Master/Slave topology and failure behaviour if master, bus or gateway is lost.
6. Current OCPP versions, security/update lifecycle and supported meter list.
7. RDC-M and external RCD requirements for the successor.

## 9. Exit status

**M1.4B: PARTIAL / PROCUREMENT BLOCKED.** Historical manual extraction is recorded; current availability and successor confirmation are outstanding. CC613 is not eligible for V1 selection on present evidence.

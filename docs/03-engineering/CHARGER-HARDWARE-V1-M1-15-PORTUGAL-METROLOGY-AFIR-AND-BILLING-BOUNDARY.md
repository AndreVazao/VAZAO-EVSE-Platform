# VAZÃO EVSE — Charger Hardware V1 — M1.15: Portugal metrology, AFIR and billing boundary

**Status:** PARTIAL — Portuguese legal framework and public-charging obligations mapped; no legal opinion, meter approval or billing release.  
**Date:** 2026-11-10  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.13 and M1.14.

## 1. Executive decision

M1.15 separates four matters that must not be conflated:

1. **Meter product conformity:** the meter's MID / EU type-examination and conformity-assessment documentation.
2. **National legal metrology:** the Portuguese legal-control regime and competent national institution.
3. **EVSE/OCMF integration:** whether the exact meter firmware, CHARX firmware and backend preserve and verify signed transaction records.
4. **Commercial charging service:** operator, payment, price disclosure, invoicing, consumer and AFIR obligations.

A MID label, a CHARX selectable meter profile or an OCMF-compatible entry does not, by itself, prove all four.

**Current engineering direction:**
- EMH iML e-moc remains the leading *prototype* candidate for a CHARX OCMF-capable metering chain because Phoenix lists its exact model/firmware/OCMF version and EMH publishes charging-specific MID/national-approval and signed-record functions.
- Phoenix EEM-XM355 1674509 remains a strong *point measurement/load-management* candidate, as the current CHARX 1.9.1 configuration lists it, but it is not in the current CHARX OCMF legal-metrology table.
- Neither candidate is approved for Portuguese commercial billing.
- For the 22 kW AC reference point (below 50 kW), AFIR's public-access rules require ad-hoc access and transparent price-component disclosure; the under-50-kW price components are ordered kWh, minute, session, then other components. For public points deployed from 13 April 2024, AFIR permits a secure internet-connected payment device such as a specific QR-code payment route below 50 kW. Payment does not need to be implemented inside the EVSE safety controller.

## 2. Portuguese legal-metrology framework

### 2.1 Decree-Law 29/2022

Official Diário da República text:  
https://diariodarepublica.pt/dr/detalhe/decreto-lei/29-2022-181756966

Decree-Law 29/2022 of 7 April establishes Portugal's general regime for legal metrological control of measurement methods and instruments. Article 13 identifies the **Instituto Português da Qualidade (IPQ, I.P.)** as the National Metrology Institution, responsible for ensuring and managing the legal-metrology control system and coordinating/qualifying competent entities.

Engineering consequences:
- IPQ is the first national authority to consult for the legal-metrology interpretation and applicable control path.
- Do not attribute primary legal-metrology authority to DGEG merely because DGEG has energy-sector responsibilities.
- The applicability of the relevant instrument category and conformity route must be confirmed for the exact EV charging transaction and meter configuration.
- Any required initial/periodic verification, seals, conformity assessment, approved configuration or competent-body involvement must be established from the applicable instrument-specific rules and IPQ guidance.

This document does **not** conclude that a meter with a CE/MID mark automatically satisfies every Portuguese obligation for every charging business model. Obtain a written IPQ or qualified legal-metrology assessment before commercial release.

### 2.2 MID scope and meter certificate evidence

The relevant European instrument framework for active electrical energy meters is Directive 2014/32/EU (MID), Annex MI-003. For the selected meter, obtain the complete and current:
- EU-type examination certificate (or applicable conformity assessment documentation).
- Declaration of conformity and notified-body identification where applicable.
- Module / production-conformity route (for example, the applicable B+D, F or H1 route as stated by the manufacturer; do not assume one).
- Exact type designation, hardware revision, firmware, current/voltage range, wiring topology, accuracy class and environmental limits covered.
- Installation, sealing, parameter-protection and maintenance requirements.
- Evidence that the meter is approved for the intended direct-connected or CT-operated topology and the exact CTs, if any.

The EMH iML e-moc manufacturer page describes MID and national approval, but the complete certificate package and exact scope for the intended installation have not yet been received. Treat the claim as product-level evidence only until certificates are reviewed.

The Phoenix EEM-XM355 product MID statement and its CHARX selectable point-meter profile are not evidence of signed OCMF support. Conversely, a meter's presence in the CHARX OCMF list is not by itself proof that the complete Portuguese legal and commercial chain is compliant.

## 3. AFIR — public access, payment and pricing for the 22 kW product

Official consolidated Regulation (EU) 2023/1804, Article 5:  
https://eur-lex.europa.eu/eli/reg/2023/1804/2026-01-08

European Commission AFIR questions and answers:  
https://transport.ec.europa.eu/transport-themes/clean-transport/alternative-fuels-sustainable-mobility-europe/alternative-fuels-infrastructure/questions-and-answers-regulation-deployment-alternative-fuels-infrastructure-eu-20231804_en

AFIR Article 5 applies to publicly accessible recharging points, except where a provision expressly has a narrower scope.

### 3.1 Ad-hoc access and payment

- Operators of publicly accessible points must offer ad-hoc charging.
- For publicly accessible points deployed from 13 April 2024, ad-hoc charging must be possible using a widely used payment instrument through an electronic payment terminal/device.
- Article 5(1) permits payment-card readers, contactless card-capable devices, and, for points below 50 kW, secure internet-connected payment devices such as a specific QR-code payment route.
- A payment terminal/device may serve multiple points in a charging pool.
- Automatic RFID/app authentication cannot remove the end user's right to choose ad-hoc charging or another contract-based option.

**V1 architecture decision:** payment is an optional service module / external payment integration. The EVSE local safety controller must never depend on the payment provider, internet connection or payment terminal to perform CP/PP safety, contactor control, residual-current monitoring or safe stop. A payment failure means no new paid session is authorised; an active session follows the local safe-stop and transaction-reconciliation policy.

### 3.2 Pricing below 50 kW

For publicly accessible points below 50 kW, the operator must make all ad-hoc price components clearly and easily available before the session starts, in this order:
1. Price per kWh.
2. Price per minute.
3. Price per session.
4. Any other applicable price component.

The rule applies to all sub-50-kW public points from the application date of AFIR (13 April 2024), as clarified by the Commission Q&A. The 22 kW AC reference point falls below 50 kW.

Do not use the simplified “50 kW or more” price-display rule for this 22 kW product. Do not assume that a per-kWh-only display is sufficient below 50 kW when other price components apply.

AFIR requires prices to be reasonable, comparable, transparent and non-discriminatory. The European Commission Q&A clarifies that “reasonable” is assessed case by case and is informed by costs plus a reasonable profit margin; it does not provide a universal numeric cap.

### 3.3 Digital connectivity and smart charging

AFIR Article 5 requires publicly accessible points to be digitally connected (deadline 14 October 2024) and points built after 13 April 2024 or renovated after 14 October 2024 to be capable of smart recharging.

This is an operator/product-system requirement, not a reason to make the local electrical safety function cloud-dependent. The design must distinguish:
- Local electrical safety and charging control.
- Optional network/backend connectivity and smart charging.
- Payment and ad-hoc user journey.
- Signed metering/transaction records where legally required.

### 3.4 Applicability boundary

The above AFIR obligations are for **publicly accessible** recharging points. Private, restricted-access or workplace installations may have a different legal context. The operator must classify each deployment and confirm its access model; do not assume that all installed EVSEs are public or that all private points are exempt from every other legal requirement.

## 4. Meter candidate decision matrix

| Criterion | EMH iML e-moc | Phoenix EEM-XM355 1674509 |
|---|---|---|
| Manufacturer MID claim | Yes; exact certificate scope pending | Yes; exact certificate scope pending |
| 3-phase direct/CT | Direct 4-wire, 0.1–5(40) A | CT-operated, 1 A / 5 A |
| 400 V / 32 A reference | Nominal voltage fits; 40 A max; thermal/protection verification open | Depends on CT ratio and approved chain |
| CHARX point-meter configuration | OCMF-specific path; exact four-point cluster validation open | Selectable point-meter profile in current 1.9.1 help |
| CHARX OCMF legal-metrology list | Yes, firmware 1.09 / OCMF 1.4.1 | Not listed |
| Signed charging records | Manufacturer describes OCMF/signature features | Not evidenced in reviewed data |
| Portuguese billing approval | Not established | Not established |
| Current procurement / exact SKU | Supplier confirmation/quotation pending | Supplier confirmation/quotation pending |
| Current status | Leading OCMF prototype candidate | Leading non-OCMF point-meter candidate |

**Recommendation:** build the first isolated bench prototype around EMH iML e-moc if Phoenix confirms the four-point SEC-3xxx/SEC-1000 topology and EMH provides the certificate package. Keep EEM-XM355 as the alternative for load management/telemetry where signed OCMF billing is not required or where a separately compliant transaction-meter architecture is demonstrated. Do not combine both meters in the same output unless the architecture and legal purpose of each measurement are explicitly defined.

## 5. Four-output product architecture

For a quad charger:
- MTR-01 is permanently mapped to EVSE-01.
- MTR-02 is permanently mapped to EVSE-02.
- MTR-03 is permanently mapped to EVSE-03.
- MTR-04 is permanently mapped to EVSE-04.
- Optional MTR-GRID measures the upstream installation/fuse and is never used as a substitute for per-output energy attribution.
- Each point's meter identity, meter firmware, configuration, certificate reference and output mapping are stored in a controlled commissioning record.
- The backend binds each charging transaction to exactly one output, meter identity, signed meter record (when used), timestamps, tariff version, payment result and final settlement state.

No shared meter may be used to allocate customer energy by subtraction or estimated load unless an approved legal/metrology architecture explicitly supports it.

## 6. Offline, payment and transaction policy

The CHARX OCMF help reviewed in M1.13/M1.14 documents temporary offline storage on the controller with a limit of 100 charging processes, after which older records are deleted. Treat this as a critical vendor-specific capacity constraint until the exact model/firmware manual and supplier confirmation are attached to the design record.

Required V1 policy:
- No new paid session without a locally valid authorisation/payment token and a defined offline policy.
- Preserve local electrical safety independently of payment/backend availability.
- Never represent a pending offline payment as settled.
- Maintain durable transaction states: CREATED, AUTHORISED, STARTED, STOPPED, METER_RECORD_CAPTURED, UPLOADED, VERIFIED, SETTLED, RECONCILIATION_REQUIRED, VOIDED.
- Persist meter serial, point ID, signed payload, signature/key reference, meter start/end readings, energy, tariff snapshot, payment reference, timestamps and upload/verification outcome.
- Idempotent upload and reconciliation; retries must not create duplicate charges.
- Alert before the controller's offline record capacity is exhausted; do not rely on the controller as the only durable archive.
- If meter signature validation fails, meter identity is unknown, output mapping is ambiguous or records are missing, quarantine the transaction for reconciliation and do not silently bill an estimated kWh value.
- Define a customer-facing refund/dispute and operator recovery process before deployment.

These are product requirements, not claims that the current CHARX firmware implements all of them.

## 7. Supplier and authority evidence requests

### 7.1 Phoenix Contact

1. Confirm four-point operation with four EMH iML e-moc meters on the selected SEC-3xxx/SEC-1000 topology.
2. Confirm exact firmware 1.9.1 (or later) support, OCMF version, baud rate, Modbus configuration, meter address scheme and wiring.
3. Confirm whether one cluster can independently capture and preserve OCMF records for four concurrent/overlapping sessions.
4. Confirm the 100-process offline storage limit, deletion policy, power-loss/restart persistence and export/recovery process.
5. Confirm the supported OCPP release mode and backend payload path for signed OCMF records.
6. Provide the exact current manual revision, configuration guide and any known limitations.

### 7.2 EMH

1. Supply the complete MID / EU type-examination and national approval certificates and declarations.
2. Confirm 32 A continuous operation in the intended enclosure and ambient range, including terminal and protection requirements.
3. Confirm meter auxiliary supply and RS-485/OCMF operating modes, firmware and approved parameter set.
4. Confirm sealing, tamper protection, clock requirements, public-key/certificate handling and service procedure.
5. Confirm product lifecycle, orderable SKU, lead time, warranty and four-unit quotation.

### 7.3 IPQ / Portuguese qualified legal-metrology adviser

1. Confirm whether and how the iML e-moc MID/type-examination and national approval documents are recognised for commercial EV charging in Portugal.
2. Identify applicable Portuguese legal-metrology controls, verification, seals and competent-body responsibilities for the proposed charging transaction.
3. Confirm whether the complete meter + EVSE + firmware + signed-record backend chain requires additional national approval or verification.
4. Confirm how this applies to public ad-hoc, contract/RFID, fleet and private/workplace charging models.

### 7.4 Operator/payment/fiscal advisers

Confirm the responsible legal entity and process for AFIR ad-hoc access, price display, payment, invoicing, VAT/tax, consumer information, refunds, chargebacks, GDPR and transaction-data retention. AFIR does not itself settle all fiscal/invoicing questions.

## 8. M1.15 gate status

| Gate | Status |
|---|---|
| Portuguese general legal-metrology framework identified | CONFIRMED — Decree-Law 29/2022 |
| IPQ identified as National Metrology Institution | CONFIRMED — Article 13 |
| MID certificate scope for EMH iML e-moc reviewed | OPEN |
| Exact Portuguese commercial-billing applicability | OPEN — IPQ/legal confirmation required |
| AFIR Article 5 public ad-hoc and pricing rules mapped | CONFIRMED |
| 22 kW under-50-kW price-component order captured | CONFIRMED |
| Secure QR/internet payment route below 50 kW captured | CONFIRMED |
| Four-point EMH OCMF cluster compatibility | OPEN |
| Offline record capacity/recovery policy | OPEN |
| Final meter selection and production BOM | NOT SELECTED |

## 9. Release rule

No product datasheet, offer, contract or marketing material may claim Portuguese MID billing compliance, OCMF legal-metrology compliance, Eichrecht compliance or AFIR compliance solely from the candidate meter's product page or this research note.

Release requires: complete certificate review, IPQ/qualified legal-metrology confirmation, exact supplier firmware/topology evidence, four-output bench validation, signed-record verification, offline recovery test, AFIR user/payment/pricing assessment and qualified electrical design review.

**Safety:** M1.15 is a regulatory and architecture study. It does not approve components, protection, wiring, installation, energisation, billing or commercial deployment.

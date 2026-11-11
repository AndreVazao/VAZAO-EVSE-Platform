# M1.18 — Independent technical validation matrix

**Status:** DRAFT — validation planning baseline; no tests claimed as executed.  
**Date:** 2026-11-11  
**Scope:** Charger Hardware V1, single-output reference and four-output modular cluster.  
**Purpose:** separate manufacturer claims, documentary evidence, bench verification and release approval into traceable gates.

## 1. Rules of evidence

Every requirement is evaluated in four distinct layers:

- **M — Manufacturer evidence:** exact product, revision, firmware, official document and page/section or written manufacturer response.
- **D — Design evidence:** project drawing, calculation, interface schedule, risk analysis or configuration baseline reviewed by a competent engineer.
- **T — Test evidence:** reproducible test procedure, equipment, calibration status, measured results, logs, photographs and witnessed outcome.
- **A — Approval:** named competent reviewer signs the specific gate and scope.

A product-page feature statement is not a terminal schedule. A family brochure is not a four-point compatibility statement. A MID mark is not, by itself, proof that the complete installed measurement chain is approved for every Portuguese billing use. A bench test does not replace statutory conformity assessment or qualified installation review.

### Status vocabulary

| Status | Meaning |
|---|---|
| NOT STARTED | No evidence package or test execution recorded |
| OPEN | Evidence/test/review missing or incomplete |
| PARTIAL | Some evidence exists; acceptance criterion not fully met |
| PASS | All stated criteria met with retained evidence |
| FAIL | Criterion not met; corrective action required |
| BLOCKED | Cannot proceed until a dependency or external decision is resolved |
| N/A | Justified as not applicable, with reviewer and rationale |

No item is PASS merely because a document has been created. Unless explicitly stated otherwise, every row below starts OPEN or NOT STARTED.

## 2. Validation governance and safety boundary

1. No mains energisation, live fault injection, protective-device testing, EV connection or public deployment is authorised by this matrix.
2. SELV-only simulation and unpowered mechanical inspection may be planned separately; execution still requires competent personnel, risk assessment and suitable instruments.
3. Any mains-connected test must have an approved test plan, safe test enclosure, isolation/lockout procedure, emergency stop, suitable protective equipment, calibrated instruments and a qualified electrical test lead.
4. Never defeat protective earth, RCD/RCM, interlocks, contactor feedback, watchdogs or protective shutdowns to obtain a passing result.
5. CT secondary circuits must never be left open while their primary conductor is energised. Use approved shorting/isolating terminals and an approved procedure.
6. All tests must identify the exact DUT serial numbers, hardware/firmware revisions, wiring revision, test environment and operator.
7. Record unexpected behaviour as a defect. Do not repeat a hazardous test until reviewed and authorised.
8. Production release requires separate compliance, metrology, electrical design, manufacturing and operational approvals.

## 3. Requirement validation matrix

### 3.1 Controller and four-output architecture

| ID | Requirement / claim | M evidence required | D evidence required | T acceptance criterion | Failure consequence | Initial status |
|---|---|---|---|---|---|---|
| CTRL-01 | Exact SEC-3xxx + SEC-1000 combination is supported | Current compatibility matrix and written confirmation for exact order codes/revisions | Frozen cluster BOM and topology drawing | Manufacturer-approved assembly matches documented topology | Block controller selection | OPEN |
| CTRL-02 | Four SEC-1000 points operate concurrently under one cluster | Explicit four-point statement; module and firmware limits | Four-point allocation and dependency diagram | All four point identities remain distinct during concurrent simulated sessions | Block quad architecture | OPEN |
| CTRL-03 | Backplane connectors/accessories are exact | Order codes, manual, assembly instructions | Mechanical layout and connector schedule | Physical assembly matches manufacturer instructions; no improvised bus segment | Block fabrication | OPEN |
| CTRL-04 | Backplane current remains within limit | Exact limit and measurement boundary for selected cluster | Load inventory and worst-case budget | Measured worst-case bus current within published limit with margin approved by manufacturer | Block cluster power-up | OPEN |
| CTRL-05 | SEC-3xxx/gateway loss has defined safe response | Manufacturer failure behaviour and recovery manual | Fault containment and state-transition design | Every point reaches documented safe state; no unintended energisation; recovery is deterministic | Block multi-point operation | OPEN |
| CTRL-06 | Inter-module bus break has defined response | Manufacturer response to bus segmentation/open circuit | Fault-zone drawing | Affected and unaffected outputs behave exactly as approved; no unsafe restart | Block quad operation | OPEN |
| CTRL-07 | Each output has unique identity/configuration | Configuration schema and addressing rules | Point-to-port mapping register | No cross-attribution in four concurrent simulated sessions | Block billing and operation | OPEN |
| CTRL-08 | Firmware/configuration baseline is reproducible | Release notes, supported versions, update/rollback guidance | Version-controlled configuration export and hash register | Restore produces identical intended configuration; unsupported downgrade prevented | Block release | OPEN |

### 3.2 Local EVSE safety chain and switching

| ID | Requirement / claim | M evidence required | D evidence required | T acceptance criterion | Failure consequence | Initial status |
|---|---|---|---|---|---|---|
| SAFE-01 | CP/PP function is supported for exact controller | Exact manual terminal schedule and supported Type 2 interface | Per-point CP/PP schematic and component data | Approved simulator demonstrates valid states and invalid-state shutdown | Block EVSE control | OPEN |
| SAFE-02 | Contactor output can drive selected coil | Output electrical rating, isolation, inrush and suppression limits | Coil/driver calculation and interface circuit | Approved low-voltage test confirms pickup/dropout within limits; no output overload | Block contactor selection | OPEN |
| SAFE-03 | Contactor feedback detects commanded/actual mismatch | Supported feedback input and diagnostic behaviour | Feedback wiring and state logic | Simulated stuck/open/weld-feedback cases produce specified fault and inhibit restart | Block safety release | OPEN |
| SAFE-04 | Watchdog and controller reset reach safe state | Manufacturer watchdog/reset behaviour | Safety-state transition and restart interlock design | Controlled low-voltage reset tests show outputs de-energised until all restart conditions pass | Block controller release | OPEN |
| SAFE-05 | RCM sensor/interface is exact and compatible | Exact sensor code, firmware support and wiring | Sensor interface and fault threshold coordination | Approved simulator/test set verifies detection path and shutdown response | Block safety release | OPEN |
| SAFE-06 | External RCD/protection coordination is engineered | Manufacturer requirements and applicable standards references | Protection coordination study by qualified designer | Review confirms selected protective scheme and documented test method | Block mains design | OPEN |
| SAFE-07 | PE remains continuous and unswitched | Component instructions and applicable design requirements | Protective bonding drawing and conductor sizing | Qualified continuity/bonding test passes under approved procedure | Immediate stop/reject | OPEN |
| SAFE-08 | Per-output fault containment is demonstrated | Manufacturer fault matrix | Single-point versus common-cause analysis | Each injected *simulated* fault affects only the intended domain or causes documented safe global shutdown | Block quad release | OPEN |

### 3.3 Metering, OCMF and legal metrology

| ID | Requirement / claim | M evidence required | D evidence required | T acceptance criterion | Failure consequence | Initial status |
|---|---|---|---|---|---|---|
| MET-01 | Exact EMH iML e-moc variant is current and supported | Order code, lifecycle notice, datasheet, manual | Meter BOM and revision control | Received device matches approved identity and revision | Block procurement | OPEN |
| MET-02 | MID certificate covers intended meter and use | Full certificate, annexes, scope and conformity assessment | Certificate-to-use applicability review | Competent metrology reviewer confirms exact scope and limitations | Block billing use | OPEN |
| MET-03 | Portuguese legal-metrology requirements are met | Applicable authority guidance and certificate evidence | Written Portugal applicability assessment | All required approvals, verification and seals identified and satisfied | Block commercial billing | BLOCKED |
| MET-04 | 32 A continuous operation is thermally suitable | Manufacturer continuous-current/thermal data and derating | Enclosure, spacing, conductor and heat calculation | Qualified test plan and measured temperature rise meet approved limits | Block 32 A design | OPEN |
| MET-05 | Four meters remain independently attributable | Phoenix and EMH written concurrent-use confirmation | Meter-to-output mapping | Four simultaneous simulated sessions produce four distinct meter identities and no cross-assignment | Block quad billing | OPEN |
| MET-06 | OCMF signatures are verifiable | Exact OCMF profile, algorithm, key/certificate lifecycle | Trust/key management and verification design | Independent verifier validates valid records and rejects altered/invalid records | Block billing | OPEN |
| MET-07 | Record sequence and replay protection are sound | Counter, duplicate and acknowledgement semantics | Reconciliation and idempotency design | Replayed/duplicated/out-of-order test records do not create duplicate charge transactions | Block backend release | OPEN |
| MET-08 | Measurement boundary is correct | Certified installation diagram and sealing instructions | Approved metering schematic | Qualified reviewer confirms placement and seal boundary before any build | Block wiring release | OPEN |
| MET-09 | Optional XM355 alternative is correctly classified | Current profile list and meter certificate | Separate alternative architecture record | Tests distinguish point-meter/load-management capability from OCMF billing evidence | No substitution by assumption | OPEN |

### 3.4 Communications, offline persistence and cybersecurity

| ID | Requirement / claim | M evidence required | D evidence required | T acceptance criterion | Failure consequence | Initial status |
|---|---|---|---|---|---|---|
| COM-01 | RS-485 physical wiring is fully specified | Exact terminal schedule and bus manual | Approved wiring, shielding, termination and grounding schedule | Inspection confirms build matches approved schedule | Block bus energisation | OPEN |
| COM-02 | Modbus settings and meter profile are exact | Register map, baud/parity/address rules | Configuration register and point mapping | Readings, scaling, signs and error states match independent reference | Block meter integration | OPEN |
| COM-03 | Four meters can communicate without collisions | Manufacturer bus limits and topology | Bus loading/timing calculation | Worst-case polling and error recovery meet approved timing | Block quad meter bus | OPEN |
| OFF-01 | WAN loss does not bypass local safety | Local controller behaviour documentation | Offline state machine | WAN loss never changes safety permissives or bypasses local protection | Block deployment | OPEN |
| OFF-02 | Transaction records survive abrupt power loss | Documented persistence guarantees and limits | Data integrity/recovery design | Approved power-interruption simulation loses no acknowledged record and creates no duplicate | Block offline operation | OPEN |
| OFF-03 | Storage capacity and retention are adequate | Quantified capacity and retention limits | Peak session-rate and retention calculation | Test at defined worst-case load meets retention and alarm thresholds | Block public operation | OPEN |
| OFF-04 | Reconnection reconciles deterministically | Backend/controller recovery documentation | Idempotent reconciliation sequence | Repeated reconnect/retry yields one correct transaction per session | Block settlement | OPEN |
| OFF-05 | Clock and timestamps are trustworthy | Clock source, RTC accuracy and loss behaviour | Time sync, drift and audit design | Simulated clock loss/drift is detected and flagged; records remain auditable | Block billing | OPEN |
| SEC-01 | Firmware/configuration updates are controlled | Signed update and rollback documentation | Access and release process | Invalid/unauthorised update rejected; approved restore verified | Block field release | OPEN |
| SEC-02 | Credentials and signing keys are protected | Vendor security architecture | Provisioning, rotation, revocation and incident procedure | Test credentials cannot be extracted through supported user interface; revoked key rejected | Block backend release | OPEN |
| SEC-03 | Network segmentation is defined | Vendor network ports/services documentation | Threat model and network diagram | Security review finds no unapproved exposed service or shared trust path | Block deployment | OPEN |

### 3.5 Power, thermal, mechanical and environmental

| ID | Requirement / claim | M evidence required | D evidence required | T acceptance criterion | Failure consequence | Initial status |
|---|---|---|---|---|---|---|
| PWR-01 | Approved PSU supports actual cluster/peripherals | Exact PSU rating, derating and protection data | Complete worst-case current budget | Measured maximum load stays within approved continuous rating and margin | Block PSU selection | OPEN |
| PWR-02 | Backplane and auxiliary rails are not conflated | Manufacturer rail boundaries and limits | Separate rail diagrams and budgets | Inspection and measurement confirm no unauthorised cross-feed | Block power design | OPEN |
| PWR-03 | Contactor coil supply is adequately sized | Coil steady/inrush and switching data | Coil supply and suppression calculation | Approved low-voltage test shows stable operation and no rail collapse | Block switching design | OPEN |
| TH-01 | Enclosure thermal design is adequate | Component operating limits and derating | Heat-loss calculation and layout | Qualified thermal test at declared ambient/load meets all component limits | Block enclosure release | OPEN |
| MEC-01 | IP/IK and mechanical installation meet declared use | Enclosure/component certificates | Mechanical drawing, cable entries and mounting review | Inspection and appropriate certified tests meet declared IP/IK target | Block installation | OPEN |
| MEC-02 | Cable routing, segregation and strain relief are adequate | Manufacturer wiring instructions | Harness, duct and gland drawings | Inspection confirms bend radius, segregation, strain relief and serviceability | Block fabrication | OPEN |
| ENV-01 | Ambient and condensation limits are addressed | Operating/storage/environment limits | Site environmental envelope and mitigation | Environmental review/test passes declared deployment envelope | Block site release | OPEN |

### 3.6 Payment, user experience and compliance

| ID | Requirement / claim | M evidence required | D evidence required | T acceptance criterion | Failure consequence | Initial status |
|---|---|---|---|---|---|---|
| PAY-01 | Public ad-hoc access is available | Payment provider capability and AFIR advice | User journey and payment architecture | End-to-end test completes an ad-hoc journey without mandatory RFID/app contract | Block public deployment |
| PAY-02 | Price is transparent before session | Tariff and interface requirements | Tariff display specification | User can see applicable price components before authorising charge | Block public deployment |
| PAY-03 | Payment failure cannot defeat local safety | Payment service failure modes | Separation architecture | Payment/backend loss never bypasses EVSE local safety | Block payment integration |
| TAX-01 | Portuguese invoicing/tax process is valid | Qualified fiscal advice and provider documentation | Invoice and transaction mapping | Accountant/fiscal specialist signs test invoice and reconciliation flow | Block commercial launch |
| PRIV-01 | Personal data handling is lawful and minimised | Vendor data processing documentation | GDPR data map, retention and access policy | Privacy review approves collected fields, retention and deletion workflow | Block live user data |
| OPS-01 | Support, refunds and dispute evidence are defined | Provider/operator service commitments | Operations and escalation procedures | Tabletop and sandbox tests resolve interrupted session, refund and dispute scenarios | Block launch |

## 4. Bench test plan and controlled sequence

The sequence is intentionally staged. A later stage cannot start until its dependencies are PASS and the test lead authorises progression.

### Stage 0 — document and configuration gate
- Confirm exact product order codes, revisions and firmware.
- Collect complete manuals, terminal schedules, certificates and compatibility statements.
- Freeze a non-energised test configuration and record hashes of firmware/configuration exports.
- Identify all missing evidence and block any dependent test.

**Pass:** no unknown terminal mapping, no assumed product compatibility, all test equipment and procedures identified.

### Stage 1 — unpowered mechanical and SELV inspection
- Inspect DIN rail, backplane connectors, protective separation, labels, terminals, cable entries and enclosure layout.
- Check that mains and SELV domains are physically segregated as designed.
- Inspect PE bonding design without applying mains power.
- Check PSU and peripheral load calculation against exact manufacturer data.

**Pass:** drawing/build correspondence is complete; no exposed or improvised connection; qualified reviewer accepts SELV inspection.

### Stage 2 — controller and communication simulation
- Use manufacturer-approved simulator/test harness and SELV supply only.
- Verify four point identities, module discovery, configuration restore and firmware reporting.
- Simulate RS-485 devices and validate addressing, register scaling, timeout and bus recovery.
- Record per-point state and communication logs.

**Pass:** four points remain correctly identified; no cross-assignment; all errors are explicit and recoverable as documented.

### Stage 3 — meter and OCMF verification
- Use calibrated reference equipment and manufacturer-approved test conditions.
- Compare meter readings across declared operating points and directions.
- Verify OCMF signature independently, including altered payload and invalid certificate/key cases.
- Test sequence counters, acknowledgement, duplicate delivery and record export.
- Do not infer legal billing approval from a successful technical test.

**Pass:** accuracy meets exact certificate/specification and project requirement; signatures and record attribution pass; metrology reviewer signs scope.

### Stage 4 — local safety and switching simulation
- Simulate CP/PP states, interlocks, watchdog, controller reset, feedback mismatch and RCM fault using approved test interfaces.
- Test contactor driver only within approved SELV/test fixture limits until a separately authorised electrical test plan exists.
- Confirm no unexpected re-energisation after reset or communications restoration.

**Pass:** every defined fault reaches its specified safe state; restart requires all documented permissives.

### Stage 5 — four-output cluster and fault containment
- Run four concurrent simulated sessions with distinct identities and meter streams.
- Inject only approved simulated gateway loss, bus break, meter timeout, module reset and backend loss.
- Verify single-point fault containment and any documented cluster-wide safe shutdown.
- Confirm no record or meter attribution crosses between points.

**Pass:** measured behaviour matches the manufacturer-confirmed failure matrix; no undocumented degraded mode.

### Stage 6 — offline persistence and recovery
- Run the approved transaction simulation at a defined maximum event rate.
- Simulate WAN/backend loss, controller restart and controlled power interruption in a safe test fixture.
- Verify storage capacity, timestamps, sequence integrity, duplicate suppression and reconciliation.
- Record lost, delayed, rejected and recovered events.

**Pass:** all acknowledged records are retained within the documented capacity; reconciliation is deterministic; any limits are explicitly accepted by the operator and legal reviewer.

### Stage 7 — qualified electrical design and compliance review
- Review protective device selection/coordination, conductor sizing, short-circuit withstand, RCD/RCM, PE continuity, thermal, enclosure and installation.
- Review the exact certified metering boundary and Portuguese legal-metrology obligations.
- Review AFIR, fiscal, payment, consumer and GDPR obligations for the actual deployment classification.
- Prepare separate approved test and commissioning plans.

**Pass:** competent reviewers sign the exact revision and deployment scope. This stage is not replaced by software or SELV bench tests.

## 5. Required evidence packet for every test

Each test record must contain:

- Test ID and requirement IDs.
- Procedure revision and approval reference.
- Date/time, site/lab and environmental conditions.
- DUT model, serial, hardware revision and firmware.
- Wiring/configuration revision and relevant hashes.
- Instrument make/model/serial and calibration validity.
- Operator, witness and approving reviewer.
- Preconditions and safety controls.
- Raw readings/logs, expected values, tolerances and actual results.
- Photos/screenshots where useful, with sensitive information removed.
- PASS/FAIL/BLOCKED decision and rationale.
- Defect IDs, corrective action and retest linkage.
- Signatures/approval evidence.

Never replace raw evidence with a summary sentence alone.

## 6. Defect severity and stop rules

| Severity | Example | Required response |
|---|---|---|
| S0 — Critical safety | PE discontinuity, unintended contactor energisation, safety bypass, unsafe restart | Stop test immediately; isolate; quarantine DUT; no retest before safety review |
| S1 — Critical integrity | Cross-attributed meter record, invalid signature accepted, duplicate billing transaction | Block billing and deployment; preserve logs; root-cause analysis |
| S2 — Major function | Four-point topology unsupported, offline records lost, bus instability | Block affected architecture gate; corrective action and full regression |
| S3 — Minor | Label, documentation or non-safety UI defect | Track and close before relevant release; assess whether it affects operation |
| S4 — Observation | Improvement or non-blocking note | Record for design review; do not silently alter approved baseline |

Any unexpected energisation, loss of protective function, smoke, abnormal heating, exposed conductor, instrument overrange or unclear test state is an immediate stop condition.

## 7. Release gates

| Gate | Minimum closure | Current decision |
|---|---|---|
| G0 — architecture study | Manufacturer confirms exact cluster and module compatibility | OPEN |
| G1 — prototype BOM | Exact order codes, lifecycle and power budget confirmed | OPEN |
| G2 — SELV prototype | Stages 0–2 pass and evidence packet reviewed | NOT STARTED |
| G3 — meter/OCMF prototype | Certificates, attribution, signatures and stages 3/6 pass | BLOCKED |
| G4 — safety prototype | Local safety and fault containment pass under approved procedures | NOT STARTED |
| G5 — electrical design | Qualified design/protection/thermal/mechanical review signed | BLOCKED |
| G6 — Portugal commercial metrology | Exact legal-metrology applicability and verification path signed | BLOCKED |
| G7 — public service compliance | AFIR/payment/fiscal/GDPR/operator workflow approved | BLOCKED |
| G8 — production release | All applicable gates PASS; controlled drawings/BOM and manufacturing tests approved | BLOCKED |

A PASS at one gate does not imply PASS at another. A prototype pass does not automatically authorise production or public operation.

## 8. Current baseline decisions

- Retain EMH iML e-moc as the first OCMF/legal-metrology prototype candidate only.
- Retain EEM-XM355 1674509 as a point-meter/load-management alternative; do not claim OCMF billing support without evidence.
- Retain CHARX SEC-3xxx + SEC-1000 as a leading architecture study; do not claim four autonomous outputs or proven cluster failure containment.
- Keep the 6 A nominal backplane limit as a hard boundary until the exact selected cluster documentation states otherwise.
- Do not approve the previously reviewed 2.5 A PSU for quad use.
- Keep payment, network, RFID and backend services outside the local safety chain.
- No final production part numbers, wiring schedule, protective ratings, cable sizes, enclosure rating, payment provider or tariff are frozen.

## 9. Immediate next actions

1. Obtain Phoenix Contact and EMH written replies using M1.17; do not mark manufacturer-dependent rows PASS before replies are archived.
2. Request the exact EMH MID certificate/annex and written Portugal applicability review.
3. Obtain the exact terminal schedule and approved backplane/PSU configuration for the selected SEC-3xxx variant.
4. Build a non-energised document-controlled prototype configuration only after G0/G1 dependencies close.
5. Prepare test fixtures and procedures; obtain competent test lead approval before execution.
6. Populate this matrix with evidence IDs, test record IDs, dates and reviewer names; preserve all FAIL and retest history.

## 10. Change control

Any change to controller variant, firmware, meter, meter firmware, PSU, backplane, wiring, contactor, RCM, protective device, enclosure or payment architecture triggers an impact assessment. Reopen all affected matrix rows and tests. Do not overwrite old results; create a new revision and link the superseded baseline.

---
**Release statement:** M1.18 is a planning and traceability document. No physical tests have been performed or claimed by this document. It does not authorise mains energisation, fabrication, installation, billing or commercial deployment.

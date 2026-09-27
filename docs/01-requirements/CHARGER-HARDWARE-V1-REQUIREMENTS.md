# VAZÃO EVSE Charger Hardware V1 — Requirements

## 1. Product definition

V1 is an AC Mode 3 EVSE baseline for a single Type 2 charging point. The reference electrical rating is **up to 22 kW, 400 V AC three-phase, 32 A**, subject to installation, connector, thermal and regulatory limits.

The architecture shall scale to 2 and 4 outputs without redesigning the entire system.

## 2. Functional requirements

### FR-01 — Vehicle interface

- Type 2 AC interface.
- CP/PP handling according to the applicable EVSE standard.
- Contactor closure only when all required charging conditions are satisfied.
- Immediate controlled stop on critical safety fault.

### FR-02 — Local control

The local controller shall:

- maintain the EVSE state machine;
- read CP/PP state;
- command the power contactor through a safe output stage;
- acquire current/energy measurements;
- monitor temperatures and protective states;
- maintain local event logs;
- continue safe operation during network loss.

### FR-03 — Communications

The product shall support a modular communications bay:

- Ethernet;
- Wi-Fi;
- cellular LTE/4G;
- future communication modules without redesigning the power stage.

Connectivity loss shall not create an unsafe state.

### FR-04 — Authentication

Managed versions shall support RFID/NFC authentication through a replaceable reader module.

The RFID credential identifies the user/account. **The credential itself shall not be treated as an authoritative monetary ledger.** Monetary balance and authorization state shall use a secure wallet/token mechanism with cryptographic protection and anti-replay controls.

### FR-05 — Energy management

The controller shall expose an abstract available-power limit and implement local load management. For multi-output versions, a Master Controller shall allocate available power between charging sessions.

### FR-06 — Offline mode

When the CPMS is unavailable, the charger shall:

- keep safety functions local;
- retain session/event records locally;
- apply a locally provisioned authorization policy;
- support an auditable offline authorization mechanism for prepaid operation;
- synchronize records when connectivity returns.

The offline financial mechanism is a later security-design item and shall not depend on a writable RFID card balance alone.

## 3. Non-functional requirements

- Modular DIN-rail and PCB-based architecture.
- Clear separation between mains power, SELV/control and communications.
- Serviceable field wiring.
- Component identification and wire numbering.
- Event logging with monotonic sequence numbers and timestamps.
- Secure firmware update path for managed models.
- Watchdog and controlled restart.
- Default-safe behavior after controller failure.

## 4. Product variants

| Variant | Outputs | Connectivity | CPMS | Intended use |
|---|---:|---|---|---|
| Private Wallbox | 1 | optional | optional | residential/private |
| Managed Wallbox | 1–2 | Ethernet/Wi-Fi/LTE | yes | residential/business |
| Pedestal Single | 1 | modular | yes/optional | parking |
| Pedestal Dual | 2 | modular | yes/optional | parking |
| Pedestal Quad | 4 | modular | yes | parking |
| MultiStation | N | local Master | yes | charging parks |

## 5. Design constraints

The first physical prototype shall prioritize measurement, serviceability and safe test access over enclosure aesthetics.

## 6. Acceptance criteria

The V1 prototype is considered technically ready for controlled bench validation only after:

- schematic review;
- BOM review;
- insulation/PE/protection test plan approval;
- CP/PP state-machine validation;
- contactor fail-safe validation;
- current/energy measurement validation;
- communications-loss validation;
- TestStation interface definition.

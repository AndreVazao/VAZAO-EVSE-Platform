# VAZÃO EVSE Charger Hardware V1 — Electrical Architecture

## 1. System boundary

```text
GRID / INSTALLATION
       |
       v
[QF1 Main protection / isolation]
       |
       v
[Residual-current / EV protection]
       |
       v
[Surge / protection as required]
       |
       v
[Power distribution]
       |
       +---------------------> [PS1 AC/DC SELV supply]
       |
       v
[KM1 Power contactor]
       |
       v
[Energy meter / measurement]
       |
       v
[Type 2 outlet or tethered Type 2 cable]
       |
       +---- PE ---------------------------> chassis + EVSE PE
       +---- CP/PP <-----------------------> EVSE Controller

[EVSE Controller]
       +---- CP/PP interface
       +---- KM1 driver + feedback
       +---- meter communications
       +---- RCD/protection status
       +---- temperature / cabinet sensors
       +---- RFID/NFC
       +---- Ethernet/Wi-Fi/LTE
       +---- local storage / RTC
       +---- service/TestStation interface
```

## 2. Power architecture

Reference rating: 400 V AC, three-phase, up to 32 A per output for the 22 kW class.

The exact upstream protection is installation-specific and must be selected after short-circuit, earthing, cable, discrimination and local regulatory analysis. The product design shall therefore expose a protected input interface rather than hard-code one protection device as universally correct.

### Power path

`X1 -> QF1 -> residual-current/EV protection -> surge protection as required -> power distribution -> KM1 -> metering -> EV connector`

PE is bonded to the metallic enclosure and routed to the EV connector according to the final certified design.

## 3. Auxiliary power

A certified industrial AC/DC power supply provides SELV control power. The control supply is independently protected and shall be sized for:

- controller;
- communication module;
- RFID reader;
- contactor coils;
- indicator/display;
- sensors;
- service interface.

The control system shall remain galvanically separated from hazardous mains circuits except where a certified interface explicitly permits connection.

## 4. Safety chain

The safety chain shall not depend on the application processor or cloud service.

Conceptually:

```text
Protection state
   + RCD/RCM state
   + contactor feedback
   + controller watchdog
   + emergency/service interlock where applicable
          |
          v
     SAFE PERMISSION
          |
          v
   Contactor driver
          |
          v
       KM1
```

A production design shall use appropriate certified protective devices and a validated architecture for the applicable fault classes.

## 5. Measurement

For V1, the preferred architecture is a certified AC energy meter with a digital interface (for example Modbus RTU/RS-485) rather than relying on low-cost hobby current transformers for billing.

The controller may additionally monitor phase currents and temperatures for diagnostics.

Billing-grade measurement and diagnostic measurement shall be treated as separate requirements.

## 6. CP/PP subsystem

The Type 2 interface requires a dedicated EVSE CP/PP interface meeting the applicable standard. The interface shall provide:

- pilot signal generation/detection;
- vehicle presence/state detection;
- cable/proximity detection;
- electrically isolated or otherwise correctly protected MCU interface;
- fault detection.

Do not connect an MCU GPIO directly to CP or PP.

## 7. Controller architecture

Recommended V1 split:

- **Safety/EVSE MCU:** deterministic real-time state machine and local control.
- **Application/communications processor:** optional Linux-class module for networking, local UI, secure update and higher-level services.

The EVSE must remain safe and capable of terminating charging if the application processor crashes.

## 8. Expansion to dual/quad

The single-output power module becomes a repeatable channel:

```text
MASTER
  |
  +-- CHANNEL A -> protection/measurement/contacting -> Type 2 A
  +-- CHANNEL B -> protection/measurement/contacting -> Type 2 B
  +-- CHANNEL C -> protection/measurement/contacting -> Type 2 C
  +-- CHANNEL D -> protection/measurement/contacting -> Type 2 D
```

The Master performs allocation. Each channel retains its own local safety state.

## 9. MultiStation

A park controller can coordinate several charger controllers over Ethernet/RS-485/CAN or another validated field bus. Cloud connectivity is supervisory, not safety-critical.

## 10. VAZÃO EVSE TestStation integration

The charger shall expose a controlled service/test interface for:

- state-machine observation;
- CP/PP test access;
- meter verification;
- contactor state verification;
- fault injection under controlled laboratory conditions;
- firmware/version identification;
- diagnostic log extraction.

The TestStation remains external to the normal charger safety chain.

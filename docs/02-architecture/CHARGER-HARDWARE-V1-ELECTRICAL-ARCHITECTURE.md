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

`X1 -> QF1 -> residual-current/EV protection -> surge protection as required -> power distribution -> KM1 -> metering -> Type 2 output`

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

### 8.1 AC feeder topologies — mandatory design alternatives

Dual-output and quad-output products shall support an explicit engineering comparison of two installation topologies. They are alternatives to be evaluated per installation, not interchangeable wiring instructions.

**Topology A — independent incoming feeders**

- Dual: one separately protected feeder for output A and one for output B.
- Quad: one separately protected feeder for each of outputs A–D.
- Each feeder is calculated for its own output's maximum configured current and installation conditions.
- Each output has its own protective coordination and isolation provisions as required by the final design.
- This arrangement improves circuit separation and can simplify selective isolation, but may increase upstream cable routes, installation labour and space.

**Topology B — common incoming feeder with local distribution**

- Dual: one common incoming feeder supplies a suitably rated distribution assembly, which branches to the two output channels.
- Quad: one common incoming feeder supplies a suitably rated distribution assembly, which branches to four output channels.
- The common feeder and upstream protection must be designed for the maximum permitted aggregate demand, including the actual load-management policy and its failure/default state.
- Each branch from the distribution assembly to an output retains its own correctly coordinated protection and conductor sizing.
- The common feeder is not sized by simply reusing the single-output cable section. It is calculated for the aggregate design current and installation conditions.

### 8.2 Preliminary current envelope — not a cable-size table

For a 400 V three-phase output configured at 32 A, the nominal apparent-power reference is approximately 22.2 kVA per output (power factor and actual vehicle demand affect active power).

| Product | Independent-feeder envelope | Common-feeder aggregate envelope if all outputs can draw 32 A simultaneously |
|---|---:|---:|
| Single | 1 × 32 A | 32 A |
| Dual | 2 × 32 A feeders | 64 A |
| Quad | 4 × 32 A feeders | 128 A |

The 64 A and 128 A values are arithmetic aggregate design envelopes, not recommended protective-device ratings or cable selections. If a validated load-management system imposes a lower site limit, the common-feeder design may use that lower limit only when the limit is enforced locally, its sensor/control failure behavior is defined, and the upstream protection remains independently adequate. A cloud-only limit is not acceptable as the sole basis for reducing feeder capacity.

### 8.3 Conductor-sizing inputs and calculation gate

No cross-section in mm² is approved by this architecture document. For each incoming feeder and each branch feeder, the engineering calculation must record:

- design current and maximum simultaneous demand;
- supply system, phase count, voltage and earthing arrangement;
- cable conductor material, insulation type and rated temperature;
- installation method/reference method and whether installed in conduit, trunking, buried, free air or thermally insulated construction;
- ambient/soil temperature, grouping, spacing and thermal derating factors;
- route length and allowable voltage drop;
- prospective short-circuit current, disconnection time and adiabatic short-circuit withstand;
- protective-device type, rated current, trip curve/settings and coordination;
- neutral loading, harmonics and any required neutral sizing;
- PE conductor sizing and fault-loop/protective-device requirements;
- terminal, gland and connector accepted conductor ranges;
- local Portuguese rules and applicable editions of the relevant IEC/HD installation standards.

The calculation shall be performed separately for the **common trunk** and every **outgoing branch**. It shall verify current-carrying capacity after correction factors, voltage drop, short-circuit thermal withstand, automatic disconnection and protective-device coordination. The final chosen section must satisfy all applicable constraints; the most restrictive result governs.

### 8.4 Required design outputs

For each single, dual and quad variant, the CAD/electrical package shall include:

1. single-line diagram for independent-feeder topology;
2. single-line diagram for common-feeder topology;
3. feeder and branch cable schedule with calculated cross-sections and lengths;
4. protective-device schedule and coordination evidence;
5. load-management maximum-current setting and failure/default behavior;
6. terminal/distribution-block current and short-circuit ratings;
7. installation assumptions and calculation report.

Until those outputs are reviewed and approved, the cable section, breaker rating, terminal block and installation topology remain **TBD — NOT RELEASED**.

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


## 11. Local load-management boundary (M1.24)

A local energy-management controller may allocate a site or charger feeder current budget across output channels. It is supervisory to each EVSE's local safety controller and must never replace per-output protection, CP/PP state control, contactor feedback or residual-current protection.

The load manager shall:
- measure the relevant upstream phase currents using a validated measurement path;
- receive the approved aggregate feeder limit and per-output limits from a controlled configuration;
- allocate current budgets to channels and communicate them over a validated local interface;
- ensure each channel independently enforces its own permitted current;
- remain operational without CPMS/cloud connectivity;
- log allocation, limit changes, sensor faults, communication faults and fallback events.

A generic architecture does not imply that Phoenix Contact CHARX 2902802 supports this master/cluster role. Its current M1.4A review explicitly leaves multi-point coordination unproven. Any selected controller must demonstrate the required local setpoint interface and failure behavior from its own manufacturer evidence.

# VAZÃO EVSE Charger Hardware V1 — Electrical Functional Schematic

**Status:** DRAFT / engineering baseline  
**Reference:** single-output AC EVSE, Type 2, up to 22 kW / 400 V AC / 32 A three-phase.  
**Important:** functional architecture only. Final conductor sizing, protective-device coordination, earthing, short-circuit ratings, residual-current protection and installation design require qualified engineering review.

## 1. Functional power path

```text
GRID / INSTALLATION
   L1 L2 L3 N PE
        |
       QF1  Main isolation/protection
        |
       RCD1  Residual-current protection selected by final design
        |
       F1..F3  Branch protection where required
        |
       TB1  Power distribution
        |
       +--------------------+
       |                    |
      PS1                  KM1
  auxiliary AC/DC       EV power contactor
       |                    |
       |                 EM1 / meter
       |                    |
       |                X1 TYPE 2
       |                    |
       +---- PE -------------------- chassis / protective bonding
```

## 2. Control and safety architecture

```text
                     +----------------------+
                     |   SAFETY / EVSE      |
                     |  CP/PP interface     |
                     |  interlocks          |
                     +----------+-----------+
                                |
                         +------+------+
                         | MCU1 EVSE   |
                         | controller  |
                         +------+------+
                                |
             +------------------+------------------+
             |                  |                  |
          KM1 driver          EM1                COM1
             |             energy/current       Ethernet
             |               metering             |
          KM1 coil        measurement bus       LTE/Wi-Fi
                                                |
                                               CPMS
```

The cloud/CPMS path is **not** part of the primary safety chain. Loss of communications shall not cause an unsafe energisation.

## 3. Type 2 interface

The final design shall implement the applicable CP/PP interface according to the current applicable editions of the EV charging and connector standards. The controller shall not directly expose MCU pins to the vehicle interface; use a dedicated, protected EVSE CP/PP interface stage.

## 4. Protective bonding

PE shall have a dedicated protective-bonding path to:
- metallic enclosure;
- exposed conductive parts;
- Type 2 PE contact;
- any other exposed conductive assembly requiring bonding.

Protective bonding shall not be routed through the switching contactor.

## 5. Measurement

The production architecture should use a certified EVSE-compatible energy meter or metering subsystem rather than hobby-grade current transformers as the billing source.

Minimum telemetry:
- phase currents;
- phase voltages where required;
- active energy;
- frequency;
- power;
- meter status;
- temperature where applicable.

## 6. Safety states

The EVSE shall have explicit states such as:
- BOOT
- SELF_TEST
- AVAILABLE
- VEHICLE_CONNECTED
- AUTHORIZED
- READY_TO_CHARGE
- CHARGING
- STOPPING
- FAULT
- OFFLINE

A critical fault shall force a safe state independent of CPMS availability.

## 7. Reference standards

The design baseline shall be reviewed against the applicable current editions of IEC 61851-1, IEC 62196-1/-2 and IEC 60364-7-722. IEC currently lists IEC 61851-1:2017/COR1:2023, IEC 62196-1:2025 and IEC 62196-2:2025 as relevant current publications.


## 8. Multi-output feeder variants (M1.29)

The single-output functional diagram above is the repeatable output-cell reference. Dual/quad products shall additionally support these installation interfaces:

**Independent feeder option:** one separately identified incoming circuit per output, with its upstream protection/isolation and dedicated route.

**Common feeder option:** one aggregate incoming feeder to a main isolator/protection and rated distribution block/busbar, followed by separately protected output branches. Internal branch conductors are sized independently from the common incoming feeder.

**Hybrid option:** two or more independently protected feeder groups supplying defined output subsets.

**Managed common feeder:** a common feeder with a local load manager enforcing a configured maximum current per phase at the feeder boundary. The maximum demand reduction may only be used in the feeder design when the load control is installed, secured, monitored and proven to fail safely. Cloud connectivity is not a protective load limit.

In every topology, each output retains its local EVSE safety function and required individual protective architecture. A shared feeder or master controller does not replace per-output overcurrent/RCD/DC-fault protection or local safe-state control. The physical location of protective devices (upstream board or inside the EVSE) must be explicit and comply with the applicable installation/product requirements.

Reference unmanaged currents for 22 kW / 32 A three-phase outputs are 32 A per phase for one output, 64 A per phase for two outputs, and 128 A per phase for four outputs. These are planning values only; no cable section, breaker, busbar or terminal rating is selected. Cable sizing must include corrected ampacity, voltage drop, short-circuit withstand, disconnection, PE/neutral, phase balance, harmonics, grouping, ambient and actual installation method. See `docs/03-engineering/CHARGER-HARDWARE-V1-M1-29-MULTI-OUTPUT-FEEDER-TOPOLOGIES-AND-CABLE-SIZING.md`.


### External common-trunk distribution

For site installations where branching occurs upstream of the charger, represent the site main switchboard feeding a common trunk to an external local distribution/branch enclosure. From that enclosure, each EVSE output or charger unit receives a separately protected outgoing branch feeder. This external distribution board is distinct from the EVSE's internal main distribution block. The single-line diagram must identify the exact branch point, common trunk protection/isolation, branch protective devices, outgoing cable IDs, route lengths, neutral/PE arrangement and load-management measurement boundary. Cable sections and voltage drop are calculated separately for the common trunk and each branch, with total voltage drop checked to each EV connection. See M1.29.

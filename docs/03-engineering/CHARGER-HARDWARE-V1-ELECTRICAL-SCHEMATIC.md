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

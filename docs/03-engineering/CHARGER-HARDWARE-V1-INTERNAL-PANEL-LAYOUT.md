# VAZÃO EVSE Charger Hardware V1 — Internal Panel Layout

## Mechanical zoning

The cabinet is divided into three functional zones:

```text
+------------------------------------------------------+
| ZONE A — CONTROL / SELV                              |
| MCU1 | EVSE I/O | COM1 | RFID | HMI | PS1 secondary |
|------------------------------------------------------|
| ZONE B — POWER SWITCHING / MEASUREMENT               |
| KM1 | EM1 | terminal distribution | temperature      |
|------------------------------------------------------|
| ZONE C — MAINS PROTECTION / INCOMING                 |
| QF1 | RCD1 | branch protection | TB1 | PE bar        |
+------------------------------------------------------+
```

## Recommended physical rules

- Keep mains conductors physically separated from SELV/control wiring.
- Route control wiring in a separate duct.
- Cross power and signal wiring at approximately 90 degrees when crossing is unavoidable.
- Keep antenna and RF components away from high-current conductors and contactor coils.
- Provide clear service access to protection devices and terminals.
- Maintain creepage/clearance distances required by the applicable design and insulation category.
- Provide a dedicated PE bonding point on the metallic enclosure.

## Component IDs

| ID | Function |
|---|---|
| QF1 | Main protective/isolation device |
| RCD1 | Residual-current protection, final selection pending |
| TB1 | Incoming power terminal/distribution |
| PS1 | Auxiliary power supply |
| MCU1 | EVSE local controller |
| EVSE1 | Dedicated CP/PP EVSE interface |
| KM1 | Main EV power contactor |
| EM1 | Energy/current metering subsystem |
| COM1 | Ethernet/LTE/Wi-Fi communications |
| RFID1 | RFID reader |
| HMI1 | LEDs/display/user interface |
| X1 | Type 2 charging interface |
| PE1 | Protective earth/bonding bar |

## Cable segregation

### Power
QF1/RCD1/TB1/KM1/EM1/X1 power conductors.

### Control
MCU1/EVSE1/KM1 feedback/sensors.

### Communications
Ethernet/LTE/Wi-Fi/RFID.

The exact enclosure dimensions and mounting-plate hole pattern remain TBD until the selected production components are frozen.

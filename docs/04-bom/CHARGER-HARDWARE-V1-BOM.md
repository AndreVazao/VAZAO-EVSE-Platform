# VAZÃO EVSE Charger Hardware V1 — Engineering BOM

**Status:** preliminary sourcing baseline. Prices are indicative only and must be refreshed before purchasing.

## 1. BOM policy

This BOM is an engineering candidate list, not a purchasing release. Manufacturer part numbers are frozen only after the schematic, protection study, enclosure, connector interfaces and compliance strategy are frozen.

## 2. Mechanical

| Ref | Item | Qty | Status |
|---|---|---:|---|
| ENC1 | Outdoor-rated enclosure, target IP54/IP55 or higher according to installation | 1 | Select |
| MP1 | Metal mounting plate | 1 | Select |
| DIN1 | DIN rail system | 1 set | Select |
| DUCT1 | Wiring ducts / separators | 1 set | Select |
| GL1 | Cable glands / sealing system | 1 set | Select |
| PE1 | Protective-earth bonding bar | 1 | Select |

## 3. Protection and switching

| Ref | Item | Qty | Status |
|---|---|---:|---|
| QF1 | Main protective/isolation device | 1 | Engineering selection |
| RCD1 | Residual-current protection appropriate to final EVSE architecture | 1 | Engineering selection |
| SPD1 | Surge protection, selected from installation/system study | 1 | Engineering selection |
| F1.. | Branch protection where required | 1 set | Engineering selection |
| KM1 | EV power contactor with suitable AC rating and auxiliary feedback | 1 | Engineering selection |
| KMD1 | Contactor driver / interface | 1 | Custom/selected |
| TB1 | Power terminal/distribution system | 1 set | Select |

## 4. EVSE electronics

| Ref | Item | Qty | Status |
|---|---|---:|---|
| MCU1 | Industrial MCU controller board | 1 | Architecture selection |
| EVSE1 | Dedicated CP/PP EVSE interface | 1 | Select/custom |
| WDT1 | Independent watchdog / supervision | 1 | Architecture selection |
| I/O1 | Isolated digital I/O subsystem | 1 | Select/custom |
| EM1 | EVSE-compatible energy metering subsystem | 1 | Select |
| TEMP1 | Temperature sensing | 1+ | Select |

## 5. Communications

| Ref | Item | Qty | Status |
|---|---|---:|---|
| COM1 | Modular communications carrier | 1 | Architecture selection |
| ETH1 | Ethernet interface | 0/1 | Optional |
| LTE1 | LTE modem | 0/1 | Optional |
| WIFI1 | Wi-Fi interface | 0/1 | Optional |
| ANT1 | Antenna system | 0/1 | Depends on COM1 |

## 6. User interface

| Ref | Item | Qty | Status |
|---|---|---:|---|
| RFID1 | Secure RFID/NFC reader | 1 | Select |
| HMI1 | Status LED / display assembly | 1 | Select |
| ESTOP1 | Emergency/service isolation interface if required by final installation | 0/1 | Engineering selection |

## 7. Charging interface

| Ref | Item | Qty | Status |
|---|---|---:|---|
| X1 | Type 2 socket or tethered Type 2 assembly | 1 | Select |
| CP/PP | CP/PP interface components | 1 set | EVSE1 |
| CABLE1 | EV-rated internal cabling | 1 set | Final sizing pending |

## 8. Engineering rules

1. No hobby-grade sensor is accepted as the commercial billing meter.
2. Safety-critical components require documented ratings and datasheets.
3. Metering must have a defined accuracy and verification strategy before commercial billing.
4. Manufacturer part numbers are frozen only after schematic and enclosure interfaces are frozen.
5. Every production BOM item receives lifecycle status and approved alternatives.
6. Prototype cost and production cost are maintained separately.
7. All mains-connected components require final review for voltage/current rating, short-circuit withstand, temperature, creepage/clearance and applicable certification.

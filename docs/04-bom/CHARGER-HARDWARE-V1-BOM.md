# VAZÃO EVSE Charger Hardware V1 — Engineering BOM

## 1. BOM policy

The first BOM is an **engineering candidate list**, not a purchasing release. Manufacturer part numbers are selected only after the electrical schematic, protection study, enclosure dimensions, connector rating and certification strategy are frozen.

## 2. Functional BOM

| Ref | Component | Minimum requirement | Qty V1 | Status |
|---|---|---|---:|---|
| QF1 | Main isolation/protection | 3P/4P as required by final topology and installation | 1 | candidate |
| FI1 | Residual-current / EV protection | compliant with final EVSE protection concept | 1 | candidate |
| SPD1 | Surge protection | selected according to installation/system study | 1 | optional/required by design |
| PS1 | AC/DC supply | industrial, certified, SELV, sized for complete control load | 1 | candidate |
| KM1 | AC power contactor | rated for EVSE duty and selected current | 1 | candidate |
| M1 | Energy meter | suitable accuracy/compliance and digital interface | 1 | candidate |
| MCU1 | EVSE safety controller | deterministic control, watchdog, protected I/O | 1 | custom architecture |
| CPU1 | Application/comms processor | Ethernet/Wi-Fi/LTE support as configured | 1 | modular |
| RFID1 | RFID/NFC reader | supported credential technology and secure interface | 1 | candidate |
| COM1 | Ethernet | industrial interface | 1 | optional |
| COM2 | Wi-Fi | industrial module | 1 | optional |
| COM3 | LTE/4G | industrial modem + SIM/eSIM support | 1 | optional |
| T1.. | Temperature sensors | appropriate range and mounting | as required | candidate |
| J1 | Type 2 interface | certified socket or tethered assembly | 1 | candidate |
| X1.. | Terminal blocks | appropriate voltage/current/category | as required | candidate |
| DIN | DIN rails | enclosure compatible | as required | candidate |
| PE | PE terminals/bonding | protective bonding hardware | as required | mandatory |
| ENC1 | Enclosure | appropriate IP/IK, thermal and service requirements | 1 | candidate |
| GL1.. | Cable glands | suitable IP and cable ranges | as required | candidate |
| HARNESS | Internal wiring | conductor sizing from final calculation | 1 set | engineering |

## 3. Prototype electronics

The early bench prototype may use development hardware to validate the architecture. The production controller shall move to a controlled PCB design with:

- galvanic isolation where required;
- protected digital inputs/outputs;
- watchdog;
- secure boot/update strategy where applicable;
- documented connectors;
- EMC-conscious layout;
- test points for the VAZÃO EVSE TestStation.

## 4. Metering

Do not use hobby-grade current sensors as the sole billing measurement path. The billing architecture should use a suitable certified meter where required by the commercial/regulatory model. Diagnostic sensors can remain separate.

## 5. Costing

A procurement spreadsheet shall be created after the schematic is frozen. It will contain:

- manufacturer;
- exact part number;
- supplier;
- quantity breaks;
- prototype price;
- estimated production price;
- lead time;
- alternative component;
- certification evidence;
- lifecycle/availability status.

## 6. Variant reuse

The target is to reuse the following across single/dual/quad/wallbox products:

- controller architecture;
- communications module;
- RFID module;
- energy measurement architecture;
- control PSU family;
- service connectors;
- software/firmware.

Only the power/channel assemblies and mechanical arrangement should scale significantly.

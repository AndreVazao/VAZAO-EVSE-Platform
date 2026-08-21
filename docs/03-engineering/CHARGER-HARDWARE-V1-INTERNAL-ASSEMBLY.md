# VAZÃO EVSE Charger Hardware V1 — Internal Assembly

## 1. Mechanical concept

The first prototype uses a serviceable enclosure with a metal backplate. Components are grouped into functional zones.

```text
+------------------------------------------------------+
| ZONE A — CONTROL / SELV                              |
|  MCU | Application CPU | I/O | Ethernet/LTE | RFID   |
|  Service connector | low-voltage terminal blocks     |
+------------------------------------------------------+
| ZONE B — POWER CONTROL                               |
|  AC/DC supply | contactor | meter | control drivers |
|  diagnostic sensors                                  |
+------------------------------------------------------+
| ZONE C — PROTECTION / POWER ENTRY                    |
|  Main isolation/protection | residual-current        |
|  protection | SPD where required | PE/N terminals   |
+------------------------------------------------------+
| CABLE GLANDS / SERVICE ENTRY / TYPE 2 EXIT           |
+------------------------------------------------------+
```

## 2. Assembly sequence

### Step 01 — Prepare enclosure

- Fit backplate.
- Mark mains and SELV cable routes.
- Reserve service clearance around protection and contactor devices.
- Provide dedicated PE bonding point on the metallic enclosure.

### Step 02 — Install DIN rail system

Install separate DIN rail sections for:

- protection/power devices;
- auxiliary power;
- control interface devices.

### Step 03 — Install power-entry hardware

Mount the selected main isolation/protection devices and input terminals. The exact device ratings are confirmed by the electrical design and installation study.

### Step 04 — Install auxiliary power

Mount the certified AC/DC supply and its DC protection. Route SELV wiring separately from mains wiring.

### Step 05 — Install contactor and feedback

Mount the power contactor close to the EV output power terminals. Provide an auxiliary feedback contact to the controller.

### Step 06 — Install energy meter

Install the selected certified meter so that its measurement path corresponds to the final billing architecture. Connect its communication interface to the controller using the selected isolated field interface.

### Step 07 — Install EVSE controller

Mount the controller in Zone A. Keep CP/PP and low-voltage wiring away from high-current conductors.

### Step 08 — Install communications

Fit Ethernet and/or the selected Wi-Fi/LTE module. LTE antenna routing shall follow the modem manufacturer's RF requirements and shall not compromise enclosure IP protection.

### Step 09 — Install RFID

Mount the RFID/NFC reader behind a suitable non-metallic RF-transparent front area. Connect to the controller/application processor as defined by the selected module.

### Step 10 — Install Type 2 interface

Install the certified Type 2 socket or tethered cable assembly. Route PE, power conductors and CP/PP through the dedicated cable path. The final connector assembly must be mechanically secured and strain-relieved.

### Step 11 — Termination and identification

Every field conductor receives a unique wire/terminal identifier. Use ferrules and terminal blocks appropriate to the conductor and device.

### Step 12 — Inspection before energization

Verify:

- PE continuity;
- enclosure bonding;
- separation of mains and SELV wiring;
- terminal torque according to manufacturer data;
- correct protective-device arrangement;
- contactor default state;
- no exposed hazardous live parts;
- connector mechanical retention;
- correct fuse/protection identification.

## 3. Cable segregation

Use physically separated routes for:

- mains/high-current conductors;
- SELV control;
- Ethernet/communications;
- CP/PP.

Crossing between zones should be minimized and, where necessary, performed according to the relevant EMC and insulation requirements.

## 4. Serviceability

The design shall allow a technician to replace independently:

- communications module;
- RFID reader;
- controller;
- AC/DC supply;
- contactor;
- energy meter;
- Type 2 assembly;
- protective devices.

## 5. Quad-channel reuse

The single-output assembly becomes a channel module. Four channel modules are installed around a common Master and common upstream distribution while retaining channel-specific protection, measurement and safety control as required by the final electrical design.

## 6. Manufacturing note

This document defines physical architecture and assembly order. It does not authorize mains energization. Production assembly requires released electrical drawings, approved component references, torque tables, inspection records and applicable compliance documentation.

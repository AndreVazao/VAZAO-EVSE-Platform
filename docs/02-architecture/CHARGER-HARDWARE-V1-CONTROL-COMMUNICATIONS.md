# VAZÃO EVSE Charger Hardware V1 — Control & Communications

## 1. Logical modules

```text
+-----------------------------------------------------------+
|                    VAZÃO EVSE CHARGER                    |
|                                                           |
|  +----------------+       +----------------------------+  |
|  | EVSE Safety MCU|<----->| Application/Comms CPU      |  |
|  | CP/PP           |       | CPMS / OTA / local services|  |
|  | contactor       |       +----------------------------+  |
|  | local safety    |                    |                 |
|  +--------+--------+                    |                 |
|           |                              +-- Ethernet      |
|           +-- RS-485/CAN                +-- Wi-Fi         |
|           +-- Meter                     +-- LTE/4G        |
|           +-- RFID/NFC                  |                 |
|           +-- sensors                   +-- Local storage |
+-----------------------------------------------------------+
```

## 2. Controller responsibilities

### EVSE Safety MCU

- CP/PP state machine;
- contactor control;
- contactor feedback;
- protective-state monitoring;
- watchdog;
- deterministic stop on fault;
- local current limit enforcement;
- meter acquisition where required;
- event codes.

### Application/communications processor

- CPMS protocol client;
- authentication orchestration;
- RFID service;
- local cache;
- offline transaction queue;
- telemetry;
- diagnostics UI/API;
- secure firmware/update orchestration.

A single MCU may be used in the earliest prototype if the safety architecture is explicitly validated, but the production architecture should preserve a safety/control boundary.

## 3. Communications hierarchy

```text
Internet / CPMS
       |
   TLS connection
       |
Application CPU
       |
 local IPC / UART / CAN / RS-485
       |
EVSE Safety MCU
       |
 EVSE hardware
```

The CPMS never directly drives a mains contactor.

## 4. Connectivity options

### Ethernet

Preferred for fixed commercial installations where cabling is available.

### Wi-Fi

Optional for residential and suitable commercial environments.

### LTE/4G

Optional modular communication board for installations without Ethernet/Wi-Fi.

The communications bay shall support a replaceable modem and antenna arrangement.

## 5. RFID and prepaid operation

RFID is an identity/authentication mechanism. It should not be used as an unprotected monetary database.

Recommended architecture:

```text
RFID credential
      |
      v
Local authentication service
      |
      +-- online -> CPMS wallet authorization
      |
      +-- offline -> cryptographically provisioned offline allowance/token
                         |
                         v
                    local ledger
                         |
                         v
                 queued settlement
```

The offline ledger must resist replay, cloning and double spending. This is a security-design workstream and shall be specified before production deployment.

## 6. Offline behaviour

The charger maintains:

- last known configuration;
- local clock;
- active session state;
- transaction/event sequence;
- authorization cache;
- local safety state.

When connectivity returns:

1. upload events in sequence;
2. reconcile sessions;
3. reconcile transactions;
4. obtain configuration updates;
5. confirm clock/time state;
6. clear acknowledged queue entries.

## 7. Master/Slave expansion

For a quad charger:

- one Master coordinates four channel controllers;
- each channel can maintain local safety;
- the Master calculates available power;
- allocation is recalculated when a vehicle connects/disconnects, a current limit changes, or a fault occurs.

The algorithm shall prioritize safety first, configured operator policy second, and optimization third.

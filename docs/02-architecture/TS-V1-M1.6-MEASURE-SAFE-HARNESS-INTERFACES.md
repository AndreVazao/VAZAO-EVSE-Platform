# TS-V1-M1.6 — Measurement PCB, TS-SAFE & Harness/Connector Definition

**Produto:** VAZAO EVSE TestStation V1  
**Estado:** Baseline preliminar de engenharia — NÃO aprovado para fabrico/ligação à rede  
**Escopo:** AC monofásico/trifásico, 230/400 VAC, até 32 A/fase, até 22 kW.

## 1. Objetivo

M1.6 transforma a arquitetura M1.5 numa definição de interligação suficientemente concreta para iniciar desenho CAD/EDA das placas e do chicote.

Este documento define:
- fronteiras elétricas;
- blocos funcionais;
- interfaces entre PCBs;
- sinais;
- conectores;
- filosofia de cablagem;
- separação de domínios;
- pontos de teste;
- interfaces TestStation ↔ VAZAO EVSE.

Não constitui, por si só, esquema certificado nem autorização para energização.

## 2. Domínios elétricos

O TestStation deve ser dividido em cinco domínios:

1. **POWER-HV** — rede AC e carga;
2. **MEASURE-ISO** — aquisição isolada de tensão/corrente;
3. **SELV-CTRL** — 24 VDC e lógica;
4. **EV-INTERFACE** — CP/PP e interfaces de diagnóstico;
5. **COMMS** — CAN-FD/Ethernet/USB.

Regra: uma ligação entre domínios só existe através de uma interface explicitamente definida e com isolamento/proteção adequados.

## 3. Topologia geral

Fluxo funcional:

POWER-HV
→ proteção/seccionamento
→ contactores de segurança
→ Zone A / Zone B
→ interface EVSE/load

Em paralelo:

POWER-HV
→ sensores isolados
→ TS-MEASURE
→ CAN-FD
→ TS-CORE

SELV-CTRL
→ TS-SAFE
→ contactores/interlocks
→ estado seguro

EV-INTERFACE
→ TS-EV
→ CP/PP
→ EVSE

TS-CORE
→ GUI
→ testes
→ armazenamento
→ relatórios.

## 4. TS-MEASURE — definição de blocos

### 4.1 Entradas de tensão

Canais:
- VA_L1
- VA_L2
- VA_L3
- VB_L1
- VB_L2
- VB_L3

A arquitetura V1 deve reservar seis canais de tensão para permitir medição independente de Zone A e Zone B quando o hardware de potência o exigir.

Cada canal deverá possuir:
- proteção de entrada;
- limitação de energia;
- filtro;
- estágio de adaptação;
- isolamento quando necessário;
- ponto de teste;
- identificação permanente.

### 4.2 Corrente

Canais:
- IA_L1
- IA_L2
- IA_L3
- IB_L1
- IB_L2
- IB_L3

A arquitetura física pode ser reduzida numa primeira variante caso o objetivo de Zone B não exija seis canais simultâneos, mas o PCB deve reservar a expansão.

### 4.3 ADC

O ADC deve receber canais sincronizados.

Prioridade:
- mesma referência temporal;
- atraso conhecido;
- erro de fase caracterizado;
- possibilidade de captura de waveform.

O layout deve manter os canais simétricos tanto quanto possível.

### 4.4 MCU

Interface ADC:
- SPI;
- clock dedicado;
- DRDY;
- reset;
- alimentação limpa;
- referência;
- pontos de debug.

Interface externa:
- CAN-FD;
- UART de serviço;
- SWD/debug;
- sinal de sincronismo.

## 5. TS-MEASURE — conectores

### J1 — Zone A Voltage

Sinais:
- L1_A
- L2_A
- L3_A
- N_A
- PE/reference conforme arquitetura aprovada.

### J2 — Zone B Voltage

Sinais:
- L1_B
- L2_B
- L3_B
- N_B
- PE/reference conforme arquitetura aprovada.

### J3 — Current Sensors

Sinais:
- IA1
- IA2
- IA3
- IB1
- IB2
- IB3
- sensor returns/references conforme tecnologia escolhida.

### J4 — CAN-FD

- CANH
- CANL
- GND/isolated reference conforme transceiver
- shield/chassis conforme EMC.

### J5 — Service

- UART TX
- UART RX
- GND
- SWDIO
- SWCLK
- RESET
- optional synchronization.

### J6 — Calibration

Reservado para:
- referência de tensão;
- referência de fase;
- trigger/sync;
- acesso controlado a sinais de calibração.

O acesso deve ser protegido contra ligação acidental à rede.

## 6. TS-SAFE — blocos

TS-SAFE é responsável por levar o sistema para estado seguro independentemente do software principal.

### Entradas

- E_STOP;
- DOOR_INTERLOCK;
- LOAD_OVERTEMP;
- CONTACTOR_AUX_1;
- CONTACTOR_AUX_2;
- POWER_FAULT;
- WATCHDOG_HEARTBEAT;
- optional insulation/fault input.

### Saídas

- K_MAIN;
- K_ZONE_A;
- K_ZONE_B;
- K_LOAD;
- FAN_ENABLE;
- SAFE_STATUS.

A quantidade final de contactores depende do esquema de potência M1.7.

## 7. Cadeia de E-stop

Princípio:

E-STOP
→ cadeia de segurança
→ desenergização das bobinas de contactores
→ confirmação por contactos auxiliares
→ estado SAFE
→ sinalização para TS-CORE.

A MCU pode supervisionar a cadeia, mas não deve ser o único elemento responsável pelo corte.

Depois de um E-stop:
- não rearmar automaticamente;
- exigir condição segura;
- exigir comando explícito de reset;
- verificar feedback dos contactores.

## 8. Contactores e feedback

Cada contactor crítico deve possuir contacto auxiliar dedicado.

Exemplo lógico:

K_MAIN_CMD = ON
K_MAIN_AUX = OFF
→ FAULT_CONTACTOR_NOT_CLOSED

K_MAIN_CMD = OFF
K_MAIN_AUX = ON
→ FAULT_CONTACTOR_WELDED_OR_STUCK

A lógica final deverá considerar tempos de atuação e tolerâncias do fabricante.

## 9. Watchdog

Arquitetura:
- watchdog interno da MCU;
- watchdog externo;
- heartbeat entre TS-SAFE e TS-CORE.

Perda de heartbeat deve conduzir a estado seguro depois do timeout definido na análise de risco.

O timeout não deve ser escolhido arbitrariamente: deverá ser determinado pela análise de risco e tempos reais de desenergização.

## 10. TS-EV — interface CP/PP

### CP

Deve suportar:
- leitura de nível;
- geração de PWM;
- medição de duty cycle;
- estados IEC 61851 relevantes;
- fault injection controlada.

### PP

Deve suportar:
- resistência/codificação;
- identificação de cabo;
- medição;
- simulação de estados suportados.

### Fault injection

A arquitetura deve permitir falhas selecionáveis, por exemplo:
- CP aberto;
- CP curto conforme condição segura;
- estado inválido;
- alteração controlada de PP;
- perda de PWM.

Toda injeção deve ser limitada por hardware e pelo estado SAFE.

## 11. Interface TestStation ↔ VAZAO EVSE

O carregador VAZAO deve reservar uma interface de serviço.

### Grupo A — EV interface
- CP;
- PP;
- PE/reference onde apropriado.

### Grupo B — status
- contactor feedback;
- controller alive;
- charging state;
- fault state.

### Grupo C — diagnóstico
- CAN/service bus;
- UART/service;
- firmware identification;
- hardware revision;
- serial number.

### Grupo D — medição auxiliar
- tensão de controlo;
- referências;
- sinais internos selecionados.

Nenhum sinal interno deve ser exposto externamente sem análise de isolamento e segurança.

## 12. TS-LOAD

Interface de controlo:
- LOAD_ENABLE;
- LOAD_SETPOINT;
- LOAD_FAULT;
- LOAD_OVERTEMP;
- FAN_STATUS;
- LOAD_STATUS.

A potência deverá ser comandada por estágios independentes.

Proteções:
- limite de corrente;
- limite térmico;
- contactor de isolamento;
- falha de ventilação;
- timeout;
- estado seguro.

## 13. Harness principal

O chicote deve ser dividido por função:

### H-HV
Cabos de potência:
- L1;
- L2;
- L3;
- N;
- PE.

Não transportar sinais SELV no mesmo bundle sem separação física apropriada.

### H-MEASURE
- sensores de tensão;
- sensores de corrente;
- referências;
- shields.

### H-SAFE
- E-stop;
- interlocks;
- feedback contactores;
- térmicos.

### H-EV
- CP;
- PP;
- EV diagnostic.

### H-COMMS
- CAN-FD;
- Ethernet;
- USB/service.

### H-CTRL
- 24 VDC;
- GND;
- control outputs.

## 14. Regras de cablagem

- separar HV de SELV;
- minimizar loops de corrente;
- manter pares diferenciais juntos;
- CAN com impedância e terminação conforme arquitetura;
- shield/chassis definido num único documento de EMC;
- identificar ambas as extremidades;
- usar ferrules/terminais adequados;
- impedir inversão de conectores;
- usar conectores com codificação mecânica quando possível;
- separar cabos de potência de sinais de medição.

## 15. Conectores — filosofia

A escolha definitiva depende da corrente, ambiente e IP do compartimento.

Para sinais internos:
- conectores bloqueáveis;
- codificação;
- retenção mecânica;
- identificação;
- possibilidade de manutenção.

Para potência:
- bornes/terminais industriais;
- proteção contra toque;
- torque especificado;
- strain relief;
- separação física.

Para interfaces externas:
- conectores industriais adequados ao IP e ambiente;
- proteção contra ligação incorreta;
- chaveamento/codificação.

## 16. Test points

TS-MEASURE:
- TP_VA_L1
- TP_VA_L2
- TP_VA_L3
- TP_VB_L1
- TP_VB_L2
- TP_VB_L3
- TP_I_L1
- TP_I_L2
- TP_I_L3
- TP_ADC_REF
- TP_ADC_SYNC

TS-SAFE:
- TP_24V
- TP_SAFE_GND
- TP_ESTOP
- TP_WD
- TP_KMAIN_CMD
- TP_KMAIN_AUX
- TP_SAFE_STATUS

TS-EV:
- TP_CP
- TP_PP
- TP_PWM
- TP_EV_STATUS

Todos os test points ligados a domínio perigoso devem ser protegidos e claramente identificados.

## 17. PCB layout — TS-MEASURE

Separação física:
- entrada HV;
- AFE;
- ADC;
- referência;
- MCU;
- CAN.

Regras:
- evitar correntes de retorno de potência através da área analógica;
- minimizar área de loops analógicos;
- manter referência afastada de fontes de ruído;
- manter clock digital afastado de entradas sensíveis;
- plano de massa definido por análise, não por regra genérica;
- cumprir creepage/clearance calculados;
- manter simetria dos canais.

## 18. PCB layout — TS-SAFE

Separar:
- entradas de campo;
- lógica;
- drivers;
- alimentação;
- interfaces CAN.

A saída para contactores deve ser protegida contra:
- sobrecorrente;
- curto;
- transientes da bobina;
- ligação invertida.

A arquitetura de supressão da bobina deve ser escolhida de acordo com o tipo de bobina e tempos de desenergização necessários.

## 19. Diagnóstico Zone A / Zone B

O software deve associar cada canal ao ponto físico.

Exemplo:

VA_L1 → Zone A / L1  
VB_L1 → Zone B / L1

O relatório nunca deve apresentar apenas “L1” sem identificar a zona.

O mesmo princípio aplica-se a corrente, potência, energia e fase.

## 20. Dados brutos

Para cada ensaio, o sistema deverá poder guardar:
- waveform window;
- RMS;
- frequência;
- ângulo;
- sequência;
- potência;
- energia;
- temperatura;
- estados CP/PP;
- eventos de segurança;
- timestamps;
- identificação de firmware;
- identificação de hardware.

Os dados brutos devem permitir auditoria posterior do diagnóstico.

## 21. Diagnóstico inteligente

O motor de diagnóstico receberá:
- medições Zone A;
- medições Zone B;
- tolerâncias;
- incertezas;
- estados EVSE;
- eventos;
- histórico do equipamento.

A saída deve separar:
1. facto medido;
2. anomalia calculada;
3. hipótese técnica;
4. testes adicionais;
5. recomendação.

Nunca apresentar uma hipótese como componente definitivamente avariado sem evidência suficiente.

## 22. Requisitos de manutenção

Cada módulo deve poder ser substituído sem desmontagem completa da máquina.

Objetivos:
- TS-MEASURE substituível;
- TS-SAFE substituível;
- TS-EV substituível;
- TS-LOAD substituível;
- chicote identificado;
- calibração associada ao módulo quando aplicável.

## 23. Interface Mini / PRO / Factory

A mesma filosofia de conectores deve ser preservada nas três versões.

**Mini**
- menos canais;
- menor potência;
- diagnóstico essencial.

**PRO**
- canais completos;
- waveform;
- fault injection;
- carga controlada;
- diagnóstico avançado.

**Factory**
- automação;
- interfaces de produção;
- identificação automática;
- testes rápidos;
- integração MES/produção posteriormente.

O firmware/software deve abstrair diferenças de hardware através de capability discovery.

## 24. Documentos derivados

M1.6 deverá originar posteriormente:
- esquema elétrico completo;
- esquemáticos TS-MEASURE;
- esquemático TS-SAFE;
- esquemático TS-EV;
- esquemático TS-LOAD;
- harness drawing;
- connector pinout;
- wire list;
- BOM detalhada;
- PCB stackup;
- mechanical mounting;
- safety review.

## 25. Gates de aprovação

Antes do desenho PCB:
- interface freeze;
- revisão dos domínios;
- revisão de isolamento;
- revisão de conectores;
- revisão de proteção;
- revisão de sinais;
- revisão da arquitetura Zone A/B.

Antes de fabricar PCB:
- ERC/DRC;
- revisão esquemática;
- creepage/clearance;
- thermal review;
- EMC review;
- manufacturing review;
- BOM review.

Antes de energizar:
- ensaios sem tensão de rede;
- continuidade PE;
- isolamento;
- teste E-stop;
- teste contactores;
- teste feedback;
- teste watchdog;
- teste térmico;
- teste CP/PP;
- commissioning controlado.

## 26. Estado

**M1.6 — baseline de interligação definida.**

O próximo nível deve converter esta definição em esquemas CAD/EDA e pinouts completos.

## 27. Próximo marco

**TS-V1-M1.7 — Power Architecture + Protection Calculation + Contactor/Load Topology**

M1.7 fechará a arquitetura de potência que falta para transformar os blocos de M1.6 em circuitos concretos, incluindo Zone A/Zone B, contactores, proteção, carga e distribuição 24 VDC.

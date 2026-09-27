# VAZAO EVSE TestStation V1 — M2.2
## Real Sensor Front-End + CP/PP Detailed Schematic Baseline

**Estado:** M2.2 — engenharia detalhada de protótipo  
**Branch:** feat/charger-hardware-v1  
**Dependências:** M2.1  
**Objetivo:** transformar a arquitetura M2.1 em circuitos concretos para medição isolada, CP/PP, drivers de contactores e interface de calibração.

> Segurança: documento de engenharia de protótipo. Não é autorização para montagem/ligação à rede. O dimensionamento final deve ser revisto contra a instalação, normas aplicáveis, isolamento, curto-circuito, EMC, temperatura e ensaios.

---

## 1. Nova decisão importante: medição de tensão isolada

Para evitar colocar a rede diretamente no domínio do ADC, a baseline M2.2 passa a considerar **amplificador isolado de precisão para tensão**.

### Candidato principal
**TI AMC1311B**

Características verificadas na documentação TI:
- entrada de alta impedância otimizada para divisores resistivos;
- entrada de 2 V;
- isolamento reforçado;
- 5 kVrms de isolamento conforme especificação indicada pelo fabricante;
- tensão de trabalho de isolamento até 1500 Vrms;
- versão B com erro de ganho máximo de 0,2% segundo a ficha do fabricante;
- saída diferencial;
- alimentação low-side compatível com o domínio ADC.

O AMC1311B passa a ser **CANDIDATE FOR PROTOTYPE**, não ainda APPROVED.

Fonte: TI AMC1311.  

---

# 2. Canal de tensão — baseline

Cada canal segue:

Lx
→ proteção HV
→ divisor resistivo de alta impedância
→ AMC1311B
→ filtro diferencial
→ ADS131M06
→ STM32G474RE

Para cada fase existem dois conjuntos:

### Zone A
- VA_L1
- VA_L2
- VA_L3

### Zone B
- VB_L1
- VB_L2
- VB_L3

Total: **6 canais de tensão isolados**.

---

# 3. Divisor de tensão — cálculo inicial

O AMC1311B aceita entrada de aproximadamente 2 V no lado de alta impedância.

Para 230 Vrms:

Vpeak ≈ 230 × sqrt(2) ≈ 325.3 V

Objetivo inicial:

Vinput_peak ≈ 1.8 V

Razão:

Rbottom / (Rtop + Rbottom) ≈ 1.8 / 325.3 ≈ 0.00553

Uma implementação inicial de estudo:

Rtop total ≈ 1.8 MΩ  
Rbottom ≈ 10 kΩ

Razão ≈ 0.00552.

A corrente do divisor a 230 Vrms seria aproximadamente:

I ≈ 230 / 1.81 MΩ ≈ 127 µA

Potência total aproximada:

P ≈ 230² / 1.81 MΩ ≈ 29 mW

Estes valores são **calculados para estudo**, não BOM final.

### Por que vários resistores no Rtop

O Rtop deve ser dividido em vários componentes para:
- distribuir tensão;
- distribuir potência;
- aumentar margem contra tensão máxima individual;
- melhorar layout;
- permitir creepage/clearance adequado.

Exemplo arquitetural:

RTA1 + RTA2 + RTA3 + RTA4 + RTA5 + RTA6

O valor individual e o tipo do resistor serão congelados após seleção de tensão de trabalho e requisitos de isolamento da PCB.

---

# 4. Proteção do canal de tensão

Cada canal terá:

1. fusível/limitação upstream conforme arquitetura;
2. resistor limitador;
3. divisor HV;
4. proteção contra surto apropriada;
5. AMC1311B;
6. filtro;
7. clamp secundário;
8. ADC.

O clamp secundário não pode ser usado como substituto da proteção contra sobretensão do domínio HV.

---

# 5. AMC1311B — domínio de alimentação

Cada AMC1311B possui dois domínios:

### High-side
- VDD1;
- GND1;
- divisor de tensão;
- rede HV.

### Low-side
- VDD2;
- GND2;
- saída diferencial;
- ADS131M06.

O isolamento entre os domínios deve ser mantido fisicamente na PCB.

Não colocar vias, cobre ou componentes de baixa tensão atravessando a barreira de isolamento.

A TI especifica para a família AMC1311 isolamento reforçado e apresenta valores de creepage/clearance no encapsulamento; a PCB continua sujeita aos requisitos do sistema completo.

---

# 6. Alimentação isolada do high-side

A alimentação do lado HV do AMC1311B não deve ser assumida como fornecida pelo domínio SELV comum.

Baseline:

24V/5V control
→ DC/DC isolado
→ alimentação high-side do AMC1311B

O DC/DC isolado será selecionado em M2.3 depois de:
- corrente necessária;
- tensão de isolamento;
- capacitância de barreira;
- EMC;
- creepage;
- clearance;
- disponibilidade.

---

# 7. ADS131M06

O ADS131M06 continua como ADC principal.

A ficha atual TI confirma:
- 6 canais;
- 24 bit;
- até 32 kSPS;
- amostragem simultânea;
- SPI;
- referência interna ou externa;
- entradas diferenciais/single-ended.

A escolha de um ADS por zona continua recomendada para manter o mapeamento simples e permitir diagnóstico independente.

---

# 8. Corrente — mudança de estratégia

A avaliação M2.1 mostrou que não devemos congelar o TMCS1100A2 como sensor de 32 A.

Portanto:

**TMCS1100A2 = laboratório/prova de conceito**

Para o protótipo V1:

### Opção A
Sensor Hall com margem >32 A RMS contínuos.

### Opção B
CT de precisão com burden protegido.

### Critério de aprovação
O sensor final deve demonstrar:
- ≥32 A RMS contínuos;
- margem de sobrecarga;
- erro de ganho;
- erro de offset;
- erro de fase;
- deriva térmica;
- isolamento;
- largura de banda;
- repetibilidade.

A escolha final do MPN passa para M2.3 depois de comparar pelo menos uma solução Hall e uma solução CT.

---

# 9. Corrente — CT protection

Se for escolhida solução CT:

CT
→ burden
→ proteção secundária
→ filtro diferencial
→ ADS131M06

É obrigatório impedir condição perigosa de secundário aberto.

O burden deve ser dimensionado considerando:
- corrente máxima;
- relação do CT;
- tensão máxima;
- classe;
- potência;
- frequência;
- saturação.

---

# 10. CP transmitter

Arquitetura:

STM32
→ timer PWM
→ driver CP
→ proteção
→ CP connector

O duty-cycle é configurado pelo firmware, mas o sinal efetivamente entregue ao EVSE é medido por um canal de feedback.

O sistema guarda:
- frequência;
- duty;
- Vmax;
- Vmin;
- offset;
- estado;
- timestamp.

---

# 11. CP receiver

CP recebido:

CP connector
→ proteção
→ divisor/level shifting
→ ADC/comparator
→ MCU

O receptor deve permitir distinguir os estados definidos pela arquitetura IEC 61851.

O software não deve inferir o estado apenas pelo duty-cycle.

---

# 12. PP simulator

Baseline:

MCU
→ driver isolado/protegido
→ rede resistiva selecionável
→ PP connector

A seleção da resistência deve ser feita por componentes dimensionados para:
- tensão;
- corrente;
- dissipação;
- tolerância;
- falha aberta;
- falha em curto.

Fault injection:
- OPEN;
- SHORT;
- VALUE-A;
- VALUE-B;
- VALUE-C.

Cada estado deve ter feedback quando possível.

---

# 13. Contactor driver

Arquitetura:

SAFETY/MCU GPIO
→ resistor gate
→ MOSFET logic-level
→ bobina 24 VDC
→ retorno 0 V

Proteções:
- flyback/TVS;
- gate pulldown;
- current limitation quando necessário;
- feedback de comando;
- proteção contra sobretensão local.

### Regra

O MOSFET não deve ser o único elemento de segurança.

O E-STOP deve interromper a cadeia de energia de forma independente.

---

# 14. Feedback do contactor

Para K_MAIN e K_LOAD:

COMMAND
+
AUXILIARY CONTACT
+
SAFETY INPUT

O firmware recebe o estado, mas a lógica de segurança também deve poder retirar energia.

Tabela:

| Comando | Feedback | Diagnóstico |
|---|---|---|
| OFF | OFF | normal |
| ON | ON | normal |
| OFF | ON | contacto potencialmente soldado |
| ON | OFF | falha de fecho |

---

# 15. 24 VDC protection

Distribuição:

PSU_24V
→ F_SAFE
→ F_CONTROL
→ F_AUX
→ drivers/módulos

Cada ramo deve possuir proteção individual.

Proposta inicial:
- 24V-SAFE: safety MCU + E-stop interface;
- 24V-CONTROL: measurement/communications/CPU;
- 24V-AUX: HMI/fans/auxiliares;
- 24V-COIL: contactors.

Os valores dos fusíveis serão determinados pelo consumo real e capacidade de curto-circuito do barramento.

---

# 16. PCB isolation zones

Layout:

[ HV ] | [ ISOLATION BARRIER ] | [ SELV ]

Não atravessar a barreira com:
- GND;
- power plane;
- clock;
- SPI;
- vias;
- heatsinks metálicos;
- mounting hardware não controlado.

A distância final deve ser calculada segundo tensão, categoria de sobretensão, pollution degree, material group, altitude e isolamento requerido.

---

# 17. Phase measurement

Para reduzir erro de fase:

- todos os canais de uma zona usam aquisição simultânea;
- filtros devem ter resposta conhecida;
- atraso do sensor deve ser caracterizado;
- atraso do amplificador isolado deve ser caracterizado;
- qualquer CT deve ter correção de fase individual;
- firmware guarda coeficientes de calibração.

Modelo:

φcorrected = φmeasured - φsensor - φfilter - φAFE

Os coeficientes serão obtidos na calibração.

---

# 18. Calibração

### Tensão

Referência externa:
- fonte AC calibrada ou instrumento de referência adequado.

Pontos:
- baixa tensão;
- nominal;
- alta faixa de operação.

### Corrente

Fonte de corrente/carga de referência.

Pontos:
- 1 A;
- 5 A;
- 16 A;
- 32 A.

### Fase

Fonte trifásica calibrada.

Pontos:
- 120°;
- variações controladas;
- diferentes frequências dentro da faixa.

O TestStation nunca é a própria referência.

---

# 19. Test fixture

M2.2 define a interface para um fixture externo.

O fixture deve permitir:
- injeção de tensão;
- injeção de corrente;
- referência de fase;
- CP;
- PP;
- CAN;
- fault injection controlado.

O fixture será o elemento usado para verificar:
- ADC;
- front-end;
- calibração;
- firmware;
- diagnóstico.

---

# 20. BOM v0.3

| Ref | Componente | MPN/Família | Estado |
|---|---|---|---|
| U-VSx | Isolated voltage amplifier | TI AMC1311B | CANDIDATE |
| U-ADCx | ADC | TI ADS131M06 | BASELINE |
| U-MCU | Measurement MCU | STM32G474RE | BASELINE |
| U-CP | CP front-end | VAZAO design | DESIGN |
| U-PP | PP front-end | VAZAO design | DESIGN |
| U-CAN | CAN isolation | TI ISO1044 | BASELINE |
| K-MAIN | Contactor | Schneider LC1D32BL | CANDIDATE |
| PS1 | 24 V PSU | Phoenix 2904616 | EVALUATION |
| R-HV | HV resistor network | precision HV | HOLD |
| U-DCISO | Isolated DC/DC | TBD | HOLD |
| I-SENSE | Current sensor | Hall/CT | HOLD |
| Q-DRIVE | Contactor MOSFET | logic-level | HOLD |
| F-* | Secondary protection | TBD | HOLD |

---

# 21. M2.2 engineering holds

Continuam deliberadamente em HOLD:

- sensor final de corrente;
- DC/DC isolado;
- valores finais do divisor;
- resistor MPN;
- proteção HV;
- CP driver final;
- PP resistor MPN;
- MOSFET final;
- fusíveis;
- SPD;
- RCD/RCM;
- contactores finais de todas as posições;
- load stages;
- thermal system.

Não congelar estes componentes apenas para aumentar artificialmente a aparência de progresso.

---

# 22. Verification matrix

| Função | Método | Resultado esperado |
|---|---|---|
| VA voltage | referência externa | erro dentro orçamento |
| VB voltage | referência externa | erro dentro orçamento |
| IA current | referência externa | erro dentro orçamento |
| Phase L1-L2 | fonte trifásica | erro dentro orçamento |
| Phase L2-L3 | fonte trifásica | erro dentro orçamento |
| Phase L3-L1 | fonte trifásica | erro dentro orçamento |
| CP PWM | osciloscópio/referência | frequência/duty corretos |
| CP state | resistor/state fixture | estado correto |
| PP | resistência conhecida | leitura correta |
| K_MAIN | comando + auxiliar | concordância |
| K_LOAD | comando + auxiliar | concordância |
| E_STOP | interrupção física | energia removida |
| Overtemp | simulação | energia removida |
| Watchdog | timeout | safe state |

---

# 23. M2.3 — próximo milestone

**Real Current Sensor + Isolated DC/DC + Protection Values + PCB Front-End**

Entregáveis:
1. comparação quantitativa Hall vs CT;
2. MPN final do sensor;
3. MPN do DC/DC isolado;
4. valores dos divisores;
5. resistor MPNs;
6. proteção HV;
7. CP component-level schematic;
8. PP component-level schematic;
9. MOSFET driver MPN;
10. feedback circuit;
11. BOM v0.4;
12. first PCB placement;
13. creepage/clearance worksheet;
14. calibration fixture BOM;
15. verification procedure v0.2.

**Critério:** passar de “arquitetura detalhada” para “component-level design review”, sem declarar certificação ou segurança de rede antes dos ensaios.

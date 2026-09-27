# VAZAO EVSE TestStation V1 — M2.0
## Component Selection Freeze + Schematic Review + Prototype BOM

**Estado:** M2.0 — engenharia de protótipo  
**Branch:** `feat/charger-hardware-v1`  
**Objetivo:** transformar a arquitetura M1.x numa baseline concreta de componentes, interfaces e BOM para o primeiro protótipo funcional.

> **IMPORTANTE:** esta é uma seleção de protótipo/engenharia. Não constitui aprovação para ligação à rede, certificação, produção ou instalação em campo. Valores de proteção, poder de corte, cablagem, isolamento, coordenação, temperatura e EMC continuam sujeitos aos dados finais do equipamento, instalação e ensaios.

---

## 1. Decisões M2.0

| Bloco | Baseline M2.0 | Estado |
|---|---|---|
| ADC de medição | **TI ADS131M06** | Selecionado para protótipo |
| MCU de medição | **STM32G474RE** | Selecionado |
| Sensor de corrente | **TI TMCS1100A2** como candidato inicial; alternativa por CT de precisão | Selecionado para avaliação |
| CAN-FD | **TI ISO1044** para isolamento do domínio CAN | Selecionado |
| CAN-FD não isolado local | **TI TCAN1044A-Q1** | Candidato |
| Contator de potência | **Schneider TeSys D LC1D32BL**, bobina 24 VDC | Candidato de protótipo |
| PSU 24 VDC | **Phoenix Contact QUINT4-PS/1AC/24DC/10/+ — 2904616** | Selecionado para avaliação |
| PSU alternativa | **Phoenix Contact QUINT-PS/3AC/24DC/10 — 2866705** | Alternativa |
| Medição de tensão | Divisor/resistor de precisão + proteção + isolamento conforme análise final | Em engenharia |
| CP/PP | Front-end dedicado EVSE, isolado/protegido onde necessário | Em engenharia |
| Carga | Banco resistivo/estágios + contactores/SSR adequados à potência | Em engenharia |
| Safety MCU | STM32G0/G4-class | Baseline, MPN final em M2.1 |
| Proteções AC | Definidas por estudo de curto-circuito/coordenação | **HOLD** |
| SPD | Classe/tipo e Up definidos após cenário de instalação | **HOLD** |
| RCD/monitorização residual | Definição conforme arquitetura final e requisitos aplicáveis | **HOLD** |

---

## 2. ADC — ADS131M06

O **ADS131M06** é a escolha principal para o protótipo de medição.

Características relevantes do fabricante:
- 6 canais;
- 24 bit;
- amostragem simultânea;
- até 32 kSPS;
- PGA configurável;
- referência interna de baixo drift;
- calibração de ganho/offset;
- calibração de atraso de fase entre canais.

A arquitetura usa os seis canais para a medição sincronizada mínima:

- CH0 = VA_L1
- CH1 = VA_L2
- CH2 = VA_L3
- CH3 = IA_L1
- CH4 = IA_L2
- CH5 = IA_L3

Para a **Zone B**, a primeira implementação pode usar um segundo ADS131M06, mantendo a mesma referência temporal do sistema.

**Regra de projeto:** não usar a diferença de fase entre ADCs independentes sem uma estratégia explícita de sincronização e calibração.

Fonte fabricante:  
https://www.ti.com/product/ADS131M06

---

## 3. MCU de medição — STM32G474RE

O **STM32G474RE** fica definido como MCU principal do domínio TS-MEASURE.

Razões:
- Cortex-M4 até 170 MHz;
- FPU;
- DSP;
- até 512 KB Flash;
- até 128 KB SRAM na família;
- periféricos analógicos e temporizadores adequados a aquisição/controlo;
- margem suficiente para cálculo de RMS, potência, energia, frequência e fase.

Responsabilidades:
1. controlar ADC;
2. receber amostras;
3. aplicar calibração;
4. calcular RMS;
5. calcular potência ativa;
6. calcular potência aparente;
7. calcular fator de potência;
8. calcular frequência;
9. calcular fase;
10. detetar clipping/saturação;
11. validar integridade dos sensores;
12. enviar dados para o computador principal;
13. disponibilizar dados brutos quando solicitado.

Fonte fabricante:  
https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html

---

## 4. Sensor de corrente — TMCS1100A2

O **TI TMCS1100A2** é o primeiro candidato para corrente AC.

Características relevantes:
- sensor Hall galvanicamente isolado;
- medição AC/DC;
- working isolation voltage até 600 V;
- 80 kHz de largura de banda;
- erro total especificado inferior a 1% na faixa indicada pelo fabricante;
- versão A2 com sensibilidade nominal de 100 mV/A.

### HOLD importante

O TMCS1100A2 tem corrente contínua máxima especificada pelo fabricante de 30 A no conjunto da família apresentada na página de produto. Como o TestStation V1 pretende atingir **32 A/fase**, não fica aprovado como sensor final de 32 A.

Portanto:

**TMCS1100A2 = sensor de bancada/protótipo para avaliação.**

Antes de congelar o sensor V1:
- verificar corrente RMS contínua de 32 A;
- verificar sobrecarga;
- verificar temperatura;
- verificar erro no fundo de escala;
- verificar dissipação;
- verificar comportamento de pico;
- validar fase do sensor;
- comparar contra instrumento de referência.

Se necessário, o sensor final será substituído por uma variante/família com margem térmica e de corrente adequada ou por CT de precisão.

Fonte fabricante:  
https://www.ti.com/product/TMCS1100

---

## 5. CAN-FD

### 5.1 CAN isolado — ISO1044

O **TI ISO1044** é o candidato principal para o interface entre o domínio de controlo/medição e nós CAN que necessitem de isolamento.

Características relevantes:
- CAN FD;
- até 5 Mbps;
- isolamento galvânico;
- tensão de isolamento especificada pelo fabricante;
- proteção de falha no barramento;
- operação industrial.

Fonte fabricante:  
https://www.ti.com/product/ISO1044

### 5.2 CAN local — TCAN1044A-Q1

O **TCAN1044A-Q1** pode ser utilizado onde o isolamento não seja necessário e existe vantagem numa camada física CAN-FD robusta.

Características:
- CAN clássico e CAN FD;
- até 8 Mbps em condições adequadas;
- proteção de falha do barramento ±58 V;
- timeout TXD dominante;
- proteção térmica;
- alimentação lógica configurável.

Fonte fabricante:  
https://www.ti.com/product/TCAN1044A-Q1

---

## 6. Contator de potência — LC1D32BL

Baseline de protótipo:

**Schneider Electric TeSys D LC1D32BL**
- 3 polos;
- 32 A AC-3;
- 50 A AC-1;
- bobina 24 VDC;
- contacto auxiliar;
- utilização adequada para avaliação da comutação de carga resistiva dentro das condições especificadas.

Para o TestStation, o regime **AC-1** é particularmente relevante quando o elemento comutado é uma carga resistiva, mas a seleção final depende do perfil real da carga, número de operações, corrente de pico, temperatura e coordenação.

Fonte Schneider / documentação de referência:
https://www.se.com/

### Regra

O LC1D32BL não fica automaticamente aprovado para todas as funções K_MAIN/K_ZONE/K_LOAD.

Cada posição deve ser avaliada separadamente quanto a:
- corrente;
- categoria de utilização;
- tensão;
- frequência;
- curto-circuito presumido;
- coordenação;
- número de operações;
- dissipação;
- contacto auxiliar;
- estado seguro em perda de comando.

---

## 7. Alimentação 24 VDC

Baseline:

**Phoenix Contact QUINT4-PS/1AC/24DC/10/+ — 2904616**

Características relevantes:
- entrada 100–240 VAC;
- saída 24 VDC;
- 10 A nominal;
- arquitetura industrial DIN rail;
- SFB;
- monitorização;
- margem para picos conforme configuração.

A opção 10 A é coerente com a estimativa inicial M1.8 de aproximadamente 11 A apenas se o orçamento real for revisto. Portanto, **não se assume que 10 A é suficiente**.

### Decisão de engenharia

Antes do protótipo final:
1. medir consumo real de todos os módulos;
2. separar cargas permanentes e cargas de pico;
3. incluir bobinas;
4. incluir ventilação;
5. incluir iluminação/HMI;
6. incluir margem térmica;
7. calcular corrente de arranque;
8. validar seletividade dos fusíveis secundários.

Se a medição ultrapassar o orçamento, migrar para uma PSU de maior capacidade.

Alternativa já documentada:

**Phoenix Contact QUINT-PS/3AC/24DC/10 — 2866705**, com 10 A nominal e Power Boost até 15 A nas condições indicadas pelo fabricante.

Fontes:
https://www.phoenixcontact.com/pt-pt/produtos/power-supply-unit-quint4-ps-1ac-24dc-10-2904616
https://www.phoenixcontact.com/gb/products/2866705/pdf

---

## 8. Medição de tensão

A medição das tensões L1/L2/L3 não será feita diretamente no ADC.

Cada canal deve conter, no mínimo:

**rede → proteção → limitação de energia → divisor/transformação apropriada → filtro → proteção de entrada → ADC**

Para cada fase:
- VA_L1
- VA_L2
- VA_L3
- VB_L1
- VB_L2
- VB_L3

### Requisitos

- isolamento conforme arquitetura;
- resistor network de precisão;
- tensão nominal compatível;
- impulso e creepage/clearance adequados;
- proteção contra sobretensão;
- filtro com fase conhecida;
- calibração individual;
- identificação da contribuição do filtro para erro de fase.

**HOLD:** valores finais dos divisores, fusíveis, resistores e filtros serão definidos em M2.1 após escolha da faixa de medição e classe de segurança.

---

## 9. Medição de fase

A medição de fase é uma função principal do TestStation.

Para cada zona:

- φ(L1,L2)
- φ(L2,L3)
- φ(L3,L1)

E, adicionalmente, para cada fase tensão/corrente:

- φ(VL1,IL1)
- φ(VL2,IL2)
- φ(VL3,IL3)

O sistema deve armazenar:
- valor bruto;
- valor calibrado;
- incerteza estimada;
- frequência;
- timestamp;
- estado da aquisição;
- estado do sensor;
- qualidade do sinal.

O relatório não deve apresentar simplesmente “fase OK/FAIL”. Deve apresentar a medição e o intervalo/critério aplicado.

---

## 10. Zone A / Zone B

### Zone A — entrada

Representa o estado elétrico **antes do EVSE**.

Mede:
- tensão;
- corrente quando aplicável;
- frequência;
- sequência de fases;
- fase;
- potência.

### Zone B — lado EVSE

Representa o estado elétrico **depois do ponto de comutação/EVSE definido na arquitetura**.

Mede os mesmos parâmetros.

### Diagnóstico

O motor de diagnóstico compara:

`ZoneA → ZoneB`

Classificação:

1. **FACT** — valor efetivamente medido;
2. **ANOMALY** — diferença fora do critério;
3. **HYPOTHESIS** — causa possível;
4. **TEST** — ensaio recomendado;
5. **RECOMMENDATION** — ação técnica possível.

Nunca converter automaticamente uma hipótese em diagnóstico confirmado.

---

## 11. CP / PP

O módulo TS-EV deverá permitir:

- geração de CP;
- leitura de CP;
- geração/leitura PWM;
- estados IEC 61851;
- deteção de presença;
- PP;
- simulação de diferentes correntes máximas;
- deteção de falhas;
- testes de continuidade/PE conforme arquitetura;
- registo temporal do comportamento.

O circuito deve ser isolado/protegido relativamente ao domínio de potência.

### Objetivo V1

Permitir validar o comportamento do EVSE sem necessitar de um veículo real.

---

## 12. Carga eletrónica

O M2.0 não congela ainda um único componente para a carga de 22 kW.

Razão:

22 kW convertidos integralmente em calor representam aproximadamente:

**22 000 W térmicos**

Isto transforma a carga num subsistema térmico e elétrico significativo.

### Estratégia

Dividir a carga em estágios:

- LOAD-1
- LOAD-2
- LOAD-3
- LOAD-N

Cada estágio deve possuir:
- proteção;
- comutação;
- feedback;
- sensor térmico;
- contacto auxiliar/estado quando aplicável;
- desligamento independente de segurança.

O software deverá comandar potência através de um **setpoint**, mas o hardware de segurança deve poder remover a potência independentemente do software.

---

## 13. Safety

A cadeia mínima permanece:

`E_STOP → SAFETY_LOGIC → K_MAIN/K_LOAD → LOAD`

O computador principal não pode ser o único elemento responsável por retirar energia.

Entradas:
- E_STOP;
- DOOR_INTERLOCK;
- LOAD_OVERTEMP;
- CONTACTOR_FB;
- POWER_FAULT;
- WATCHDOG.

Saídas:
- K_MAIN;
- K_ZONE_A;
- K_ZONE_B;
- K_LOAD;
- FAN_ENABLE;
- SAFE_STATUS.

### Contactor feedback

Para cada contactor crítico:

`COMMAND` ≠ `FEEDBACK`

deve gerar estado de falha.

Exemplos:
- comando OFF + contacto ainda fechado → possível contacto soldado;
- comando ON + contacto não fechado → possível falha de bobina/contator/cablagem.

---

## 14. BOM M2.0 — estrutura

| Ref. | Quant. | Componente | MPN / família | Estado |
|---|---:|---|---|---|
| U-MEASURE-01 | 1 | ADC simultâneo | TI ADS131M06 | **SELECTED** |
| U-MEASURE-02 | 1 | MCU medição | STM32G474RE | **SELECTED** |
| U-MEASURE-03..05 | 3 | Sensor corrente | TMCS1100A2 | **EVALUATION** |
| U-CAN-01 | 1+ | CAN isolado | TI ISO1044 | **SELECTED** |
| U-CAN-02 | 1+ | CAN-FD local | TI TCAN1044A-Q1 | **CANDIDATE** |
| K-MAIN-01 | 1 | Contator 3P | Schneider LC1D32BL | **CANDIDATE** |
| PS1 | 1 | PSU 24 VDC | Phoenix 2904616 | **EVALUATION** |
| PS2 | 1 | PSU alternativa | Phoenix 2866705 | **ALTERNATIVE** |
| U-SAFE-01 | 1 | Safety MCU | STM32G0/G4 family | **HOLD MPN** |
| U-EV-01 | 1 | CP/PP front-end | dedicated VAZAO design | **DESIGN** |
| LOAD-01..N | N | Load stages | resistive/protected | **DESIGN** |
| QF* | N | Proteção AC | TBD | **HOLD** |
| SPD* | N | SPD | TBD | **HOLD** |
| F* | N | Fusíveis | TBD | **HOLD** |
| S* | N | sensores térmicos | TBD | **HOLD** |
| J* | N | conectores | industrial family TBD | **HOLD** |

---

## 15. MPN approval gates

Um MPN só passa de **CANDIDATE** para **APPROVED FOR PROTOTYPE** depois de:

- datasheet arquivado;
- rating verificado;
- disponibilidade confirmada;
- footprint/CAD confirmado;
- temperatura verificada;
- isolamento verificado;
- creepage/clearance verificados;
- corrente/tensão verificadas;
- comportamento de falha analisado;
- alternativa identificada quando o componente for crítico.

Para componentes de segurança ou potência, também:
- coordenação;
- SCCR/Icc;
- curto-circuito presumido;
- proteção upstream;
- ensaio térmico;
- ensaio de falha.

---

## 16. Schematic review — M2.0

A revisão dos esquemas M1.9 passa a ter estes pontos obrigatórios:

### Sheet 01 — SINGLE-LINE-POWER
- entrada;
- isolamento;
- proteção;
- K_MAIN;
- Zone A;
- Zone B;
- K_LOAD;
- PE;
- N;
- pontos de medição.

### Sheet 02 — INPUT-PROTECTION
- proteção contra curto;
- SPD;
- coordenação;
- seccionamento;
- hold points.

### Sheet 09 — MEASUREMENT
- ADS131M06;
- 6 canais;
- referência;
- clock;
- SPI;
- proteção;
- calibração.

### Sheet 10 — EV-CP-PP
- CP;
- PP;
- PWM;
- IEC 61851;
- fault injection;
- isolamento/proteção.

### Sheet 07 — SAFETY-ESTOP
- E-stop;
- watchdog;
- feedback;
- contactor drive;
- safe state.

---

## 17. O que fica deliberadamente por decidir

Não vamos inventar valores só para fechar uma BOM.

**HOLD M2.1:**
- disjuntor principal;
- fusíveis;
- SPD;
- RCD/RCM;
- secção dos condutores;
- bornes de potência;
- sensores finais de corrente;
- divisores de tensão;
- isolação da medição;
- contactores finais K_ZONE_A/K_ZONE_B/K_LOAD;
- tecnologia final da carga;
- ventiladores;
- sensores térmicos;
- conectores EV;
- creepage/clearance de PCB;
- gabinete;
- dissipação;
- EMC filtering.

Estes valores dependem da configuração elétrica final, poder de curto-circuito, arquitetura de carga e resultados dos cálculos/ensaios.

---

## 18. Próximo milestone — M2.1

**M2.1 — Protection Coordination + Sensor Front-End + CP/PP Schematic**

Entregáveis:
1. seleção final preliminar dos sensores;
2. circuito de entrada de tensão;
3. circuito completo dos 6 canais ADC;
4. calibração de ganho/offset/fase;
5. proteção das entradas;
6. CP/PP schematic;
7. driver dos contactores;
8. cálculo de corrente das bobinas;
9. 24 VDC load budget;
10. primeira matriz de proteção;
11. first-pass creepage/clearance;
12. BOM v0.2;
13. datasheet register;
14. prototype purchasing list.

**Critério de passagem:** nenhum componente crítico de segurança ou potência passa a “APPROVED” sem datasheet + cálculo + revisão.

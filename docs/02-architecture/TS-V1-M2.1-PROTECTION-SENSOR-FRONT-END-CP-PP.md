# VAZAO EVSE TestStation V1 — M2.1
## Protection Coordination + Sensor Front-End + CP/PP Schematic Baseline

**Estado:** M2.1 — engenharia detalhada de protótipo  
**Branch:** feat/charger-hardware-v1  
**Dependências:** M1.9 + M2.0  
**Objetivo:** fechar a primeira implementação elétrica dos front-ends de medição, CP/PP, drivers de contactores e orçamento 24 VDC, mantendo em HOLD tudo o que depende de dados finais de instalação/curto-circuito.

> NOTA DE SEGURANÇA: este documento é uma baseline de engenharia para protótipo. Não autoriza ligação direta à rede nem substitui cálculo de curto-circuito, coordenação, isolamento, ensaio, certificação ou revisão por engenheiro qualificado.

---

## 1. Decisões M2.1

| Bloco | Decisão | Estado |
|---|---|---|
| ADC | TI ADS131M06 | BASELINE |
| ADC por zona | 1 ADC por zona | BASELINE |
| MCU medição | STM32G474RE | BASELINE |
| Aquisição | simultânea, tensão + corrente | BASELINE |
| Sensor corrente | Hall/CT a validar; TMCS1100A2 apenas avaliação | HOLD FINAL |
| Entrada tensão | divisor isolado/protegido ou transdutor isolado | HOLD FINAL |
| Referência ADC | referência interna ADS131M06 no protótipo inicial | BASELINE |
| Clock ADC | clock comum por domínio; sincronização entre ADCs | BASELINE |
| CP | front-end dedicado + isolamento/proteção | BASELINE |
| PP | ADC/GPIO protegido + rede de simulação | BASELINE |
| Driver K* | MOSFET low-side + proteção de bobina + feedback | BASELINE |
| Safety | corte de hardware independente do PC | BASELINE |
| PSU | 24 VDC industrial | BASELINE |
| Proteção AC | estudo de Icc + coordenação | HOLD |
| SPD | seleção dependente da instalação | HOLD |
| RCD/RCM | seleção dependente da arquitetura e requisitos | HOLD |
| Carga 22 kW | estágios independentes + segurança térmica | BASELINE |

---

## 2. Medição — arquitetura elétrica

### 2.1 Zone A

Canais do ADS131M06-A:
- CH0 = VA_L1
- CH1 = VA_L2
- CH2 = VA_L3
- CH3 = IA_L1
- CH4 = IA_L2
- CH5 = IA_L3

### 2.2 Zone B

ADS131M06-B:
- CH0 = VB_L1
- CH1 = VB_L2
- CH2 = VB_L3
- CH3 = IB_L1
- CH4 = IB_L2
- CH5 = IB_L3

A escolha do ADS131M06 é adequada à arquitetura porque o componente possui seis canais simultâneos, 24 bit, até 32 kSPS e calibração de atraso de fase entre canais. O fabricante também especifica entradas diferenciais/single-ended e possibilidade de ligação a divisores resistivos, CT ou Rogowski, mas a rede analógica final continua dependente do sensor escolhido.

Fonte: TI ADS131M06.

---

## 3. Front-end de tensão

Cada fase segue o conceito:

Lx → proteção primária → limitador de energia → divisor/isolação → filtro RC → proteção ADC → ADS131M06

Não ligar a rede diretamente ao ADC.

### 3.1 Requisitos do divisor

O divisor deve ser dimensionado para:
1. tensão nominal;
2. sobretensão temporária;
3. sobretensão transitória;
4. tensão máxima de entrada do ADC;
5. potência dissipada;
6. tolerância;
7. coeficiente térmico;
8. tensão máxima por resistor;
9. creepage;
10. clearance.

### 3.2 Regra de projeto

Preferir uma cadeia de vários resistores em série no braço de alta tensão em vez de um único resistor de alto valor, quando necessário para cumprir tensão de trabalho e requisitos de isolamento.

### 3.3 Proteção secundária

Depois do divisor:
- resistor série;
- filtro anti-alias;
- clamp apropriado;
- proteção ESD/transiente quando necessário;
- ponto de teste.

O clamp nunca deve ser dimensionado como substituto da proteção primária.

---

## 4. Front-end de corrente

### 4.1 Opção A — Hall

Arquitetura:

Condutor → sensor Hall → filtro → ADS131M06

Vantagens:
- isolamento;
- medição AC/DC;
- sem shunt diretamente no caminho de potência.

### 4.2 Opção B — CT

Arquitetura:

Condutor → CT → burden → filtro → ADS131M06

Requisitos adicionais:
- burden dimensionado;
- proteção contra circuito aberto;
- fase conhecida;
- saturação analisada;
- corrente máxima;
- classe/erro;
- temperatura.

### 4.3 TMCS1100A2

Continua apenas como componente de avaliação.

Não é aprovado como sensor final de 32 A sem validação específica de margem térmica/corrente.

---

## 5. Aquisição e sincronização

O ADS131M06 oferece seis canais de amostragem simultânea e mecanismo de calibração de atraso de fase.

### 5.1 Clock

Todos os canais de uma zona usam o mesmo clock.

Para Zone A e Zone B:
- clock comum ou relação determinística;
- timestamp comum;
- sincronização de início;
- calibração de offset temporal.

### 5.2 Regra de fase

Não calcular fase a partir de sinais adquiridos em instantes diferentes sem compensação.

O software deve guardar:
- timestamp;
- sample index;
- frequência;
- taxa de amostragem;
- configuração PGA;
- estado de sincronização.

---

## 6. Cálculos elétricos

RMS:

Vrms = sqrt(mean(v²))

Irms = sqrt(mean(i²))

Potência ativa:

P = mean(v × i)

Potência aparente:

S = Vrms × Irms

Fator de potência:

PF = P/S

Energia:

E = integral(P dt)

Ângulo V/I:

O algoritmo inicial deve usar correlação/cross-spectrum ou método equivalente com compensação de atraso conhecido.

O relatório deve distinguir:
- displacement angle;
- power factor;
- distortion effects.

Não assumir PF = cos(φ) quando houver distorção significativa.

---

## 7. Fase L1/L2/L3

Para cada zona:
- φ12 = angle(VL1,VL2)
- φ23 = angle(VL2,VL3)
- φ31 = angle(VL3,VL1)

A análise deve incluir sequência de fases.

### Estado de exemplo

Entrada:
- φ12 = 120.1°
- φ23 = 119.8°
- φ31 = 120.1°

Não classificar apenas pelo valor absoluto.

Comparar ZoneB - ZoneA e a incerteza combinada.

---

## 8. Cálculo de incerteza

Para uma diferença de fase:

uΔφ = sqrt(uA² + uB² + uref² + usensor² + ualg²)

Quando as contribuições forem correlacionadas, aplicar a matriz de covariância adequada.

O sistema deve apresentar:
- medição;
- incerteza;
- limite aplicado;
- origem do limite.

Nunca usar um limite arbitrário de “1 grau” como regra universal.

---

## 9. CP — arquitetura

O CP deve possuir:
- geração PWM;
- leitura do nível;
- proteção contra sobretensão;
- proteção contra curto;
- isolamento apropriado relativamente ao domínio de potência;
- medição da amplitude;
- frequência;
- duty cycle;
- estado IEC 61851.

### 9.1 PWM

O MCU gera o sinal de referência.

O front-end deverá garantir:
- amplitude correta;
- duty-cycle mensurável;
- frequência estável;
- proteção do pino MCU;
- estado seguro em reset.

### 9.2 Feedback

O sinal que sai para o EVSE deve ser medido de volta.

Assim:

CP_COMMAND ≠ CP_ASSUMED

O TestStation deve validar o CP real.

---

## 10. PP — arquitetura

PP deve permitir:
- leitura;
- identificação de estados;
- simulação de resistência conforme configuração;
- seleção por relé/analógico protegido;
- deteção de circuito aberto;
- diagnóstico de curto.

A rede PP deve possuir proteção contra erro de ligação.

---

## 11. Fault Injection

Fault injection não deve depender apenas de software.

O hardware deve disponibilizar caminhos controlados para:
- CP open;
- CP abnormal;
- PP open;
- PP abnormal;
- comunicação perdida;
- contactor feedback mismatch;
- overtemperature;
- emergency stop.

Cada falha deve possuir:
- ID;
- pré-condição;
- método;
- timeout;
- safe state;
- critério de recuperação.

---

## 12. Driver de contactores

Baseline:

MCU/SAFETY → isolação lógica quando necessária → gate driver/MOSFET → bobina K

Cada bobina deve possuir proteção adequada à tecnologia escolhida.

Para bobina DC:
- flyback adequado;
- TVS quando necessário para desligamento rápido;
- limitação de corrente;
- diagnóstico de alimentação.

### Feedback

Cada contactor crítico deve possuir feedback independente do comando.

| Command | Feedback | Estado |
|---|---|---|
| OFF | OFF | SAFE |
| ON | ON | ENERGIZED |
| OFF | ON | WELDED/FAULT |
| ON | OFF | FAILED-TO-CLOSE |

---

## 13. Safety chain

A cadeia deve continuar funcional mesmo que o computador principal:
- bloqueie;
- reinicie;
- perca comunicação;
- tenha firmware defeituoso;
- perca alimentação de controlo.

Entradas:
- E_STOP;
- DOOR;
- OVERTEMP;
- CONTACTOR_FB;
- POWER_FAULT;
- SAFETY_WATCHDOG.

Saídas:
- K_MAIN;
- K_LOAD;
- FAN_ENABLE;
- SAFE_STATUS.

---

## 14. 24 VDC budget

A PSU Phoenix Contact 2904616 fornece 24 VDC/10 A nominal, com 12,5 A de static boost e 20 A de dynamic boost durante 5 s segundo a documentação atual do fabricante. A seleção final continua dependente do consumo medido e do duty cycle dos picos.

### Budget preliminar

| Carga | Corrente alvo |
|---|---:|
| Safety MCU + I/O | 0.25 A |
| Measurement electronics | 0.50 A |
| Main computer/DC-DC | 2.50 A |
| CAN/communications | 0.25 A |
| CP/PP | 0.50 A |
| HMI/indicators | 0.75 A |
| Fans | 1.50 A |
| Contactor coils | 1.50 A |
| Service margin | 1.50 A |
| **Total preliminar** | **9.25 A** |

Este valor é deliberadamente inferior a 10 A apenas por 0,75 A. Portanto, a PSU 10 A não fica congelada como solução final.

Se o computador ou ventilação exigirem mais potência, migrar para uma PSU de maior corrente ou separar:
- 24V-SAFE;
- 24V-CONTROL;
- 24V-AUX.

---

## 15. Proteção da PSU

A PSU possui proteção interna e recomendações específicas do fabricante para proteção de entrada. A seleção do dispositivo upstream deve seguir a documentação do fabricante e a coordenação do quadro do TestStation.

Não copiar automaticamente um disjuntor de catálogo para a entrada geral do TestStation.

---

## 16. Proteção de potência AC

### HOLD

Não fechar ainda:
- QF1;
- fusíveis;
- SPD;
- RCD/RCM;
- poder de corte;
- seletividade;
- SCCR/Icc.

Precisamos de:
1. sistema de alimentação;
2. tensão;
3. esquema de ligação à terra;
4. Icc presumida;
5. comprimento dos condutores;
6. secção;
7. método de instalação;
8. temperatura;
9. número de circuitos;
10. categoria de utilização;
11. arquitetura da carga.

---

## 17. Carga 22 kW

Para 22 kW trifásicos a 400 V:

I ≈ 22000/(sqrt(3)×400) ≈ 31.75 A

Este valor é a referência nominal para carga resistiva equilibrada a PF≈1.

A carga real deverá ser dividida em vários estágios.

Exemplo arquitetural:
- Stage A ≈ 5.5 kW
- Stage B ≈ 5.5 kW
- Stage C ≈ 5.5 kW
- Stage D ≈ 5.5 kW

Estes valores são arquitetura de referência, não componentes finais.

Cada estágio necessita de:
- proteção;
- contactor/SSR apropriado;
- sensor térmico;
- feedback;
- desligamento de segurança.

---

## 18. Thermal safety

A carga de 22 kW pode dissipar aproximadamente 22 kW de calor quando totalmente resistiva.

Consequentemente:

LOAD_ENABLE = TRUE

só pode permanecer ativo enquanto:
- temperatura < limite;
- ventilação OK;
- contactors OK;
- E_STOP OK;
- safety watchdog OK;
- airflow OK.

Uma falha térmica deve remover a energia da carga independentemente do PC.

---

## 19. PCB partition

### TS-MEASURE
Contém:
- ADS131M06;
- referência;
- ADC clock;
- filtros;
- sensores;
- MCU;
- SPI;
- isolamento de comunicação.

### TS-SAFE
Contém:
- safety MCU;
- watchdog;
- E-stop interface;
- contactor drivers;
- feedback;
- safety I/O.

### TS-EV
Contém:
- CP;
- PP;
- PWM;
- fault injection;
- proteção.

### TS-LOAD

Preferencialmente fora da PCB de sinal:
- contactores;
- SSR;
- potência;
- sensores térmicos;
- feedback.

---

## 20. Creepage / clearance

A seleção final das PCB deve ser baseada em:
- tensão de trabalho;
- sobretensão;
- pollution degree;
- material group;
- altitude;
- isolamento requerido;
- barreiras;
- slots;
- coating, quando aplicável.

Não fixar uma única distância em M2.1 sem esses dados.

---

## 21. Test points

Obrigatórios:

### Measurement
- TP-VA1
- TP-VA2
- TP-VA3
- TP-IA1
- TP-IA2
- TP-IA3
- ADC_REF
- ADC_CLK
- ADC_SYNC

### Safety
- SAFE_24V
- E_STOP
- K_MAIN_FB
- K_LOAD_FB
- WATCHDOG

### EV
- CP_RAW
- CP_PWM
- PP_RAW

### Communications
- CAN_H
- CAN_L
- UART_SERVICE

---

## 22. Calibration interface

O TestStation deve possuir connector dedicado:

J_CAL

para ligação a equipamento externo de referência.

Não calibrar o instrumento usando os seus próprios valores como referência.

Calibração mínima:
- tensão L1/L2/L3;
- corrente L1/L2/L3;
- offset;
- ganho;
- fase;
- frequência.

Guardar:
- serial;
- data;
- operador;
- instrumento de referência;
- certificado;
- valores antes;
- valores depois;
- firmware;
- hardware revision.

---

## 23. Diagnóstico inteligente

O motor de diagnóstico recebe:

RAW → CALIBRATED → DERIVED → ANOMALY → HYPOTHESIS → TEST → RECOMMENDATION

Exemplo:

FACT
- Zone A φ12 = 120.0°
- Zone B φ12 = 116.8°

ANOMALY
- Δφ = -3.2°

HYPOTHESES
- sensor mismatch;
- filter phase error;
- wiring/reference problem;
- EVSE power-stage influence.

TESTS
1. repetir aquisição;
2. verificar frequência;
3. executar zero/load reference;
4. comparar com instrumento externo;
5. verificar sequência de fases;
6. isolar EVSE.

Só depois pode surgir uma recomendação.

---

## 24. Capacitor correction

O sistema pode calcular uma candidatura de correção de fator de potência/correção de fase quando os dados justificarem.

Nunca apresentar “Instalar capacitor X” sem verificar:
- tensão nominal;
- frequência;
- potência;
- harmónicos;
- risco de ressonância;
- corrente;
- duty cycle;
- switching;
- discharge;
- temperatura;
- norma aplicável.

O resultado deverá ser:

**Candidato calculado — requer validação de engenharia.**

---

## 25. M2.1 exit criteria

M2.1 só fica fechado quando:
- [x] arquitetura de 6 canais definida;
- [x] ADC definido;
- [x] MCU definido;
- [x] sincronização definida;
- [x] algoritmo elétrico inicial definido;
- [x] CP/PP architecture definida;
- [x] contactor driver architecture definida;
- [x] safety chain definida;
- [x] 24 V budget inicial calculado;
- [ ] sensor final 32 A validado;
- [ ] front-end de tensão calculado;
- [ ] proteção AC coordenada;
- [ ] SPD definido;
- [ ] RCD/RCM definido;
- [ ] carga final definida;
- [ ] thermal design validado;
- [ ] creepage/clearance final calculado.

Os itens em HOLD passam para M2.2/M2.3 conforme dependências.

---

## 26. Próximo milestone

### M2.2 — Real Sensor Front-End + CP/PP Detailed Schematic

Entregáveis:
1. MPN final do sensor de corrente;
2. circuito elétrico completo de VA/VB;
3. valores preliminares dos divisores;
4. filtros RC;
5. proteção de entrada;
6. ADC reference/clock;
7. SPI + CRC;
8. CP transmitter;
9. CP receiver;
10. PP simulator;
11. fault injection;
12. contactor MOSFET drivers;
13. feedback inputs;
14. 24 V protection;
15. PCB isolation zones;
16. BOM v0.3;
17. test fixture;
18. calibration procedure v0.1.

M2.2 continua a privilegiar componentes reais e datasheets verificáveis, sem transformar um protótipo documental em equipamento certificado.

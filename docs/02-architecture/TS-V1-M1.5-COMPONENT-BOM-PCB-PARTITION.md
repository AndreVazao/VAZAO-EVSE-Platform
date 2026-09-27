# TS-V1-M1.5 — Component Selection, Protection & PCB Partition

**Produto:** VAZAO EVSE TestStation V1  
**Estado:** Baseline preliminar de engenharia — NÃO aprovado para aquisição/produção  
**Escopo:** AC monofásico/trifásico, 230/400 VAC, até 32 A/fase, até 22 kW.

## 1. Objetivo

Transformar a arquitetura M1.4 numa baseline concreta de seleção de componentes, proteção e particionamento de PCB, mantendo separação entre potência perigosa, medição, segurança, controlo EV e carga eletrónica.

Esta documentação é uma base de engenharia. A seleção final depende das condições reais de instalação, corrente de curto-circuito presumida, categoria de sobretensão, temperatura, isolamento, EMC, duty cycle, normas aplicáveis e validação dos datasheets.

## 2. Princípio de seleção

Os componentes abaixo são famílias/candidatos de engenharia. Nenhum componente é considerado automaticamente aprovado para produção.

Critérios obrigatórios:
- tensão e corrente reais de operação;
- categoria de sobretensão e grau de poluição;
- isolamento e creepage/clearance;
- temperatura e dissipação;
- corrente de curto-circuito e capacidade de interrupção;
- duty cycle;
- EMC;
- disponibilidade e ciclo de vida;
- calibração e rastreabilidade;
- requisitos de certificação do produto final.

## 3. TS-MEASURE — medição sincronizada

### 3.1 ADC principal

**Candidato:** TI ADS131M06-class ou equivalente.

Função:
- aquisição simultânea de múltiplos canais;
- tensão L1/L2/L3;
- corrente L1/L2/L3;
- preservação da relação temporal entre canais;
- aquisição de formas de onda para diagnóstico de fase, potência e harmónicos.

Direção de engenharia:
- preferir ADC simultâneo quando o diagnóstico de deslocamento de fase for uma função principal;
- manter interface digital determinística com MCU;
- usar referência de tensão de precisão;
- prever filtragem analógica e proteção de entrada antes do ADC.

**Alternativa/benchmark:** Analog Devices ADE9000-class ou equivalente, caso a arquitetura dedicada de metrologia seja mais vantajosa após comparação de erro, firmware e certificação.

### 3.2 MCU de medição

**Candidato:** STM32G4-class ou equivalente.

Requisitos:
- SPI de alta velocidade;
- DMA;
- temporizadores de precisão;
- RAM suficiente para janelas de waveform;
- CAN-FD;
- watchdog;
- UART/service interface;
- processamento determinístico de RMS, potência, energia e fase.

Funções:
- aquisição;
- filtragem;
- compensação de ganho/offset;
- compensação de fase;
- cálculo de RMS;
- potência ativa/reativa/aparente;
- energia;
- sequência de fases;
- ângulos L1-L2, L2-L3 e L3-L1;
- publicação dos dados para o computador principal.

### 3.3 Sensores de corrente

Devem ser avaliadas duas arquiteturas:

**Hall industrial**
- isolamento galvânico natural;
- boa integração mecânica;
- resposta adequada para aquisição de waveform;
- verificar offset, drift térmico e largura de banda.

**Transformador de corrente**
- excelente isolamento;
- adequado para AC;
- boa estabilidade para medição AC;
- exige atenção a burden, saturação, fase e proteção do secundário.

A seleção final deve ser feita depois de comparar erro de amplitude, erro de fase, largura de banda, temperatura e integração mecânica.

### 3.4 Medição de tensão

Cada fase terá canal de medição isolado ou uma topologia de entrada devidamente isolada e protegida.

Requisitos:
- resistorização de alta tensão apropriada;
- proteção contra surtos;
- filtragem;
- isolamento compatível com a categoria do equipamento;
- baixo erro de ganho;
- baixo erro de fase;
- capacidade de suportar transientes especificados.

### 3.5 Referência

**Candidato:** família ADR45xx-class ou equivalente.

A referência deve ser dimensionada em conjunto com ADC, temperatura, ruído, deriva e estratégia de calibração.

## 4. TS-SAFE — segurança

### 4.1 MCU de segurança

**Candidato:** STM32G0/G4-class ou equivalente.

A MCU não substitui a cadeia de segurança por hardware.

Arquitetura:
- E-stop físico;
- interlocks;
- comando de contactores;
- leitura de contactos auxiliares;
- watchdog externo;
- heartbeat;
- deteção de estado incoerente;
- corte de potência em condição insegura.

### 4.2 Contactores

Famílias industriais Schneider Electric, ABB, Siemens ou Eaton podem ser usadas como candidatos.

A seleção final deve considerar:
- categoria de utilização;
- corrente térmica;
- corrente operacional;
- tensão da bobina;
- número de polos;
- contactos auxiliares;
- capacidade de interrupção;
- endurance;
- coordenação com proteção.

**Nota:** 32 A de corrente de teste não significa automaticamente que um contactor de 32 A seja adequado.

### 4.3 Alimentação de controlo

Usar fonte industrial 24 VDC para a cadeia de controlo.

A potência nominal será fechada depois do levantamento completo de:
- contactores;
- relés;
- ventiladores;
- PLC/MCU;
- interfaces;
- válvulas/atuadores, se existirem;
- margem de arranque.

## 5. Comunicação

### CAN-FD

**Candidato:** TI TCAN1044A-class ou equivalente.

CAN-FD será o barramento principal entre:
- TS-CORE;
- TS-MEASURE;
- TS-SAFE;
- TS-EV;
- TS-LOAD.

Usar isolamento galvânico nos limites onde a análise de domínio elétrico/EMC o exigir.

## 6. TS-EV — simulação do veículo

Funções:
- medição e geração de CP;
- geração de PWM;
- simulação de estados IEC 61851;
- PP;
- resistência/codificação de cabo;
- fault injection;
- deteção de comportamento incorreto do EVSE.

A rede PP deve usar componentes com tensão, tolerância, potência e comportamento térmico apropriados.

A injeção de falhas deve ser controlada pela cadeia de segurança e nunca depender apenas de software.

## 7. TS-LOAD — carga eletrónica

Arquitetura inicial:
- carga escalonada para testes funcionais;
- possibilidade de carga eletrónica controlada para PRO;
- monitorização térmica;
- ventilação forçada;
- corte independente por sobretemperatura.

A potência da carga deve ser definida para os perfis de teste reais. Não assumir que 22 kW contínuos serão dissipados internamente sem uma análise térmica dedicada.

## 8. Particionamento das PCB

### PCB 1 — TS-MEASURE

Responsabilidades:
- entradas de tensão;
- interfaces de corrente;
- AFE;
- ADC simultâneo;
- referência;
- MCU de medição;
- processamento;
- CAN isolado quando necessário.

Objetivo:
- módulo de medição calibrável e reutilizável.

### PCB 2 — TS-SAFE

Responsabilidades:
- E-stop;
- interlocks;
- watchdog;
- comando de contactores;
- feedback auxiliar;
- deteção de contacto soldado;
- trip térmico;
- estado seguro;
- CAN.

### PCB 3 — TS-EV

Responsabilidades:
- CP;
- PP;
- PWM;
- medição CP;
- fault injection;
- interface de diagnóstico.

### PCB 4 — TS-LOAD

Responsabilidades:
- comando da carga;
- sensores térmicos;
- ventiladores;
- proteção de temperatura;
- estados de carga;
- CAN.

### Razão para separar as placas

A separação permite:
- contenção de falhas;
- melhor EMC;
- manutenção simples;
- substituição de módulos;
- calibração independente;
- reutilização entre Mini, PRO e Factory;
- evolução da eletrónica sem redesenhar toda a máquina.

## 9. Proteções — estado atual

A arquitetura deve incluir, conforme cálculo final:
- seccionamento principal;
- proteção contra sobrecorrente;
- proteção de circuitos auxiliares;
- proteção contra surtos;
- PE dedicado;
- proteção/falha residual quando aplicável;
- E-stop;
- proteção térmica;
- proteção específica da carga.

Os valores nominais continuam em HOLD até fechar:
- sistema de alimentação;
- corrente de curto-circuito presumida;
- secção e comprimento dos condutores;
- método de instalação;
- temperatura ambiente;
- coordenação/selectividade;
- capacidade de interrupção;
- arquitetura de PE.

Não fixar disjuntores, fusíveis ou secções apenas pela corrente nominal de 32 A.

## 10. Calibração de fase

A calibração deverá usar uma fonte trifásica de referência/controlada.

Procedimentos:
1. aplicar tensão conhecida;
2. verificar ganho;
3. verificar offset;
4. verificar sequência de fases;
5. aplicar deslocamentos angulares conhecidos;
6. determinar erro de fase;
7. guardar coeficientes;
8. repetir em condições térmicas relevantes;
9. validar contra instrumento de referência independente.

O TestStation não deve ser a única referência usada para calibrar o próprio sistema.

## 11. Zonas de diagnóstico

### Zone A — Pre-EVSE

Medição do lado da alimentação/instalação, antes do EVSE.

Registar:
- tensão;
- corrente;
- frequência;
- potência;
- sequência de fases;
- ângulos entre fases;
- desequilíbrio;
- qualidade relevante da alimentação.

### Zone B — EVSE

Medição no caminho elétrico associado ao EVSE.

Registar os mesmos parâmetros.

### Comparação

O relatório deve mostrar:
- valor Zone A;
- valor Zone B;
- diferença;
- incerteza;
- conclusão técnica condicionada.

Exemplo de diagnóstico:
Zone A:
- L1-L2 = 120,1°
- L2-L3 = 119,8°
- L3-L1 = 120,1°

Se Zone B apresentar desvio significativo depois de considerada a incerteza de medição, o sistema pode sinalizar que a anomalia foi introduzida ou amplificada pelo EVSE.

Não utilizar um limite arbitrário universal de 1°. O limite deverá resultar da incerteza de medição, características do sistema e requisitos elétricos aplicáveis.

## 12. Modelo de relatório de fase

Campos mínimos:
- timestamp;
- equipamento;
- número de série;
- operador;
- ponto de medição;
- Zone A;
- Zone B;
- tensão RMS por fase;
- corrente RMS por fase;
- frequência;
- sequência;
- ângulos entre fases;
- erro/uncertainty;
- diferença A/B;
- estado PASS/ATTENTION/FAIL segundo regras configuráveis;
- recomendações;
- dados brutos disponíveis para auditoria.

## 13. Recomendação de compensação capacitiva

Quando a análise demonstrar um caso real de compensação reativa, o software poderá calcular uma **candidatura** de capacitância.

A recomendação não deve ser apresentada automaticamente como ordem de reparação.

Antes de qualquer aplicação devem ser verificados:
- tensão nominal;
- frequência;
- corrente;
- tensão de serviço do capacitor;
- descarga;
- comutação;
- tolerância;
- temperatura;
- harmónicos;
- risco de ressonância;
- duty cycle;
- proteção;
- requisitos da instalação;
- normas aplicáveis.

O TestStation deve distinguir claramente:
1. valor calculado;
2. valor comercial próximo;
3. recomendação de engenharia;
4. reparação aprovada.

## 14. Interface TestStation ↔ VAZAO EVSE

O carregador VAZAO deve prever, desde o projeto:
- acesso CP;
- PP;
- feedback dos contactores;
- estados do controlador;
- pontos de diagnóstico de baixa tensão;
- interface de serviço;
- sinais de estado relevantes;
- identificação do equipamento;
- possibilidade de diagnóstico sem comprometer as funções de segurança.

Qualquer sinal ligado a domínio perigoso deve possuir isolamento e proteção adequados.

Isto transforma o TestStation numa ferramenta de desenvolvimento do próprio carregador e reduz o custo de diagnóstico em campo.

## 15. Preliminary BOM

### TS-MEASURE
- ADC simultâneo 6 canais — 1
- MCU de medição STM32G4-class/equivalente — 1
- referência de precisão — 1
- sensores de tensão — 3 canais
- sensores de corrente — 3 canais
- proteção/filtragem analógica — conforme canais
- CAN-FD — 1
- memória não volátil para calibração — 1
- conectores/test points — conforme layout

### TS-SAFE
- MCU de segurança — 1
- watchdog externo — 1
- drivers de contactor — conforme canais
- contactores — conforme arquitetura de potência
- contactos auxiliares — conforme contactores
- E-stop — 1 ou mais conforme categoria/arquitetura
- interlocks — conforme máquina
- sensores térmicos — conforme zonas
- CAN — 1

### TS-EV
- interface CP — 1
- geração/medição PWM — 1
- rede PP — 1
- circuitos de fault injection — conforme estados suportados
- isolamento/proteção — conforme domínio

### TS-LOAD
- estágio de potência da carga — conforme perfil
- sensores térmicos — conforme dissipadores
- ventiladores — conforme cálculo térmico
- drivers — conforme estágio
- contactores/relés — conforme potência

### Sistema
- fonte 24 VDC industrial — 1
- seccionador principal — 1
- proteção de entrada — conforme cálculo
- SPD — conforme análise
- PE/barra de terra — 1
- distribuição 24 VDC — conforme carga
- cablagem e terminais — conforme corrente e instalação

## 16. Gates de aprovação

Antes de aquisição para protótipo energizado:
- esquema elétrico revisto;
- datasheets verificados;
- isolamento verificado;
- creepage/clearance verificados;
- proteção calculada;
- PE definido;
- térmica avaliada;
- PCB revista;
- firmware de segurança definido;
- medição validada em baixa tensão;
- calibração definida;
- ensaios de falha definidos.

Antes de ligação à rede:
- análise de risco;
- verificação de proteção;
- ensaio de continuidade PE;
- ensaio de isolamento;
- verificação da cadeia de E-stop;
- teste de contactores;
- teste de feedback;
- teste térmico;
- commissioning controlado.

## 17. Estado

**M1.5 — definido como baseline preliminar.**

Este documento não autoriza aquisição indiscriminada nem construção para ligação à rede sem os gates de engenharia acima.

## 18. Próximo marco

**TS-V1-M1.6 — Measurement PCB Schematic + TS-SAFE Schematic + Preliminary Harness/Connector Definition**

M1.6 deverá transformar esta seleção em esquemas elétricos e definição preliminar de cablagem/conectores, mantendo os domínios de segurança e medição separados.

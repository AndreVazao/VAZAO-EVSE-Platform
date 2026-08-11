# VAZAO EVSE Platform — Persistent Project Memory

> Este ficheiro é a memória persistente consolidada do projeto. Deve ser atualizado quando uma decisão técnica, requisito, arquitetura ou estado relevante for confirmado.

## 1. Identidade

- Projeto: **VAZAO EVSE Platform**
- Repositório: `AndreVazao/VAZAO-EVSE-Platform`
- Proprietário: AndreVazao
- Estado: Desenvolvimento ativo
- Fonte de verdade: este repositório GitHub

## 2. Objetivo

Criar um ecossistema profissional para desenvolver, testar, validar, diagnosticar e produzir carregadores de veículos elétricos VAZAO.

O ecossistema integra o desenvolvimento dos carregadores com uma plataforma de ensaio própria, permitindo fechar o ciclo:

**Desenvolvimento → Teste → Diagnóstico → Correção → Validação → Produção**

## 3. Linhas principais

### VAZAO EVSE Chargers

Linha de carregadores AC modulares, incluindo:

- carregador simples;
- carregador duplo;
- carregador quádruplo;
- wallbox;
- futuras multistations.

O desenvolvimento dos carregadores e da TestStation é considerado parte do mesmo ecossistema técnico.

### VAZAO EVSE TestStation

Plataforma profissional de ensaio destinada inicialmente aos carregadores VAZAO e posteriormente a EVSE de terceiros.

Gama:

- **Mini** — instalação e assistência técnica;
- **PRO** — desenvolvimento, investigação e validação;
- **Factory** — produção e testes automáticos em linha.

## 4. TestStation — primeira geração

Objetivo inicial:

- AC monofásico;
- AC trifásico;
- IEC 61851;
- até 32 A por fase;
- até 22 kW;
- simulação de veículo elétrico;
- simulação de estados de bateria/carga;
- diferentes consumos de corrente;
- testes automáticos e manuais;
- testes prolongados e stress;
- simulação controlada de falhas;
- medição de tensão, corrente, potência, energia e temperatura;
- validação CP, PP e PWM;
- histórico de ensaios;
- diagnóstico inteligente;
- relatórios PDF.

A futura expansão para DC/CCS deve ser considerada desde a arquitetura, mas não faz parte do primeiro MVP.

## 5. Arquitetura conceptual

```text
VAZAO EVSE PLATFORM
│
├── EVSE CHARGERS
│   ├── Hardware
│   ├── Firmware
│   ├── Software
│   ├── Mechanical
│   └── Manufacturing
│
└── TESTSTATION
    ├── TS-CORE
    ├── TS-SAFE
    ├── TS-EV
    ├── TS-MEASURE
    ├── TS-LOAD
    └── TS-COM
```

Fluxo principal da TestStation:

```text
HMI
 ↓
Test Engine
 ↓
Diagnostic Engine
 ↓
Hardware Abstraction Layer
 ↓
CAN-FD
 ↓
MCUs / Safety / Measurement / EV Simulation / Power
```

## 6. Princípio de segurança

O computador principal não deve ser responsável isoladamente pela segurança funcional.

A arquitetura deve possuir uma cadeia de segurança independente, incluindo, conforme o desenho final:

- MCU/controlador de segurança;
- contactores;
- relés de segurança;
- emergência;
- interlocks;
- watchdog;
- deteção de condições perigosas;
- colocação da potência em estado seguro em caso de falha do computador principal.

## 7. Test Engine

Os testes não devem ficar rigidamente codificados na interface.

Devem existir TestPacks e testes versionados, contendo pelo menos:

- ID;
- nome;
- versão;
- pré-condições;
- sequência;
- medições;
- limites;
- resultado;
- código de erro;
- informação diagnóstica.

Resultados possíveis previstos:

- PASS;
- PASS WITH WARNING;
- FAIL;
- ABORTED;
- SAFETY TRIP;
- NOT TESTED.

## 8. Diagnóstico inteligente

A TestStation não deve limitar-se a PASS/FAIL.

Para uma falha deve conseguir determinar, quando possível:

1. teste que falhou;
2. condição observada;
3. motivo técnico provável;
4. componentes/circuitos suspeitos;
5. probabilidade relativa das causas;
6. sequência recomendada de verificações;
7. sugestão de reparação;
8. evidência baseada nas medições registadas.

A arquitetura deverá permitir evolução futura para uma base de conhecimento alimentada pelos ensaios históricos.

## 9. Dados e rastreabilidade

Cada ensaio deverá poder ser associado a:

- EVSE ID;
- número de série;
- revisão de hardware;
- versão de firmware;
- TestStation ID;
- operador;
- data/hora;
- TestPack/version;
- resultados;
- medições;
- eventos;
- falhas;
- relatório.

A sessão deverá permitir reconstruir temporalmente o comportamento do EVSE durante o teste.

## 10. Instrumentação pretendida

Precisões de projeto inicialmente pretendidas:

- tensão: ±0,5 %;
- corrente: ±0,5 %;
- potência: ±1 %;
- energia: Classe 1.

Instrumentação prevista:

- sensores Hall ou equivalente;
- medição de tensão;
- ADC de precisão;
- sensores de temperatura;
- captura/análise de CP;
- captura/análise de PP;
- análise de PWM.

## 11. Estrutura física conceptual

Formato pretendido: caixa tipo trolley.

Dimensões aproximadas:

- altura: 72 cm;
- largura: 48 cm;
- profundidade: 30 cm.

Peso estimado: 25–35 kg.

Elementos previstos:

- rodas;
- pega telescópica;
- pegas laterais;
- ecrã tátil;
- LEDs de estado;
- buzzer;
- impressora opcional.

## 12. Roadmap base

1. Especificação técnica
2. Arquitetura
3. Hardware
4. Firmware
5. Software
6. Diagnóstico inteligente
7. Segurança
8. Mecânica
9. Calibração
10. Ensaios
11. Certificação
12. Produção

## 13. Milestone atual

**TS-V1-M0 — Technical Baseline**

Próximo documento oficial:

**TS-V1-M0-01 — Product Definition & System Requirements**

## 14. Regras de projeto

- Desenvolver uma plataforma comum e não três produtos independentes.
- Manter Mini, PRO e Factory como variantes da mesma plataforma.
- Projetar a TestStation em conjunto com os carregadores VAZAO.
- Preparar a arquitetura para futura expansão DC/CCS sem contaminar o MVP AC.
- Não colocar funções críticas de segurança exclusivamente no computador principal.
- Manter testes, protocolos e regras de diagnóstico versionáveis.
- Registar decisões técnicas importantes no GitHub.
- Evitar perder conhecimento nas conversas: decisões consolidadas devem entrar nesta memória e na documentação oficial.

## 15. Próximos passos

1. Consolidar a documentação existente dos carregadores VAZAO.
2. Criar `docs/01-requirements/TS-V1-M0-01-Product-Definition.md`.
3. Criar matriz Mini/PRO/Factory.
4. Definir requisitos funcionais e não funcionais.
5. Definir arquitetura elétrica e de segurança.
6. Definir interfaces entre hardware, firmware e software.
7. Definir primeiro TestPack IEC 61851.
8. Só depois iniciar seleção detalhada de componentes e PCB.

---

**Última consolidação:** 2026-08-11

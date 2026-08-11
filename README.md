# VAZAO EVSE Platform

Plataforma integrada para desenvolvimento, validação, diagnóstico e produção de equipamentos EVSE da VAZAO.

## Ecossistema

A plataforma integra duas linhas principais:

- **VAZAO EVSE Chargers** — desenvolvimento dos carregadores AC modulares VAZAO (single, dual, quad, wallbox e futuras multistations).
- **VAZAO EVSE TestStation** — plataforma profissional de ensaio, validação, diagnóstico, assistência e produção dos EVSE.

## TestStation

A gama prevista é:

- **TestStation Mini** — instalação e assistência técnica.
- **TestStation PRO** — desenvolvimento, investigação e validação.
- **TestStation Factory** — produção e testes automáticos em linha.

A primeira geração suporta EVSE AC monofásico e trifásico até 32 A por fase / 22 kW, com IEC 61851, simulação EV, CP/PP/PWM, medição, testes automáticos, testes de stress, diagnóstico e relatórios.

A arquitetura será modular e preparada para futura expansão para CCS/DC, ISO 15118, PLC e outros protocolos.

## Princípio de engenharia

A TestStation será desenvolvida em conjunto com os carregadores VAZAO. O ciclo de desenvolvimento será:

**Desenvolver → Testar → Diagnosticar → Corrigir → Validar → Produzir**

O GitHub é a fonte de verdade da documentação e das decisões técnicas do projeto. A conversa pode ser usada para análise e desenvolvimento, mas decisões e resultados consolidados devem ser registados no repositório.

## Estrutura documental

Consulte `docs/` para requisitos, arquitetura, hardware, firmware, software, testes, diagnóstico, segurança, calibração, certificação e produção.

Consulte `project-memory/` para a memória persistente do projeto, estado atual, decisões e próximos passos.

## Estado atual

**Fase:** TS-V1-M0 — Technical Baseline

**Próximo marco:** TS-V1-M0-01 — Product Definition & System Requirements

---

**Projeto:** VAZAO EVSE Platform  
**Proprietário:** AndreVazao  
**Estado:** Desenvolvimento ativo

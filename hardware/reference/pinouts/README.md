# VAZAO EVSE — Base de conhecimento de pinouts e blocos eletrónicos

**Idioma:** PT-PT  
**Estado:** catálogo vivo; primeira edição em 2026-10-16  
**Objetivo:** criar uma referência reutilizável para aprendizagem, revisão de esquemas, criação/validação de símbolos KiCad e deteção assistida de erros.

## Começar aqui

- [Catálogo inicial de pinouts e interfaces](PINOUT-CATALOG.md)
- [Biblioteca de símbolos verificados — TestStation M2.9](../../teststation/V1/CAD/symbols/README.md)
- [Registo de verificação dos componentes M2.9](../../teststation/V1/CAD/verification/M2.9-K-COMPONENT-PIN-VERIFICATION-REGISTER.md)

## Princípio essencial

**“Pinout universal” raramente significa pinout idêntico entre todos os componentes.** Esta base separa:

1. **Pinout de componente exato** — fabricante, código completo, pacote e revisão de datasheet identificados.
2. **Interface/padrão** — sinais típicos de I²C, SPI, UART, CAN, RS-485, USB, etc.; o conector físico e a ordem dos pinos podem variar.
3. **Regra de aprendizagem/diagnóstico** — heurísticas que sugerem erros, sem alterar automaticamente o circuito.
4. **Pinout por confirmar** — informação incompleta, que nunca deve ser tratada como aprovada.

Um nome de família (por exemplo, STM32, 7805, LM358 ou USB-C) **não chega** para escolher números de pinos, footprint ou ligação. Confirmar sempre o código completo, pacote, vista do desenho (top/bottom), marca de pino 1 e datasheet do fabricante.

## Regras de manutenção

Sempre que entra um componente novo:

1. Registar fabricante, código completo e variantes relevantes.
2. Guardar ligação oficial para datasheet e página do produto; registar revisão/data consultada.
3. Extrair a tabela de pinos e confrontá-la com o desenho de encapsulamento.
4. Registar pacote e footprint proposto, mas marcar como **não aprovado** até validar a numeração dos pads.
5. Classificar cada pino: alimentação, massa, entrada, saída, bidirecional, open-drain/open-collector, passivo, NC ou reservado.
6. Registar comportamento de pinos não usados, resistências pull-up/down, desacoplamento e componentes externos exigidos pelo datasheet.
7. Comparar o símbolo KiCad e o footprint com as fontes primárias.
8. Adicionar regras de deteção de erros conhecidas e exemplos de ERC/DRC.
9. Rever por uma segunda pessoa/agente; manter histórico Git e nunca sobrescrever silenciosamente uma versão confirmada.
10. Se houver contradição entre símbolo, footprint, BOM e datasheet, bloquear a migração até resolução.

## Campos mínimos recomendados para cada registo

- ID interno e estado: `draft`, `datasheet-checked`, `footprint-checked`, `reviewed`, `deprecated`.
- Fabricante, código completo, package code, quantidade de pinos e variante.
- Número do pino, nome/função oficial, tipo elétrico, restrições e tratamento quando não usado.
- Footprint KiCad e fonte que confirma a correspondência pad–pino.
- URL oficial, revisão do datasheet, data da verificação e responsável/revisor.
- Erros comuns, testes automáticos aplicáveis e histórico de alterações.

## Limites de segurança

Esta base é uma ferramenta de aprendizagem e revisão, não substitui datasheets, normas, revisão de engenharia, análise de isolamento, cálculos térmicos, EMC, creepage/clearance nem validação por profissional qualificado. **Não usar uma tabela genérica para energizar equipamento EVSE ou circuitos ligados à rede.**

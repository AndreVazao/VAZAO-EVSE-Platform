# Catálogo de pinouts e interfaces eletrónicas — edição inicial

Data da edição: 2026-10-16  
Estado geral: **referência de aprendizagem; validar sempre a variante e o pacote antes de usar num projeto.**

Este catálogo começa com padrões muito reutilizáveis e alguns componentes comuns. Será ampliado à medida que surgirem componentes na plataforma VAZÃO EVSE. Os pinouts específicos abaixo são limitados aos códigos/pacotes indicados.

## 1. Interfaces reutilizáveis

### 1.1 I²C — sinais do barramento

| Sinal | Função | Observações |
|---|---|---|
| SDA | Dados bidirecionais | Normalmente linha open-drain/open-collector com pull-up |
| SCL | Relógio | Normalmente linha open-drain/open-collector com pull-up |
| GND | Referência comum do domínio | A necessidade e arquitetura de referência dependem do sistema |
| VCC/VDD | Alimentação do dispositivo | Não é um sinal universal do barramento; confirmar tensão de cada dispositivo |

**Verificações automáticas úteis:** SDA/SCL sem pull-up quando exigido; pull-up para uma tensão incompatível com algum dispositivo; duas saídas push-pull ligadas ao mesmo barramento; endereços duplicados; ausência de referência de massa quando o desenho exige ligação galvânica.

A ordem dos pinos num conector I²C não é universal.

### 1.2 SPI — sinais do barramento

| Sinal comum | Outros nomes | Direção típica |
|---|---|---|
| SCLK | SCK | Controlador → periférico |
| MOSI | COPI, SDI, DIN | Controlador → periférico |
| MISO | CIPO, SDO, DOUT | Periférico → controlador |
| CS/SS | nCS, /CS | Normalmente controlador → periférico, ativo a nível baixo |
| GND/VDD | — | Alimentação conforme o dispositivo |

Os nomes variam entre fabricantes e alguns dispositivos invertem a nomenclatura de entrada/saída conforme o ponto de vista. Confirmar sempre a direção **vista pelo componente**. Cada periférico pode exigir modo SPI (CPOL/CPHA), frequência e temporização diferentes.

**Erro típico:** ligar duas saídas MISO/DOUT push-pull ao mesmo net sem tri-state/seleção apropriada; esquecer CS independente; confundir pinos DIN/DOUT de um ADC com MOSI/MISO do controlador.

### 1.3 UART / serial assíncrona

| Sinal | Ligação típica entre dois equipamentos |
|---|---|
| TX do equipamento A | RX do equipamento B |
| RX do equipamento A | TX do equipamento B |
| GND | Referência comum quando a interface não é isolada |

TX liga-se normalmente a RX, não a TX. UART TTL/CMOS **não é** RS-232 nem RS-485; níveis elétricos e proteção são diferentes. Verificar 1,8 V / 3,3 V / 5 V e não assumir tolerância de 5 V.

### 1.4 CAN / CAN FD

| Sinal | Função |
|---|---|
| TXD | Dados enviados pelo controlador para o transceiver |
| RXD | Dados recebidos pelo controlador a partir do transceiver |
| CANH | Linha diferencial alta do barramento |
| CANL | Linha diferencial baixa do barramento |
| VCC/GND | Alimentação do lado correspondente |

- Um controlador CAN (por exemplo, MCP2515) e um transceiver físico CAN são funções diferentes; um controlador SPI não liga diretamente ao par CANH/CANL sem transceiver.
- Em interfaces isoladas, confirmar as alimentações de ambos os lados e a estratégia de alimentação isolada.
- A terminação do barramento depende da topologia; não colocar automaticamente 120 Ω em cada nó.
- **ISO1044:** o fabricante classifica o produto como isolador/transceiver CAN com isolamento básico na página do produto; não inferir uma classe de segurança do sistema apenas pelo nome “isolado”. Confirmar requisitos e documentação aplicável.

Fontes: [TI ISO1044](https://www.ti.com/product/ISO1044), [Microchip MCP2515](https://www.microchip.com/en-us/product/MCP2515).

### 1.5 RS-485

| Sinal comum | Nomes alternativos |
|---|---|
| A / D− | Nomes não consistentes entre todos os fabricantes |
| B / D+ | Nomes não consistentes entre todos os fabricantes |
| DE | Driver enable |
| /RE ou RE | Receiver enable; polaridade depende do componente |
| DI | Entrada de dados do driver |
| RO | Saída de dados do recetor |

**A/B não é nomeação suficientemente segura para inferir polaridade entre fabricantes.** Confirmar tabela de verdade e definição A/B do transceiver específico. Verificar terminação, bias/failsafe, topologia, proteção ESD/surge e controlo de DE/RE.

### 1.6 USB

- USB 2.0 usa D+ e D− como par diferencial; verificar impedância, encaminhamento, proteção e orientação do conector.
- USB-C é um conector com várias funções e pinos; **não** ligar VBUS, CC1/CC2, SBU ou pares SuperSpeed com base numa pinagem simplificada.
- A pinagem do recetáculo USB-C tem contactos A e B e regras de orientação; consultar a especificação USB-IF e o desenho exato do conector escolhido.
- CC1/CC2, resistências de configuração, alimentação VBUS e negociação de potência dependem do papel (source/sink/DRP) e do perfil pretendido. USB-C não significa automaticamente USB Power Delivery.

Fonte: [USB-IF — especificações e documentação](https://www.usb.org/documents).

### 1.7 Alimentação e conectores genéricos

Não existe pinout universal para conectores JST, Molex, terminais de parafuso, headers de 2,54 mm ou conectores DC coaxiais. A família pode incluir orientações e polaridades diferentes. Registar o código do fabricante e a vista de referência.

Em cada bloco de alimentação, confirmar: entrada, saída, massa, polaridade, gama de tensão, corrente, dissipação, condensadores exigidos, proteção contra inversão e comportamento de arranque. Nunca inferir a pinagem de um regulador apenas pelo texto “7805” ou pelo aspeto do encapsulamento.

## 2. Componentes com pinout específico

### 2.1 LM358 — amplificador operacional duplo, SOIC-8 / PDIP-8 compatível com a pinagem clássica

| Pino | Função |
|---:|---|
| 1 | OUT A |
| 2 | IN− A |
| 3 | IN+ A |
| 4 | V− / GND em alimentação simples |
| 5 | IN+ B |
| 6 | IN− B |
| 7 | OUT B |
| 8 | V+ |

Fonte: [TI LM358 — página do fabricante e datasheet](https://www.ti.com/product/LM358).

**Atenção:** confirmar a variante exata (LM358, LM358B, LM358BA, fabricante alternativo), package e características elétricas. Pinout semelhante não garante desempenho, faixa de modo comum, offset ou estabilidade iguais. Não confundir entradas inversora e não inversora.

### 2.2 NE555 — temporizador, DIP-8 / SOIC-8 conforme variante

| Pino | Função |
|---:|---|
| 1 | GND |
| 2 | TRIG |
| 3 | OUT |
| 4 | RESET (ativo baixo) |
| 5 | CTRL / CONT |
| 6 | THRESH |
| 7 | DISCH |
| 8 | VCC |

Usar como referência inicial, não como substituto do datasheet do fabricante e variante escolhidos. Verificar limites de alimentação, corrente de saída, desacoplamento e uso do pino CTRL.

### 2.3 MCP2515 — controlador CAN, pacote PDIP/SOIC de 18 pinos

Este mapa é **apenas para PDIP/SOIC-18**. TSSOP-20 e QFN-20 têm numeração diferente.

| Pino | Função | Pino | Função |
|---:|---|---:|---|
| 1 | TXCAN | 18 | VDD |
| 2 | RXCAN | 17 | RESET |
| 3 | CLKOUT/SOF | 16 | CS |
| 4 | TX0RTS | 15 | SO (SPI MISO) |
| 5 | TX1RTS | 14 | SI (SPI MOSI) |
| 6 | TX2RTS | 13 | SCK |
| 7 | OSC2 | 12 | INT |
| 8 | OSC1 | 11 | RX0BF |
| 9 | VSS/GND | 10 | RX1BF |

Fonte: [Microchip MCP2515 — datasheet oficial](https://ww1.microchip.com/downloads/en/DeviceDoc/MCP2515-Family-Data-Sheet-DS20001801K.pdf).

**Erro comum:** tratar TXCAN/RXCAN como CANH/CANL. São sinais lógicos entre controlador CAN e transceiver. É necessário um transceiver físico compatível.

### 2.4 ISO1044 — transceiver CAN isolado, SOIC-8

| Pino | Função |
|---:|---|
| 1 | VCC1 |
| 2 | TXD |
| 3 | RXD |
| 4 | GND1 |
| 5 | CANL |
| 6 | CANH |
| 7 | GND2 |
| 8 | VCC2 |

Fonte: [TI ISO1044 — página do fabricante/datasheet](https://www.ti.com/product/ISO1044).

O mapa de pinos não confirma por si só o cumprimento dos requisitos de isolamento de um sistema EVSE. Verificar revisão do datasheet, sufixo exato, alimentação de cada lado, proteção, footprint, creepage/clearance e norma aplicável.

## 3. Componentes já usados no projeto TestStation M2.9

Estes componentes têm registos de verificação dedicados. A biblioteca separada é um **rascunho ainda não validado pelo KiCad CLI**; não usar como prova de ligação física aprovada.

### ADS131M06IPBSR — ADC de seis canais diferenciais, TQFP-32

| Pino | Função | Pino | Função |
|---:|---|---:|---|
| 1 | AIN2P | 17 | CS |
| 2 | AIN2N | 18 | DRDY |
| 3 | AIN3N | 19 | SCLK |
| 4 | AIN3P | 20 | DOUT |
| 5 | AIN4P | 21 | DIN |
| 6 | AIN4N | 22 | XTAL2 |
| 7 | AIN5N | 23 | XTAL1/CLKIN |
| 8 | AIN5P | 24 | CAP |
| 9–12 | NC | 25 | DGND |
| 13 | AGND | 26 | DVDD |
| 14 | REFIN | 27 | NC |
| 15 | AVDD | 28 | AGND |
| 16 | SYNC/RESET | 29 | AIN0P |
|  |  | 30 | AIN0N |
|  |  | 31 | AIN1N |
|  |  | 32 | AIN1P |

Fonte: [TI ADS131M06 datasheet](https://www.ti.com/lit/ds/symlink/ads131m06.pdf) e [página da variante IPBSR](https://www.ti.com/product/ADS131M06/part-details/ADS131M06IPBSR).

**Erro legado confirmado:** o símbolo cache anterior associava os pinos 1–6 a canais diferentes dos definidos no datasheet. Nunca inferir a ligação dos sensores a partir desse símbolo antigo.

### AMC1311BDWVR — amplificador isolado, SOIC-8

| Pino | Função |
|---:|---|
| 1 | VDD1 |
| 2 | IN |
| 3 | SHTDN |
| 4 | GND1 |
| 5 | GND2 |
| 6 | OUTN |
| 7 | OUTP |
| 8 | VDD2 |

Fonte: [TI AMC1311 datasheet](https://www.ti.com/lit/ds/symlink/amc1311.pdf) e [variante BDWVR](https://www.ti.com/product/AMC1311/part-details/AMC1311BDWVR).

**Erro legado confirmado:** o símbolo cache anterior tinha funções associadas a números de pino errados. Confirmar tratamento de SHTDN e a atribuição dos domínios de isolamento antes de migrar o esquema.

### TMCS1123 — sensor de corrente, pacote SOIC-10

| Pino | Função |
|---:|---|
| 1 | IN+ |
| 2 | IN− |
| 3 | GND |
| 4 | ALERT |
| 5 | VREF |
| 6 | VOUT |
| 7 | OC |
| 8 | VS |
| 9 | VOC |
| 10 | NC |

Fonte: [TI TMCS1123 datasheet](https://www.ti.com/lit/ds/symlink/tmcs1123.pdf) e [página do produto](https://www.ti.com/product/TMCS1123).

**Estado da variante:** o código exato `TMCS1123A3AQDVGR` ainda não foi confirmado por evidência de encomenda atual. O mapa funcional da família não prova que o sufixo completo do BOM está correto. Confirmar também o tratamento de ALERT, VREF, OC, VOC e NC no circuito.

## 4. Regras iniciais para deteção automática de erros

Estas regras podem orientar um analisador de esquemas/netlists. Devem produzir **alertas explicados**, nunca correções automáticas sem aprovação.

| ID | Regra | Severidade sugerida | Falsos positivos / ressalvas |
|---|---|---|---|
| PIN-001 | Número de pino do símbolo não coincide com datasheet da variante/pacote | Bloqueante | Exige código e package exatos |
| PIN-002 | Símbolo omite pinos físicos sem justificativa | Alta | Alguns pinos NC podem ser intencionalmente ocultados, mas devem estar documentados |
| ELEC-001 | Saída push-pull ligada diretamente a outra saída | Alta | Pode haver interfaces especiais; exigir prova |
| ELEC-002 | Pino de alimentação sem fonte identificada | Alta | ERC pode não reconhecer fontes externas ou power flags |
| ELEC-003 | Entrada de alta impedância flutuante | Média/alta | Pode ser intencional ou configurada por software, mas requer justificativa |
| ELEC-004 | Open-drain sem pull-up ou equivalente | Alta | Pull-up pode estar noutro módulo; verificar a netlist completa |
| BUS-001 | UART TX ligado a TX sem conversão explícita | Média/alta | Confirmar a perspetiva de nomes e a arquitetura |
| BUS-002 | MCP2515 sem transceiver CAN na interface física | Alta | O transceiver pode estar noutro bloco/placa |
| BUS-003 | CAN com terminação duplicada ou ausente | Média/alta | Depende da topologia e do local físico das terminações |
| PWR-001 | Alimentação fora da gama do componente | Bloqueante | Exige análise elétrica e tolerâncias |
| ISO-001 | Sinais atravessam barreira de isolamento sem componente/caminho aprovado | Bloqueante | Exige análise do sistema, não só ERC |
| PCB-001 | Footprint pad-number não corresponde ao número de pino do símbolo | Bloqueante | Validar com desenho de encapsulamento do fabricante |
| BOM-001 | Código de componente incompleto ou não confirmado | Alta | Distinguir “não confirmado” de “inválido” |

## 5. Próximas expansões recomendadas

Prioridade para a plataforma VAZÃO EVSE:

1. Diodos comuns e TVS: polaridade, cátodo/ânodo, VRWM e potência.
2. MOSFETs N/P: G/D/S, body diode, pacote e pinagem que varia por fabricante.
3. Reguladores lineares e DC/DC comuns: entrada, GND, saída, enable, feedback e componentes externos.
4. Optoacopladores e isoladores digitais: pinos, direção, isolamento, CMTI e alimentação.
5. Transceivers RS-485/CAN: DI/RO/DE/RE, A/B, CANH/CANL e proteção.
6. Conectores comuns (JST-XH/PH, Micro-Fit, terminais, USB-C): número de parte, vista, orientação e pin 1.
7. MCU usados no projeto: tabela completa por referência exata e package, incluindo alimentação, reset, boot, SWD/JTAG e pinos multiplexados.
8. Relés e contactores: bobina, contactos COM/NO/NC, tensão/corrente e supressão.
9. Medição EVSE: amplificadores isolados, ADCs, sensores de corrente/tensão, referências e fontes isoladas.
10. Regras de revisão ERC/DRC com casos de teste e resultados esperados.

## Histórico

- 2026-10-16 — primeira edição; padrões I²C/SPI/UART/CAN/RS-485/USB e pinouts iniciais LM358, NE555, MCP2515, ISO1044 e componentes da TestStation M2.9.

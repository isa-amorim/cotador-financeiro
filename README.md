# 📈 Financial Monitoring & Currency Alert System
Aplicação CLI modular em Python projetada para o monitoramento de câmbio em tempo real via AwesomeAPI. O sistema implementa validação rigorosa de contratos de dados, cálculo financeiro exato, alertas de oportunidade de compra e interface de terminal rica em componentes visuais.

## 📌 Problema de Negócio & Solução
Acompanhar cotações de moedas de forma manual ou por scripts simples expõe aplicações a **erros de arredondamento financeiro (float)** e **falhas de rede não tratadas**.

Esta aplicação resolve esses gargalos operacionais atuando como uma **Camada de Integração e Monitoramento Financeiro:**

1. **Consumo Resiliente:** Trata timeouts, erros HTTP (4xx/5xx) e falhas de conexão sem quebrar a execução do sistema.
2. **Garantia de Precisão Financeira:** Converte todas as entradas numéricas para decimal.Decimal, prevenindo dízimas ocultas do padrão IEEE 754.
3. **Validação de Contrato:** Sanitiza e valida o *payload* JSON da API externa via modelos imutáveis do Pydantic.
4. **Motor de Alertas e Apresentação:** Compara cotações em tempo real contra metas configuráveis e renderiza os resultados em tabelas/painéis responsivos na CLI.

## 🏗️ Arquitetura e Estrutura do Repositório
O projeto adota uma **arquitetura orientada a serviços**, separando estritamente responsabilidades de I/O, regras de negócio e apresentação **(Clean Code e SOLID).**

```
cotador-financeiro/
│
├── cotador/                        # Pacote Principal (Lógica da Aplicação)
│   ├── __init__.py                 # Ponto de exportação de símbolos
│   ├── client.py                   # Cliente HTTP desacoplado com httpx
│   ├── exceptions.py               # Hierarquia de exceções de domínio (CotadorError)
│   ├── models.py                   # Schemas Pydantic e conversão de tipos (CurrencyQuote)
│   ├── services.py                 # Regras de negócio, cálculos e alertas (CurrencyService)
│   └── views.py                    # Apresentação visual CLI com Rich (TerminalView)
│
├── tests/                          # Suíte de Testes Unitários Automatizados
│   ├── test_client.py              # Simulação de chamadas HTTP com MockTransport
│   └── test_services.py            # Testes de regras de negócio e parsing com Mocks
│
├── .gitignore                      # Exclusão de venv, caches e arquivos de configuração
├── config.py                       # Configurações globais e valores padrão do sistema
├── LICENSE                         # Licença open-source MIT
├── main.py                         # Orquestrador CLI e ponto de entrada principal
├── README.md                       # Documentação técnica do repositório
└── requirements.txt                # Mapeamento de dependências externas
```

## 🛠️ Destaques de Engenharia de Software
- **Precisão Matemática Rigorosa:** Uso exclusivo de decimal.Decimal para operações e representações monetárias, assegurando exatidão absoluta nos valores de compra (bid) e venda (ask).

- **Inversão de Dependências (DIP):** O serviço CurrencyService aceita injeção de dependência do cliente HTTP, viabilizando o isolamento total dos testes sem dependência de conexões ativas de rede.

- **Mapeamento de Exceções de Domínio:** Falhas de infraestrutura e biblioteca externa (httpx) são capturadas e traduzidas em exceções de domínio próprias (APIConnectionError, HTTPStatusError).

- **Testabilidade com Mocks:** Suíte de testes unitários automatizados cobrindo parsing de dados, conversões de timestamp e regras de disparo de alertas com cobertura isolada via pytest e unittest.mock.

## 🚀 Como Executar a Aplicação
### Pré-requisitos
- Python **3.11** ou superior instalado.

#### 1. Clonar o Repositório
```
git clone https://github.com/isa-amorim/cotador-financeiro.git
cd cotador-financeiro
```

#### 2. Instalar Dependências
```
python -m pip install -r requirements.txt
```

#### 3. Executar Consulta Padrão (USD, EUR, BTC)
```
python main.py
```

#### 4. Executar Monitoramento com Alerta de Preço-Alvo
```
python main.py --pairs USD-BRL EUR-BRL --target-pair USDBRL --target-price 5.20
```

## 🧪 Executando os Testes Automáticos
Para rodar a suíte de testes unitários e validar o comportamento do sistema e dos Mocks:
```
python -m pytest -v
```

## 📑 Licença

Este projeto está sob a licença **MIT**. Para mais detalhes, acesse o arquivo [LICENSE](https://github.com/isa-amorim/cotador-financeiro/blob/main/LICENSE).

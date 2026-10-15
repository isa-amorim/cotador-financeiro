"""
Módulo de Configurações Globais da Aplicação.
Centraliza parâmetros operacionais, timeouts e listas padrão de monitoramento.
"""

from typing import List

# Timeout padrão para requisições HTTP (em segundos)
DEFAULT_HTTP_TIMEOUT: float = 10.0

# Pares de moedas monitorados por padrão
DEFAULT_CURRENCY_PAIRS: List[str] = ["USD-BRL", "EUR-BRL", "BTC-BRL"]

# Mapeamento de pares para chaves internas da API
PAIR_KEY_MAP: dict[str, str] = {
    "USD-BRL": "USDBRL",
    "EUR-BRL": "EURBRL",
    "BTC-BRL": "BTCBRL",
}
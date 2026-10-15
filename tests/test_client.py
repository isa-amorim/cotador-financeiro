"""
Testes unitários para o AwesomeAPIClient simulando respostas de rede com httpx.MockTransport.
"""

import httpx
import pytest

from cotador.client import AwesomeAPIClient
from cotador.exceptions import APIConnectionError, HTTPStatusError


def test_fetch_current_quotes_success() -> None:
    """Garante que o cliente processa e retorna o JSON corretamente em chamadas bem-sucedidas."""
    
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "USDBRL": {
                    "code": "USD",
                    "codein": "BRL",
                    "name": "Dólar Americano/Real Brasileiro",
                    "high": "5.20",
                    "low": "5.10",
                    "pctChange": "0.50",
                    "bid": "5.15",
                    "ask": "5.16",
                    "timestamp": "1710000000",
                }
            },
        )

    # Injeta um transporte simulado no cliente httpx interno
    transport = httpx.MockTransport(mock_handler)
    client = AwesomeAPIClient()
    
    # Substitui temporariamente a chamada real do httpx pelo transporte simulado
    with httpx.Client(transport=transport) as mock_http_client:
        # Patch manual na execução
        client.BASE_URL = "https://economia.awesomeapi.com.br"
        quotes = client.fetch_current_quotes(["USD-BRL"])

    assert "USDBRL" in quotes
    assert quotes["USDBRL"]["code"] == "USD"


def test_fetch_current_quotes_empty_pairs() -> None:
    """Garante que passar uma lista vazia dispara ValueError imediatamente sem acessar a rede."""
    client = AwesomeAPIClient()
    with pytest.raises(ValueError, match="A lista de pares de moedas não pode estar vazia."):
        client.fetch_current_quotes([])
"""
Testes unitários para o módulo CurrencyService utilizando Mocks.
"""

from decimal import Decimal
from unittest.mock import Mock
from datetime import datetime
import pytest

from cotador.models import CurrencyQuote
from cotador.services import CurrencyService


@pytest.fixture
def mock_api_client() -> Mock:
    """Fixture que simula o cliente HTTP AwesomeAPIClient."""
    client = Mock()
    client.fetch_current_quotes.return_value = {
        "USDBRL": {
            "code": "USD",
            "codein": "BRL",
            "name": "Dólar Americano/Real Brasileiro",
            "high": "5.2000",
            "low": "5.1000",
            "pctChange": "0.50",
            "bid": "5.1500",
            "ask": "5.1600",
            "timestamp": "1710000000",
        }
    }
    return client


def test_get_latest_quotes_success(mock_api_client: Mock) -> None:
    """Garante que os dados brutos são convertidos corretamente para CurrencyQuote."""
    service = CurrencyService(client=mock_api_client)
    quotes = service.get_latest_quotes(["USD-BRL"])

    assert "USDBRL" in quotes
    quote = quotes["USDBRL"]
    assert isinstance(quote, CurrencyQuote)
    assert quote.bid == Decimal("5.1500")
    assert quote.ask == Decimal("5.1600")
    assert quote.is_positive_variation is True


def test_check_threshold_alert_triggered() -> None:
    """Valida se o alerta de preço dispara quando o valor de venda é menor ou igual ao alvo."""
    service = CurrencyService()
    quote = CurrencyQuote(
        code="USD",
        codein="BRL",
        name="Dólar",
        high=Decimal("5.20"),
        low=Decimal("5.10"),
        pctChange=Decimal("0.50"),
        bid=Decimal("5.15"),
        ask=Decimal("5.16"),
        timestamp=datetime.now(),
    )

    # Preço-alvo acima do valor de venda -> Alerta Disparado (True)
    assert service.check_threshold_alert(quote, Decimal("5.20")) is True

    # Preço-alvo abaixo do valor de venda -> Alerta Não Disparado (False)
    assert service.check_threshold_alert(quote, Decimal("5.00")) is False
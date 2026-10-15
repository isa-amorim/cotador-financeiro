"""
Módulo de Serviços de Cotação Financeira.
Contém as regras de negócio para processamento de cotações, cálculos e alertas.
"""

from decimal import Decimal
from typing import Dict, List

from cotador.client import AwesomeAPIClient
from cotador.models import CurrencyQuote


class CurrencyService:
    """Serviço responsável por processar e aplicar regras de negócio sobre as cotações."""

    def __init__(self, client: AwesomeAPIClient | None = None) -> None:
        """Permite injeção de dependência do cliente HTTP para facilitarmos testes unitários."""
        self.client = client or AwesomeAPIClient()

    def get_latest_quotes(self, pairs: List[str]) -> Dict[str, CurrencyQuote]:
        """
        Busca e converte o JSON bruto da API em um dicionário de objetos CurrencyQuote validados.
        
        :param pairs: Lista de pares desejados (ex: ['USD-BRL', 'EUR-BRL']).
        :return: Dicionário mapeando a chave do par (ex: 'USDBRL') para seu respectivo objeto CurrencyQuote.
        """
        raw_data = self.client.fetch_current_quotes(pairs)
        quotes: Dict[str, CurrencyQuote] = {}

        for key, payload in raw_data.items():
            # Converte cada item do dicionário bruto no modelo Pydantic fortemente tipado
            quotes[key] = CurrencyQuote(**payload)

        return quotes

    def check_threshold_alert(
        self, quote: CurrencyQuote, target_price: Decimal
    ) -> bool:
        """
        Verifica se o valor de venda da moeda atingiu ou ficou abaixo do preço-alvo.
        
        :param quote: Objeto CurrencyQuote com os dados atuais da moeda.
        :param target_price: Valor teto (alvo) definido pelo usuário para compra.
        :return: True se a cotação atual for menor ou igual ao preço-alvo.
        """
        return quote.ask <= target_price
"""
Módulo de Cliente HTTP para comunicação com a AwesomeAPI.
Responsável por realizar chamadas resilientes e traduzir exceções para o domínio da aplicação.
"""

from typing import Any, Dict, List
import httpx

from cotador.exceptions import APIConnectionError, HTTPStatusError


class AwesomeAPIClient:
    """Cliente HTTP desacoplado para consumo dos endpoints de economia da AwesomeAPI."""

    BASE_URL = "https://economia.awesomeapi.com.br"

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout

    def fetch_current_quotes(self, pairs: List[str]) -> Dict[str, Any]:
        """
        Busca as cotações em tempo real para os pares de moedas informados.
        """
        if not pairs:
            raise ValueError("A lista de pares de moedas não pode estar vazia.")

        pairs_query = ",".join(pairs)
        url = f"{self.BASE_URL}/last/{pairs_query}"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException as exc:
            raise APIConnectionError(
                f"Tempo limite excedido ({self.timeout}s) ao conectar à AwesomeAPI.",
                original_exception=exc,
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise HTTPStatusError(
                status_code=exc.response.status_code,
                detail=exc.response.text,
            ) from exc

        except httpx.RequestError as exc:
            raise APIConnectionError(
                f"Falha de conexão de rede ao acessar a AwesomeAPI: {str(exc)}",
                original_exception=exc,
            ) from exc

    def fetch_daily_history(self, pair: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Busca o histórico diário de cotações de um par específico para análise de tendência.
        """
        url = f"{self.BASE_URL}/json/daily/{pair}/{days}"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException as exc:
            raise APIConnectionError(
                f"Timeout ao buscar histórico de {pair}.", original_exception=exc
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise HTTPStatusError(
                status_code=exc.response.status_code, detail=exc.response.text
            ) from exc

        except httpx.RequestError as exc:
            raise APIConnectionError(
                f"Erro de rede ao buscar histórico de {pair}.", original_exception=exc
            ) from exc
"""
Módulo de Exceções Customizadas do Cotador Financeiro.
Define a hierarquia de erros para isolar falhas de infraestrutura de regras de domínio.
"""


class CotadorError(Exception):
    """Exceção base para todas as falhas mapeadas no Cotador Financeiro."""

    pass


class APIConnectionError(CotadorError):
    """Disparada quando ocorrem falhas de rede, timeouts ou indisponibilidade da API."""

    def __init__(self, message: str, original_exception: Exception | None = None) -> None:
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)


class HTTPStatusError(CotadorError):
    """Disparada quando a API responde com um status code de erro (4xx ou 5xx)."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Erro HTTP {self.status_code}: {self.detail}")


class InvalidCurrencyError(CotadorError):
    """Disparada quando o par de moedas solicitado não existe ou é inválido."""

    def __init__(self, pair: str) -> None:
        self.pair = pair
        super().__init__(f"O par de moedas '{self.pair}' é inválido ou não foi encontrado.")
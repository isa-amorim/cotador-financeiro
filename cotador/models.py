from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Union
from pydantic import BaseModel, Field, field_validator


class CurrencyQuote(BaseModel):
    """Modelo imutável para parsing e validação das cotações recebidas da API."""

    code: str
    codein: str
    name: str
    high: Decimal
    low: Decimal
    pct_change: Decimal = Field(..., alias="pctChange")
    bid: Decimal
    ask: Decimal
    timestamp: datetime

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, value: Union[str, int, datetime]) -> datetime:
        """Converte o timestamp UNIX recebido como string/int para datetime, preservando objetos datetime já instanciados."""
        if isinstance(value, datetime):
            return value
        return datetime.fromtimestamp(int(value))

    @property
    def is_positive_variation(self) -> bool:
        """Retorna True se a variação diária for maior ou igual a zero."""
        return self.pct_change >= Decimal("0.00")
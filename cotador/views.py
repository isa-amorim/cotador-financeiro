"""
Módulo de Apresentação (View) do Cotador Financeiro.
Responsável pela renderização de tabelas e painéis no terminal utilizando Rich.
"""

from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cotador.models import CurrencyQuote


class TerminalView:
    """Camada de interface no terminal responsável por exibir cotações e alertas."""

    def __init__(self) -> None:
        self.console = Console()

    def render_quote_table(self, quotes: Dict[str, CurrencyQuote]) -> None:
        """
        Constrói e exibe uma tabela estilizada com as cotações fornecidas.
        
        :param quotes: Dicionário contendo os modelos CurrencyQuote processados.
        """
        table = Table(
            title="[bold blue] Cotações do Câmbio Financeiro[/bold blue]",
            caption="Dados atualizados via AwesomeAPI",
            header_style="bold magenta",
        )

        table.add_column("Moeda", justify="left", style="cyan", no_wrap=True)
        table.add_column("Par", justify="center", style="white")
        table.add_column("Compra (Bid)", justify="right", style="green")
        table.add_column("Venda (Ask)", justify="right", style="bold green")
        table.add_column("Máxima", justify="right", style="dim white")
        table.add_column("Mínima", justify="right", style="dim white")
        table.add_column("Variação (%)", justify="right")

        for key, quote in quotes.items():
            # Define cor condicional com base na variação percentual
            var_color = "bold green" if quote.is_positive_variation else "bold red"
            var_icon = "▲" if quote.is_positive_variation else "▼"
            var_formatted = f"[{var_color}]{var_icon} {quote.pct_change}%[/{var_color}]"

            table.add_row(
                quote.name,
                f"{quote.code}/{quote.codein}",
                f"R$ {quote.bid:.4f}",
                f"R$ {quote.ask:.4f}",
                f"R$ {quote.high:.4f}",
                f"R$ {quote.low:.4f}",
                var_formatted,
            )

        self.console.print(table)

    def render_alert(self, quote: CurrencyQuote, target_price: str) -> None:
        """Exibe um painel destacado quando um alerta de preço é disparado."""
        panel = Panel(
            f"[bold yellow]OPORTUNIDADE DE COMPRA DETECTADA![/bold yellow]\n\n"
            f"A moeda [bold cyan]{quote.name}[/bold cyan] atingiu o preço de venda "
            f"[bold green]R$ {quote.ask:.4f}[/bold green] (Meta configurada: R$ {target_price}).",
            title=" Alerta de Cotação",
            border_style="green",
        )
        self.console.print(panel)
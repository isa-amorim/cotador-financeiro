"""
Ponto de entrada do Cotador Financeiro.
Orquestra os módulos de infraestrutura, serviço e apresentação via CLI.
"""

import argparse
from decimal import Decimal, InvalidOperation
import sys

from cotador.client import AwesomeAPIClient
from cotador.exceptions import CotadorError
from cotador.services import CurrencyService
from cotador.views import TerminalView


def parse_arguments() -> argparse.Namespace:
    """Configura e analisa os argumentos fornecidos pela linha de comando."""
    parser = argparse.ArgumentParser(
        description="Sistema de Monitoramento Financeiro e Alertas de Câmbio."
    )
    
    parser.add_argument(
        "--pairs",
        nargs="+",
        default=["USD-BRL", "EUR-BRL", "BTC-BRL"],
        help="Lista de pares de moedas para cotação (ex: USD-BRL EUR-BRL).",
    )
    
    parser.add_argument(
        "--target-pair",
        type=str,
        help="Par de moeda específico para monitorar alerta (ex: USDBRL).",
    )
    
    parser.add_argument(
        "--target-price",
        type=str,
        help="Preço-alvo para disparo de alerta de compra (ex: 5.10).",
    )

    return parser.parse_args()


def main() -> None:
    """Executa a orquestração principal do sistema de cotação."""
    args = parse_arguments()
    view = TerminalView()

    try:
        # Inicialização dos componentes com injeção de dependência
        client = AwesomeAPIClient(timeout=10.0)
        service = CurrencyService(client=client)

        # 1. Consulta e renderização das cotações principais
        quotes = service.get_latest_quotes(pairs=args.pairs)
        view.render_quote_table(quotes)

        # 2. Avaliação de alerta de preço (se parâmetros forem fornecidos)
        if args.target_pair and args.target_price:
            if args.target_pair not in quotes:
                view.console.print(
                    f"[bold red]Erro:[/bold red] O par '{args.target_pair}' não está entre os pares consultados."
                )
                sys.exit(1)

            target_decimal = Decimal(args.target_price)
            selected_quote = quotes[args.target_pair]

            if service.check_threshold_alert(selected_quote, target_decimal):
                view.render_alert(selected_quote, args.target_price)

    except CotadorError as err:
        view.console.print(f"[bold red]Erro de Aplicação:[/bold red] {err}")
        sys.exit(1)
    except InvalidOperation:
        view.console.print("[bold red]Erro de Validação:[/bold red] O preço-alvo fornecido é um valor numérico inválido.")
        sys.exit(1)
    except Exception as err:
        view.console.print(f"[bold red]Erro Inesperado:[/bold red] {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
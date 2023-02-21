
import io

from textwrap import wrap
from rich.console import Console
from rich.table import Table
from rich.text import Text

from lib.builder import encode_lexical_semantics


def print_table(df, ptc=0.7, date_width=15, short_width=50, link_width=35):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim", width=date_width)
    table.add_column("Short Description")
    table.add_column("Link to powerpoint", style="dim")
    table.add_column("Expected project length", justify="right")

    for _, row in df.iterrows():
        short_desc_wrapped = encode_lexical_semantics(row['Short Description'], ptc, short_width)
        link_wrapped = wrap(row['Link to powerpoint'], link_width)
        num_lines = max(len(short_desc_wrapped), len(link_wrapped), 1)

        for i in range(num_lines):
            if i == 0:
                table.add_row(
                    Text.from_markup(
                        f"[bold]{row['Date'].strftime('%d - %b - %Y')}[/bold]"),
                    short_desc_wrapped[i],
                    Text.from_markup(f"[dim]{link_wrapped[i]}[/dim]"),
                    Text.from_markup(
                        f"[bold]{row['Expected project length']}[/bold]"),
                )
            else:
                table.add_row(
                    "",
                    short_desc_wrapped[i] if i < len(
                        short_desc_wrapped) else "",
                    Text.from_markup(link_wrapped[i]) if i < len(
                        link_wrapped) else "",
                    "",
                )

    console = Console()
    console.print(table)


def table_to_str(table):
    table_str = io.StringIO()
    table_str.write(str(table))
    return table_str.getvalue()

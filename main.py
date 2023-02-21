
import os 

from lib.args import get_args
from lib.setup import init_nltk
from lib.loader import print_table
from lib.builder import format_table, populate_dataframe


if __name__ == "__main__":
    # Get the arguments
    args = get_args()

    # Example usage
    df = populate_dataframe(args.input)

    init_nltk(args.output)

    # Print the table
    print_table(
        df=df, ptc=args.top_k_pct, date_width=args.date_width, 
        short_width=args.desc_width, link_width=args.link_width
    )

    # Get the formatted table as a string
    table_str = format_table(
        df=df, date_width=args.date_width, short_width=args.desc_width,
        link_width=args.link_width, length_width=args.length_width)

    # Save the table string to a file
    with open(os.path.join(args.output, 'notes.log'), 'w') as f:
        f.write(table_str)

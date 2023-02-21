
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='data/notes', help='Path to the directory containing the notes')
    parser.add_argument('--output', type=str, default='data', help='Path to the directory to save the output')
    parser.add_argument('--top-k-pct', type=float, default=0.7, help='Percentage of total number of words to use as top-K keywords')
    parser.add_argument('--desc-width', type=int, default=50, help='Width of the description column in the output table')
    parser.add_argument('--date-width', type=int, default=15, help='Width of the date column in the output table')
    parser.add_argument('--link-width', type=int, default=35, help='Width of the link column in the output table')
    parser.add_argument('--length-width', type=int, default=25, help='Width of the length column in the output table')
    args = parser.parse_args()
    return args

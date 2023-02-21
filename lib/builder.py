
import os
import json
import nltk
import string
import textwrap
import pandas as pd

from rich.text import Text
from keybert import KeyBERT


def populate_dataframe(directory):
    df = pd.DataFrame(columns=["Date", "Short Description", "Link to powerpoint", "Expected project length"])

    for file in os.listdir(directory):
        if file.endswith(".json"):
            with open(os.path.join(directory, file), "r") as f:
                data = json.load(f)

                date_str = data.get("Date")
                if date_str:
                    date = pd.to_datetime(date_str, format="%d-%b-%Y").date()
                else:
                    date = pd.NaT

                short_desc = data.get("Short Description")
                link = data.get("Link to powerpoint")
                length = data.get("Expected project length")

                df = df.append({
                    "Date": date,
                    "Short Description": short_desc,
                    "Link to powerpoint": link,
                    "Expected project length": length
                }, ignore_index=True)

    return df

# TODO: Fix the issue with whitespace before ')' and ']' and '}' and '>' and ending '`'.
# TODO: Fix the issue with whitespace removal between some words.
# Define a function to encode lexical semantics and encolor the output
def encode_lexical_semantics(text, top_k_pct=0.1, width=50):
    # Initialize KeyBERT extractor
    kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')

    # Get total number of words in text
    num_words = count_words(text)

    # Calculate top_k based on percentage of total number of words
    top_k = max(int(num_words * top_k_pct), 1)

    # Extract top-K keywords using KeyBERT
    keywords = kw_extractor.extract_keywords(text, top_n=top_k,
                                             keyphrase_ngram_range=(1, 1),
                                             stop_words='english')

    # Categorize words based on whether they are in the top-K keywords
    important_words = set([word for word, score in keywords])
    not_important_words = set(nltk.word_tokenize(text)) - important_words

    # Tokenize text into words
    words = nltk.word_tokenize(text)

    # Wrap the text into lines of maximum width 50
    wrapped_text = textwrap.wrap(text, width=width)

    # Create Text object with color annotations
    encolored_text = []
    text_obj = Text()
    en_punkt = False
    for line in wrapped_text:
        line_words = nltk.word_tokenize(line)
        line_word_index = 0
        for word in line_words:
            # Check if the current word is in the set of important words
            if word in important_words:
                text_obj.append(word, style="bold green")
            else:
                text_obj.append(word)

            # Determine the length of the current word, and update the line_word_index
            word_len = len(word)
            line_word_index += word_len

            # Check if the next word (if any) should be appended with a space
            if line_word_index < width and len(line_words) > 1 and line_words.index(word) < len(line_words) - 1:
                next_word = line_words[line_words.index(word) + 1]
                curr_word = line_words[line_words.index(word)]
                if curr_word[0] in ")" or curr_word[0] in "]" or curr_word[0] in "}" or curr_word[0] in ">" or curr_word[0] in "`":
                    if next_word[0] not in string.whitespace and next_word[0] not in string.punctuation:
                        text_obj.append(" ")
                else:
                    if next_word[0] not in string.whitespace and next_word[0] not in string.punctuation and not en_punkt:
                        text_obj.append(" ")
                    else:
                        if en_punkt:
                            en_punkt = False
                        else:
                            if next_word[0] in "(" or next_word[0] in "[" or next_word[0] in "{" or next_word[0] in "<" or next_word[0] in '`':
                                text_obj.append(" ")
                                en_punkt = True

            # Check if the line has exceeded the maximum width
            if line_word_index >= width:
                encolored_text.append(text_obj)
                text_obj = Text()
                line_word_index = word_len

            # Check if the current word ends with a punctuation mark
            if word_len > 1 and word[-1] in string.punctuation:
                # Append a space after the punctuation mark
                text_obj.append(" ")

        # Append the line Text object to the list
        encolored_text.append(text_obj)
        text_obj = Text()

    # Remove empty Text objects from the list
    encolored_text = [obj for obj in encolored_text if len(obj) > 0]

    return encolored_text


def count_words(text):
    # Tokenize text into words using nltk
    words = nltk.word_tokenize(text)

    # Return number of words
    return len(words)


# Define the function to format and return the dataframe as a table string
def format_table(df, date_width=15, short_width=50, link_width=35, length_width=25):
    # Define the maximum width of each column
    col_widths = {
        'Date': date_width,
        'Short Description': short_width,
        'Link to powerpoint': link_width,
        'Expected project length': length_width
    }

    # Create a list to store the formatted table rows
    rows = []

    # Add the header row to the list
    header = '|'
    for col, width in col_widths.items():
        header += f' {col.upper():^{width}} |'
    rows.append(header)
    rows.append('-' * len(header))

    # Add each row of the dataframe to the list
    for _, row in df.iterrows():
        # Wrap the text in the Short Description and Link to powerpoint columns to multiple lines if needed
        short_desc_wrapped = textwrap.wrap(row['Short Description'], col_widths['Short Description'])
        link_wrapped = textwrap.wrap(row['Link to powerpoint'], col_widths['Link to powerpoint'])

        # Calculate the number of lines needed for this row
        num_lines = max(len(short_desc_wrapped), len(link_wrapped), 1)

        # Add each line of the row to the list
        for i in range(num_lines):
            if i == 0:
                # Add the first line of the row with the original date and project length values
                line = f"| {row['Date'].strftime('%d - %b - %Y'):^{col_widths['Date']}} | "
                line += f"{short_desc_wrapped[i]:^{col_widths['Short Description']}} | "
                line += f"{link_wrapped[i]:^{col_widths['Link to powerpoint']}} | "
                line += f"{row['Expected project length']:^{col_widths['Expected project length']}} |"
                rows.append(line)
            else:
                # Add additional lines of the row with blank date and project length values
                line = f"| {'':^{col_widths['Date']}} | "
                if i < len(short_desc_wrapped):
                    line += f"{short_desc_wrapped[i]:^{col_widths['Short Description']}} | "
                else:
                    line += f"{'':^{col_widths['Short Description']}} | "
                if i < len(link_wrapped):
                    line += f"{link_wrapped[i]:^{col_widths['Link to powerpoint']}} | "
                else:
                    line += f"{'':^{col_widths['Link to powerpoint']}} | "
                line += f"{'':^{col_widths['Expected project length']}} |"
                rows.append(line)

        # Add the separator between rows to the list
        rows.append('-' * len(header))

    # Join the rows into a single string and return it
    return '\n'.join(rows)
        
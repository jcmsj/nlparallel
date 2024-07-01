# Ways a word may be misspelled:
# 1. Insertion: hello -> helllo
#  1.1 # space separated h e l l o
# 2. Deletion: hello -> helo
# 3. Substitution: hello -> hallo
# Must handle spaces

# Algo:
# 1. Read the profanity data
# 2. Apply string search (KMP) w/ the profanity words as the pattern
# 3. dictionary check
# 4. Find words w/ edit distance <= 3
# 5. Detect unusual amount of spaces
#    Possible regex test: \w+\s*\w+
# h e l l o -> hello
# 6. Everytime a match happens from the above, note:
#   1. location,
#   2. word typed,
#   3. profanity word

# Handling false positives:
#  assemble -> ass
#   false xerox
from lang import lemmatize_en, lemmatize_fil, columns as candidateColumns, en, fil
from prepare import Candidate, scan_text
import concurrent.futures

# argparse
def cli():
    import argparse

    parser = argparse.ArgumentParser(description="Scan text for profanity")
    parser.add_argument("text", type=str, help="Text to scan")
    parser.add_argument(
        "-d",
        "--distance",
        type=int,
        default=4,
        help="Maximum edit distance to consider a word as a profanity",
    )
    # distance fil
    parser.add_argument(
        "-d-fil",
        "--distance-filipino",
        type=int,
        default=4,
        help="Overide for edit distance for Filipino",
    )
    parser.add_argument(
        "-d-en",
        "--distance-english",
        type=int,
        default=4,
        help="Overide for edit distance for English",
    )
    # -o output file
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file to write the results",
    )

    args = parser.parse_args()
    return args


def scan_both(text: str, distanceFil: int, distanceEN: int):
    """Scan text in both languages concurrently
    Args:
        text (str): Text to scan
        distanceFil (int): Maximum edit distance to consider a word as a profanity for Filipino
        distanceEN (int): Maximum edit distance to consider a word as a profanity for English
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        future_fil = executor.submit(
            scan_text_filipino,
            text,
            distanceFil,
        )
        future_english = executor.submit(
            scan_text_english,
            text,
            distanceEN,
        )
        result_fil = future_fil.result()
        result_en = future_english.result()
    return {"fil": result_fil, "en": result_en}

def scan_text_filipino(text, distance):
    # Use filipino-specific globals and arguments
    return scan_text(
        profanity_words=fil.profanity,
        stop_words=fil.stopwords,
        word_dictionary=fil.dictionary,
        lemmatize=lemmatize_fil,
        text=text,
        distance=distance,
    )

def scan_text_english(text, distance):
    # Use english-specific globals and arguments
    return scan_text(
        profanity_words=en.profanity,
        stop_words=en.stopwords,
        word_dictionary=en.dictionary,
        lemmatize=lemmatize_en,
        text=text,
        distance=distance,
    )

def scan_both_non_concurrent(text: str, distanceFil: int, distanceEN: int):
    result_fil = scan_text_filipino(text, distanceFil)
    result_en = scan_text_english(text, distanceEN)
    return {"fil": result_fil, "en": result_en}

def toDf(cs: list[Candidate]):
    import pandas as pd

    return pd.DataFrame.from_records(cs, columns=candidateColumns)


def main():
    """Run if main module"""
    import pandas as pd

    args = cli()
    # override distance for filipino and english
    distanceEN = args.distance_english or args.distance
    distanceFil = args.distance_filipino or args.distance
    result: dict[str, list[Candidate]] = scan_both(
        args.text, distanceFil=distanceFil, distanceEN=distanceEN
    )
    # combine the results while adding a language column
    df_fil = toDf(result["fil"])
    df_en = toDf(result["en"])
    result_fil = df_fil.assign(language="fil")
    result_en = df_en.assign(language="en")
    combined = pd.concat([result_fil, result_en])
    if args.output:
        combined.to_csv(args.output, index=False)
    else:
        print(combined)


if __name__ == "__main__":
    main()

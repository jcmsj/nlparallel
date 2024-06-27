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
import nltk
from collections import namedtuple

from english import profanity_words,en_trie, stop_words_en

# import pygtrie

WordSpan = namedtuple("WordSpan", ["word", "start", "end"])
def remove_stop_words(text: str) -> list[WordSpan]:
    tokenizer = nltk.WordPunctTokenizer()
    spans = list(tokenizer.span_tokenize(text))
    tokens = [text[start:end] for start, end in spans]
    # converts the words in word_tokens to lower case and then checks whether
    # they are present in stop_words or not
    filtered = [
        WordSpan(
            word=w,
            start=spans[i][0],
            end=spans[i][1],
        )
        for i, w in enumerate(tokens)
        if not w.lower() in stop_words_en
    ]
    return filtered

lemmamedWordSpan = namedtuple("lemmamedSpan", ["lemma", "word", "start", "end"])
def lemmatize(span: list[WordSpan]):
    lemmamer = nltk.WordNetLemmatizer()
    
    return [
        lemmamedWordSpan(
            lemma=lemmamer.lemmatize(wordSpan.word),
            word=wordSpan.word,
            start=wordSpan.start,
            end=wordSpan.end,
        )
        for wordSpan in span
    ]

# Declaring namedtuple()
Candidate = namedtuple(
    "Candidate", ["lemma", "word", "start", "end", "profanity", "edit_distance"]
)

def scan_text(text: str, distance: int, substitution_cost:int=1, transpositions:bool=False) -> list[Candidate]:
    """
    Scans the text for profanity words with an edit distance up to `distance`
    """
    no_stop_words_spans = remove_stop_words(text)
    filtered_spans = lemmatize(no_stop_words_spans)
    max_distance = distance+1
    matched: dict[str, list[Candidate]] = {}
    # loop through the filtered words and check if it is the matched, if it is, add to the matched, if a word is matched w/ a different profanity word, keep the one w/ the lowest edit distance
    for span in filtered_spans:
        # skip one char words
        if len(span.word) <= 1:
            continue

        lowerLemma = span.lemma.lower()
        if lowerLemma in en_trie:
            continue

        min_candidates = []
        min_distance = max_distance

        # if span.word is in matched, copy the profanity and edit_distance

        for profanity in profanity_words:
        # Remove words in the dictionary based on the lemma
            edit_distance = nltk.edit_distance(
                profanity, 
                lowerLemma, 
                substitution_cost=substitution_cost, 
                transpositions=transpositions)
            # compare w/ distance, then w/ min_candidate
            # skip words w/ the same edit distance for both word and lemma
            if edit_distance > distance or edit_distance == len(span.lemma): # or edit_distance == len(span.word) or :
                continue
            c = Candidate(
                lemma=span.lemma,
                word=span.word,
                start=span.start,
                end=span.end,
                profanity=profanity,
                edit_distance=edit_distance,
                # min(
                #     nltk.edit_distance(profanity, span.word), 
                #     nltk.edit_distance(profanity, span.lemma)
                # ),
            )
          
            if c.edit_distance == 0:
                min_candidates = [c]
                break
            elif c.edit_distance < min_distance:
                min_candidates = [c]
                min_distance = c.edit_distance
            elif c.edit_distance == min_distance:
                min_candidates.append(c)

        if len(min_candidates) > 0:
            if (span.word in matched):
                matched[span.word].extend(min_candidates)
            else:
                matched[span.word] = min_candidates
    # flatten matched into a list return value
    return [item for sublist in matched.values() for item in sublist]

import multiprocessing as mp

# argparse
def cli():
    import argparse
    parser = argparse.ArgumentParser(description="Scan text for profanity")
    parser.add_argument("text", type=str, help="Text to scan")
    parser.add_argument(
        "-d","--distance",
        type=int,
        default=1,
        help="Maximum edit distance to consider a word as a profanity",
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

def main():
    """Run if main module"""
    import pandas as pd
    args = cli()
    candidates = scan_text(args.text, args.distance)
    pd.DataFrame.from_records(candidates)
    if args.output:
        pd.DataFrame.from_records(candidates).to_csv(args.output, index=False)
    else:
        print(candidates)

if __name__ == "__main__":
    main()

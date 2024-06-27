import pandas as pd

# from networkx import prefix_tree
# Download some nltk datasets
from nltk.corpus import words
from nltk.corpus import stopwords
def load_en_stopwords():
    # check if file stopwords.en.pickle exists
    import pickle
    try:
        with open("stopwords.en.pickle", "rb") as f:
            stop_words = pickle.load(f)
            return stop_words

    except FileNotFoundError:
        stop_words = set(stopwords.words("english"))
        with open("stopwords.en.pickle", "wb") as f:
            pickle.dump(stop_words, f)
        return stop_words
stop_words_en = load_en_stopwords()
def data_clean():
    df = pd.read_csv("./datasets/profanity_en.csv")
    # export to profanity_cleaned_en
    # keep columns: canonical_form_1, category_1, severity_rating, severity_description
    df = df[
        ["canonical_form_1", "category_1", "severity_rating", "severity_description"]
    ]
    # remove duplicate values based on canonical_form_1
    df = df.drop_duplicates(subset=["canonical_form_1"])
    df.to_csv("./datasets/profanity_cleaned_en.csv", index=False)

# define a type lang: EN|PH
def read_data(lang: str):
    df = pd.read_csv(f"./datasets/profanity_cleaned_{lang}.csv")

def load_profanity():
    # check if file profanity.pickle exists
    import pickle
    try:
        with open("profanity.pickle", "rb") as f:
            profanity_words = pickle.load(f)
            return profanity_words

    except FileNotFoundError:
        df = pd.read_csv("./datasets/profanity_cleaned_en.csv")
        profanity_words = set(df["canonical_form_1"].unique())
        with open("profanity.pickle", "wb") as f:
            pickle.dump(profanity_words, f)
        return profanity_words

profanity_words = load_profanity()
def load_en() -> set[str]:
    # check if file en.pickle exists
    import pickle
    try:
        with open("en.pickle", "rb") as f:
            en_dictionary: set[str] = pickle.load(f)
            return en_dictionary

    except FileNotFoundError:
        counting_numbers = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
        ]
        # Remove profanity words from the dictionary
        en_dictionary = (set(words.words()) - profanity_words).union(counting_numbers)
        with open("en.pickle", "wb") as f:
            pickle.dump(en_dictionary, f)
        return en_dictionary
# en_dictionary = load_en()
# en_dictionary_trie = prefix_tree(en_dictionary - profanity_words)
# for number in counting_numbers:
#     en_dictionary_trie.add_node(number)

import pygtrie as trie

# Convert profanity_words to a Trie
def load_en_trie() -> trie.CharTrie:
    # check if file en_trie.pickle exists
    import pickle
    try:
        with open("en_trie.pickle", "rb") as f:
            en_trie: trie.CharTrie = pickle.load(f, encoding="utf-8")
            return en_trie

    except FileNotFoundError:
        en = trie.CharTrie()
        for word in load_en():
            en[word] = True
        with open("en_trie.pickle", "wb") as f:
            pickle.dump(en, f)
        return en
    
en_trie = load_en_trie()
__test__ = {
    "removes profanity words": """
>>> "piss" not in en_trie
True
""",
    "has counting numbers": """
>>> "one" in en_trie
True
""",
}
if __name__ == "__main__":
    import doctest

    doctest.testmod()

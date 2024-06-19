import pandas as pd

# from networkx import prefix_tree
# Download some nltk datasets
import nltk
from nltk.corpus import words


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
    return df


profanity_data = read_data("en")
profanity_words = set(profanity_data["canonical_form_1"].unique())
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

# en_dictionary_trie = prefix_tree(en_dictionary - profanity_words)
# for number in counting_numbers:
#     en_dictionary_trie.add_node(number)
__test__ = {
    "removes profanity words": """
>>> "piss" not in en_dictionary
True
""",
    "has counting numbers": """
>>> "one" in en_dictionary
True
""",
}
if __name__ == "__main__":
    import doctest

    doctest.testmod()

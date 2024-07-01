
import msgspec
import pygtrie as trie
class LanguageData(msgspec.Struct):
    profanity: set[str]
    dictionary: set[str]
    stopwords: set[str]

def load(language_code:str):
    with open(f"{language_code}.json", "rb") as f:
        return msgspec.json.decode(f.read(), type=LanguageData)

def generate_en():
    import pandas as pd
    from nltk.corpus import words
    df = pd.read_csv("./datasets/profanity_cleaned_en.csv")
    profanity_words = set(df["canonical_form_1"].unique())

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

    # make stopwords
    from nltk.corpus import stopwords
    stopwords = set(stopwords.words("english"))

    # dump to json
    with open("en.json", "wb") as f:
        bytes = msgspec.json.encode(LanguageData(
            dictionary=en_dictionary,
            profanity=profanity_words,
            stopwords=stopwords
        ))
        f.write(bytes)
    # export to en.json

def generate_fil():
    import filipino
    with open("fil.json", "wb") as f:
        bytes = msgspec.json.encode(LanguageData(
            dictionary=filipino.dictionary_words,
            profanity=filipino.filipino_profanity_list,
            stopwords=filipino.filipino_stopwords
        ))
        f.write(bytes)

def main():
    '''Run if main module'''
    generate_en()
    generate_fil()

if __name__ == '__main__':
    main()

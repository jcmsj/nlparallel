import nltk
from nltk.corpus import wordnet as wn
from loader import load
from collections import namedtuple
WordSpan = namedtuple("WordSpan", ["word", "start", "end"])
LemmedWordSpan = namedtuple("lemmamedSpan", ["lemma", "word", "start", "end"])
columns = ["lemma", "word", "start", "end", "profanity", "edit_distance"]
Candidate = namedtuple("Candidate", columns)
wn.ensure_loaded()
def lemmatize_en(span: list[WordSpan]):
    lemmer = nltk.WordNetLemmatizer()
    return [
        LemmedWordSpan(
            lemma=lemmer.lemmatize(wordSpan.word),
            word=wordSpan.word,
            start=wordSpan.start,
            end=wordSpan.end,
        )
        for wordSpan in span
    ]

def lemmatize_fil(span: list[WordSpan]):
    return [
        LemmedWordSpan(
            lemma=wordSpan.word,
            word=wordSpan.word,
            start=wordSpan.start,
            end=wordSpan.end,
        )
        for wordSpan in span
    ]

en = load('en')
fil = load('fil')

import nltk
from collections import namedtuple
WordSpan = namedtuple("WordSpan", ["word", "start", "end"])
lemmedWordSpan = namedtuple("lemmamedSpan", ["lemma", "word", "start", "end"])
Candidate = namedtuple("Candidate", ["lemma", "word", "start", "end", "profanity", "edit_distance"])
def remove_stop_words(text: str, stop_words) -> list[WordSpan]:
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
        if not w.lower() in stop_words
    ]
    return filtered

def lemmatize(span: list[WordSpan]):
    lemmer = nltk.WordNetLemmatizer()
    return [
        lemmedWordSpan(
            lemma=lemmer.lemmatize(wordSpan.word),
            word=wordSpan.word,
            start=wordSpan.start,
            end=wordSpan.end,
        )
        for wordSpan in span
    ]
def prepare(profanity_words, stop_words, word_dictionary):

    def scan_text(text: str, distance: int, substitution_cost: int = 1, transpositions: bool = False) -> list[Candidate]:
        no_stop_words_spans = remove_stop_words(text=text, stop_words=stop_words)
        filtered_spans = lemmatize(no_stop_words_spans)
        max_distance = distance + 1
        matched: dict[str, list[Candidate]] = {}

        for span in filtered_spans:
            if len(span.word) <= 1:
                continue

            lowerLemma = span.lemma.lower()
            if lowerLemma in word_dictionary:
                continue

            min_candidates = []
            min_distance = max_distance

            for profanity in profanity_words:
                edit_distance = nltk.edit_distance(
                    profanity,
                    lowerLemma,
                    substitution_cost=substitution_cost,
                    transpositions=transpositions
                )

                if edit_distance > distance:
                    continue

                c = Candidate(
                    lemma=span.lemma,
                    word=span.word,
                    start=span.start,
                    end=span.end,
                    profanity=profanity,
                    edit_distance=edit_distance,
                )

                if c.edit_distance < min_distance:
                    min_candidates = [c]
                    min_distance = c.edit_distance
                elif c.edit_distance == min_distance:
                    min_candidates.append(c)

            if len(min_candidates) > 0:
                if span.word in matched:
                    matched[span.word].extend(min_candidates)
                else:
                    matched[span.word] = min_candidates

        return [item for sublist in matched.values() for item in sublist]

    return scan_text

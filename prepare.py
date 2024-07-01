import concurrent.futures
from typing import Callable
import nltk
from lang import WordSpan, LemmedWordSpan, Candidate

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
        if len(w)>1 and not w.lower() in stop_words
    ]
    return filtered
# Function to apply remove_stop_words to a sentence and adjust spans
def process_sentence(sentence, offset, stop_words):
    filtered_spans = remove_stop_words(sentence, stop_words)
    # Adjust the start and end positions
    adjusted_spans = [
        WordSpan(word=span.word, start=span.start + offset, end=span.end + offset)
        for span in filtered_spans
    ]
    return adjusted_spans

# NO SPEEDUP
# def remove_stop_words_concurrent(text: str, stop_words, workers: int = 4) -> list[WordSpan]:
#     # Split the text into sentences
#     sentences = nltk.sent_tokenize(text)

#     # Use ProcessPoolExecutor to apply remove_stop_words in parallel
#     # no need to maintain order
#     futures: list[concurrent.futures.Future[list[WordSpan]]] = []
#     with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
#         # Prepare arguments for each sentence
#         for i, sentence in enumerate(sentences):
#             offset = sum(len(sentences[j]) for j in range(i))
#             future = executor.submit(process_sentence, sentence, offset, stop_words)
#             futures.append(future)

#     # Flatten the results
#     return [span for future in futures for span in future.result()]

def scan_text(
    profanity_words:set[str], stop_words:set[str], word_dictionary:set[str],
    lemmatize: Callable[[list[WordSpan]], list[LemmedWordSpan]],
    text: str, distance: int, substitution_cost: int = 1, transpositions: bool = False
):
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

def find_candidates_for_span(span, profanity_words, word_dictionary, distance, substitution_cost, transpositions):
    if len(span.word) <= 1:
        return []

    lowerLemma = span.lemma.lower()
    if lowerLemma in word_dictionary:
        return []

    max_distance = distance + 1
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

    return min_candidates

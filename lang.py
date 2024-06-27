from prepare import prepare
from filipino import dictionary_words, filipino_profanity_list,filipino_stopwords
import english
scan_english = prepare(english.profanity_words, english.stop_words_en, english.en_trie)
scan_filipino = prepare(
    profanity_words=filipino_profanity_list, 
    stop_words=filipino_stopwords, 
    word_dictionary=dictionary_words
)

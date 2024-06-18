from main import scan_text,Candidate
__test__ = {
    "Matches 'shit'": """ 
>>> text="piece of shit"
>>> scan_text(text, distance=1)
[Candidate(lemma='shit', word='shit', start=9, end=13, profanity='shit', edit_distance=0)]
""",
    "matches 'fvcking'":"""
>>> text="fvcking hell"
>>> results = scan_text(text, distance=4)
>>> Candidate(lemma='fvcking', word='fvcking', start=0, end=7, profanity='fuck', edit_distance=4) in results
True
>>> Candidate(lemma='hell', word='hell', start=8, end=12, profanity='hell', edit_distance=0) in results
True
"""
}

if __name__ == "__main__":
    import doctest

    doctest.testmod()

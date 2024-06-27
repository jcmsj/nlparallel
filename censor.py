from prepare import Candidate

def censor(text:str, candidates: list[Candidate], replacement:str='*'):
    """
    Censors the text based on the candidates
    """
    censored_text = text
    for candidate in candidates:
        censored_text = censored_text[:candidate.start] + replacement*len(candidate.word) + censored_text[candidate.end:]
    return censored_text

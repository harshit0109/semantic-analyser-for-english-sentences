import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

def tokenize_sentence(sentence):
    # Tokenize the sentence
    tokens = word_tokenize(sentence.lower())
    # POS tagging (for debugging / later use, but not for parser)
    pos_tags = pos_tag(tokens)
    print("POS Tags:", pos_tags)   # just to see
    return tokens

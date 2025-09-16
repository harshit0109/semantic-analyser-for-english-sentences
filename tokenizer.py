# tokenizer.py
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

def tokenize_sentence(sentence):
    # Step 1: Tokenize words
    tokens = word_tokenize(sentence)
    
    # Step 2: POS tagging
    pos_tags = pos_tag(tokens)
    
    return pos_tags

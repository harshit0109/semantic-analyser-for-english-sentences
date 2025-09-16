import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def tokenize_sentence(sentence):
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)
    print("POS Tags:", pos_tags)
    return tokens, pos_tags

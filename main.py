import nltk
from nltk import pos_tag, word_tokenize
from parser import parse_sentence
from semantic_analyzer import extract_semantics, lemmatize_tokens, pretty_print_semantics

def main():
    sentence = input("Enter an English sentence: ")
    
    # Tokenize and POS tagging
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)
    print("POS Tags:", pos_tags)
    
    # Lemmatize verbs to match grammar
    tokens = lemmatize_tokens(tokens, pos_tags)
    print("Tokens:", tokens)
    
    # Parse the sentence
    trees = parse_sentence(tokens)
    
    # Extract semantic roles
    for tree in trees:
        semantics = extract_semantics(tree)
        pretty_print_semantics(semantics)

if __name__ == "__main__":
    # Ensure required NLTK data
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    
    main()

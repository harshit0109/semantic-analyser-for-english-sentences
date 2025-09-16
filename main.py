# import nltk
# nltk.download('punkt')       # Tokenizer
# nltk.download('averaged_perceptron_tagger')  # POS tagging

# main.py
from tokenizer import tokenize_sentence

def main():
    sentence = input("Enter an English sentence: ")
    tokens = tokenize_sentence(sentence)
    print("Tokens:", tokens)

if __name__ == "__main__":
    main()


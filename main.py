from tokenizer import tokenize_sentence
from parser import parse_sentence
from semantic_analyzer import extract_semantics

def main():
    sentence = input("Enter an English sentence: ")
    
    # Step 1: Tokenize
    tokens = tokenize_sentence(sentence)
    print("Tokens:", tokens)
    
    # Step 2: Parse
    trees = parse_sentence(tokens)
    if not trees:
        return
    
    # Step 3: Semantic analysis (use the first parse tree)
    semantics = extract_semantics(trees[0])
    print("Semantic Roles:", semantics)

if __name__ == "__main__":
    main()

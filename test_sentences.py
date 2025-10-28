from semantic_analyzer import SemanticAnalyzer

def test_sentences():
    analyzer = SemanticAnalyzer()
    test_sentences = [
        "The student reads a book.",
        "The teacher teaches mathematics.",
        "A person walks to the park.",
        "The computer is on the table.",
        "She works quickly at the office.",
        "The big house is beautiful.",
        "A happy student studies well.",
        "The red car moves slowly."
    ]
    
    for sentence in test_sentences:
        print(f"\nAnalyzing: {sentence}")
        try:
            result = analyzer.analyze(sentence)
            print("Analysis successful!")
            print(f"Semantic form: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_sentences()
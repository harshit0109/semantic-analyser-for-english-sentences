from semantic_analyzer import SemanticAnalyzer
from main import analyze_and_display

if __name__ == '__main__':
    analyzer = SemanticAnalyzer()
    with open('sample_paragraphs.txt', 'r', encoding='utf-8') as fh:
        content = fh.read()
    # simple split on full stop
    sentences = [s.strip() for s in content.split('.') if s.strip()]
    for s in sentences:
        analyze_and_display(analyzer, s)

"""
main.py - Main Program
Complete implementation of Simmons & Burger (1968) Semantic Analyzer

Run examples from the paper:
1. "The angry pitcher struck the careless batter"
2. "Time flies like arrows"
3. "Old men eat fish"
4. "The condor of North America called the California Condor is the largest land bird on the continent"
"""

from semantic_analyzer import SemanticAnalyzer
import json

def print_separator(char='=', length=60):
    print(char * length)

def main():
    analyzer = SemanticAnalyzer()
    
    # Example sentences from the paper
    examples = [
        "the angry pitcher struck the careless batter",
        "time flies like arrows",
        "old men eat fish",
        # Simpler version of the condor sentence for testing
        "the condor is the largest bird",
    ]
    
    print("\n" + "="*70)
    print(" SEMANTIC ANALYZER - Simmons & Burger (1968) Implementation")
    print("="*70 + "\n")
    
    # Interactive mode or batch mode
    print("Choose mode:")
    print("1. Run example sentences from paper")
    print("2. Enter your own sentence")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        # Run all examples
        for i, sentence in enumerate(examples, 1):
            print(f"\n{'#'*70}")
            print(f"# EXAMPLE {i}")
            print(f"{'#'*70}\n")
            
            analyze_and_display(analyzer, sentence)
            
            if i < len(examples):
                input("\nPress Enter to continue to next example...")
    
    else:
        # Interactive mode
        while True:
            print("\n" + "="*70)
            sentence = input("\nEnter sentence (or 'quit' to exit): ").strip()
            
            if sentence.lower() in ['quit', 'exit', 'q']:
                break
            
            if not sentence:
                continue
            
            analyze_and_display(analyzer, sentence)

def analyze_and_display(analyzer, sentence):
    """Analyze a sentence and display results"""
    
    # Perform analysis
    interpretations = analyzer.analyze(sentence)
    
    # Display results
    print_separator('=')
    print("ANALYSIS RESULTS")
    print_separator('=')
    print()
    
    if not interpretations:
        print("❌ No valid interpretations found.")
        print("\nPossible reasons:")
        print("  - Words not in lexicon")
        print("  - No matching SEF patterns")
        print("  - Ordering constraints violated")
        return
    
    print(f"✓ Found {len(interpretations)} interpretation(s)\n")
    
    for i, interp in enumerate(interpretations, 1):
        print(f"\n{'─'*60}")
        print(f"Interpretation {i}:")
        print(f"{'─'*60}")
        
        # Format as surface relational structure
        print("\nSurface Relational Structure:")
        surface = analyzer.format_interpretation(interp, None)
        print(f"  {surface}")
        
        # Get sentence classes for sense selection
        tokens = sentence.lower().split()
        sentence_classes = {}
        for j, word in enumerate(tokens, 1):
            senses = analyzer.lexicon.lookup(word)
            if senses:
                sentence_classes[j] = {
                    'word': word,
                    'senses': senses,
                    'classes': []
                }
        
        # Select word senses
        sense_interp = analyzer.select_word_senses(interp, sentence_classes)
        
        if sense_interp:
            print("\nWith Word Sense Selection:")
            sense_structure = analyzer.format_with_senses(sense_interp)
            print(f"  {sense_structure}")
        
        # Show the semantic interpretation details
        print("\nSemantic Event Forms Used:")
        sefs_used = analyzer._collect_sefs(interp)
        for sef in set(str(s) for s in sefs_used):
            print(f"  • {sef}")
    
    print("\n" + "="*70)

def demonstrate_features():
    """Demonstrate specific features mentioned in the paper"""
    
    analyzer = SemanticAnalyzer()
    
    print("\n" + "="*70)
    print(" DEMONSTRATING KEY FEATURES FROM PAPER")
    print("="*70 + "\n")
    
    # Feature 1: Sense Disambiguation
    print("FEATURE 1: Word Sense Disambiguation")
    print("-" * 60)
    print("\nThe word 'pitcher' has 2 senses:")
    print("  1. PERSON (baseball player)")
    print("  2. CONTAINER (liquid holder)")
    print("\nThe word 'strike' has 3 senses:")
    print("  1. DISCOVER, FIND")
    print("  2. BOYCOTT, REFUSE")
    print("  3. HIT, TOUCH")
    
    print("\nSentence: 'the angry pitcher struck the careless batter'")
    print("\nSemantic Event Forms restrict combinations:")
    print("  • (PERSON MOD EMOTION) - allows 'angry pitcher' as PERSON")
    print("  • (PERSON HIT PERSON) - selects HIT sense of 'struck'")
    print("\nResult: pitcher_1 (PERSON), struck_3 (HIT)")
    
    input("\nPress Enter to continue...")
    
    # Feature 2: Multiple Interpretations
    print("\n\nFEATURE 2: Multiple Interpretations")
    print("-" * 60)
    print("\nSentence: 'Time flies like arrows'")
    print("\nThis sentence has 3 interpretations:")
    print("  1. TIME (moves) LIKE ARROWS - time passes quickly")
    print("  2. (Command) TIME the FLIES as you would time ARROWS")
    print("  3. FLIES (insects) are SIMILAR to ARROWS in some way")
    
    input("\nPress Enter to see full analysis...")
    
    analyze_and_display(analyzer, "time flies like arrows")
    
    # Feature 3: SEF as Selection Restrictions
    print("\n\nFEATURE 3: SEFs Replace Selection Restrictions")
    print("-" * 60)
    print("\nTraditional approach (Katz):")
    print("  - Words have selection restrictions: <ANIMATE>, <INANIMATE>")
    print("  - Projection rules check compatibility")
    print("\nSimmons & Burger approach:")
    print("  - SEFs directly encode valid combinations")
    print("  - (PERSON MOD EMOTION) allows 'angry person'")
    print("  - No SEF like (CONTAINER MOD EMOTION) exists")
    print("  - Therefore 'angry pitcher' can only mean pitcher_1 (PERSON)")
    
    input("\nPress Enter to continue...")
    
    print("\n\n" + "="*70)
    print(" Demo complete!")
    print("="*70 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demonstrate_features()
    else:
        main()
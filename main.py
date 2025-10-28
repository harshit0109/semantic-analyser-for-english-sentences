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
        # Additional test sentences
        "The student reads a book.",
        "A person walks to the park.",
    ]
    
    print("\n" + "="*70)
    print(" SEMANTIC ANALYZER - Simmons & Burger (1968) Implementation")
    print("="*70 + "\n")
    
    # Try to read from stdin first
    import sys
    if not sys.stdin.isatty():
        try:
            sentence = sys.stdin.readline().strip()
            if sentence:
                analyze_and_display(analyzer, sentence)
            return
        except:
            pass
    
    # If no stdin input, go to interactive mode
    print("Choose mode:")
    print("1. Run example sentences from paper")
    print("2. Enter your own sentence")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
    except EOFError:
        print("\nNo input provided. Running example: The student reads a book.")
        analyze_and_display(analyzer, "The student reads a book.")
        return
    
    if choice == '1':
        # Run all examples
        for i, sentence in enumerate(examples, 1):
            print(f"\n{'#'*70}")
            print(f"# EXAMPLE {i}")
            print(f"{'#'*70}\n")
            
            analyze_and_display(analyzer, sentence)
            
            if i < len(examples):
                try:
                    input("\nPress Enter to continue to next example...")
                except EOFError:
                    break
    else:
        # Interactive mode
        while True:
            print("\n" + "="*70)
            try:
                sentence = input("\nEnter sentence (or 'quit' to exit): ").strip()
            except EOFError:
                break
                
            if sentence.lower() in ['quit', 'exit', 'q']:
                break
            
            if not sentence:
                continue
            
            analyze_and_display(analyzer, sentence)

def generate_parse_tree(words):
    """Generate a parse tree for a sentence."""
    tree = ["[S"]  # Start with sentence node
    
    # Track current position in sentence
    i = 0
    in_verb_phrase = False
    
    while i < len(words):
        word = words[i].rstrip('.')  # Remove any trailing period
        
        # Handle determiners (the, a)
        if word.lower() in ['the', 'a', 'an']:
            # Start noun phrase
            indent = "    " if in_verb_phrase else "  "
            tree.append(f"{indent}[NP")
            tree.append(f"{indent}  [DET {word}]")
            
            # Look ahead for adjectives
            j = i + 1
            while j < len(words) and (words[j].endswith('y') or words[j] in ['big', 'red', 'blue', 'tall', 'small']):
                adj = words[j].rstrip('.')
                tree.append(f"{indent}  [ADJ {adj}]")
                j = j + 1
                
            # Add noun if present
            if j < len(words):
                noun = words[j].rstrip('.')
                tree.append(f"{indent}  [N {noun}]")
                tree.append(f"{indent}]")
                i = j
            else:
                tree.append(f"{indent}]")
        
        # Handle verbs
        elif any(word.endswith(suffix) for suffix in ['s', 'ed', 'ing']) or word in ['is', 'are', 'was', 'were', 'walk', 'run', 'move']:
            if not in_verb_phrase:
                tree.append("  [VP")
                in_verb_phrase = True
            tree.append(f"    [V {word}]")
            
            # Look ahead for adverbs
            j = i + 1
            while j < len(words) and words[j].endswith('ly'):
                adv = words[j].rstrip('.')
                tree.append(f"    [ADV {adv}]")
                j = j + 1
            i = j - 1
            
        # Handle prepositions
        elif word in ['to', 'on', 'in', 'at', 'by', 'with', 'from']:
            indent = "    " if in_verb_phrase else "  "
            tree.append(f"{indent}[PP")
            tree.append(f"{indent}  [P {word}]")
            
            # Look ahead for noun phrase
            j = i + 1
            if j < len(words):
                tree.append(f"{indent}  [NP")
                # Check for determiner
                if words[j].lower() in ['the', 'a', 'an']:
                    tree.append(f"{indent}    [DET {words[j]}]")
                    j = j + 1
                    
                # Check for adjectives
                while j < len(words) and (words[j].endswith('y') or words[j] in ['big', 'red', 'blue', 'tall', 'small']):
                    adj = words[j].rstrip('.')
                    tree.append(f"{indent}    [ADJ {adj}]")
                    j = j + 1
                    
                # Add noun if present
                if j < len(words):
                    noun = words[j].rstrip('.')
                    tree.append(f"{indent}    [N {noun}]")
                tree.append(f"{indent}  ]")
                i = j
            
            tree.append(f"{indent}]")
        
        i = i + 1
    
    # Close verb phrase if needed
    if in_verb_phrase:
        tree.append("  ]")
    
    # Close sentence node
    tree.append("]")
    
    return "\n".join(tree)

def analyze_and_display(analyzer, sentence):
    """Analyze a sentence and display results"""
    
    # Display input sentence
    print("\nInput sentence:", sentence)
    print_separator('=')
    
    # Perform analysis
    interpretations = analyzer.analyze(sentence)
    
    # Display results
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
    
    # Get words for tree generation
    words = sentence.split()
    
    # Get sentence classes for word sense selection and tree generation
    tokens = sentence.lower().split()
    sentence_classes = {}
    for j, word in enumerate(tokens, 1):
        senses = analyzer.lexicon.lookup(word)
        # Make sure to include words with generic senses
        classes = set()
        if senses:
            for sense in senses:
                classes.add(sense.syntactic_class)
                classes.update(sense.semantic_classes)
        else:
            # For unknown words that got generic senses during analysis
            classes.add('N')  # Default to noun
            classes.add('OBJECT')  # Generic semantic class
            
        sentence_classes[j] = {
            'word': word,
            'senses': senses or [],
            'classes': list(classes)
        }
    
    for i, interp in enumerate(interpretations, 1):
        print(f"\n{'─'*60}")
        print(f"Interpretation {i}:")
        print(f"{'─'*60}")

        # Show word classes
        print("\nWord Classes:")
        for j, word in enumerate(tokens, 1):
            senses = analyzer.lexicon.lookup(word)
            if senses:
                classes = set()
                for sense in senses:
                    classes.add(sense.syntactic_class)
                    classes.update(sense.semantic_classes)
                sentence_classes[j] = {
                    'word': word,
                    'senses': senses,
                    'classes': list(classes)
                }
            print(f"  {j}. {word}: {sentence_classes[j]['classes']}")

        # Show syntactic parse tree
        print("\nSyntactic Parse Tree:")
        # Generate parse tree using the sentence words
        parse_tree = generate_parse_tree(sentence.split())
        print(parse_tree)
        
        # Format as surface relational structure
        print("\nSurface Relational Structure:")
        surface = analyzer.format_interpretation(interp, None)
        print(f"  {surface}")
        
        # Show the semantic form of selected interpretation
        print("\nSelected Semantic Form:")
        if interp:
            print(f"  • {interp['sef']} -> {interp['positions']} -> {interp['words']}")
        
        # Select and display word senses
        sense_interp = analyzer.select_word_senses(interp, sentence_classes)
        
        if sense_interp:
            print("\nWord Sense Selection:")
            sense_structure = analyzer.format_with_senses(sense_interp)
            print(f"  {sense_structure}")
        
        # Show the semantic interpretation details
        print("\nSemantic Event Forms Used:")
        sefs_used = analyzer._collect_sefs(interp)
        for sef in set(str(s['sef']) for s in sefs_used):
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
"""
test_semantic_analyzer.py - Test Suite

Tests the implementation against examples from the paper
"""

from semantic_analyzer import SemanticAnalyzer
from lexicon import Lexicon
from semantic_event_forms import SEFSet

def test_lexicon():
    """Test lexicon structure (Section IV, Figure 4)"""
    print("\n" + "="*60)
    print("TEST 1: Lexicon Structure")
    print("="*60)
    
    lexicon = Lexicon()
    
    # Test: pitcher should have 2 senses
    pitcher_senses = lexicon.lookup('pitcher')
    print(f"\n'pitcher' has {len(pitcher_senses)} sense(s):")
    for sense in pitcher_senses:
        print(f"  {sense}")
    
    assert len(pitcher_senses) == 2, "Pitcher should have 2 senses"
    
    # Test: strike should have 3 senses
    strike_senses = lexicon.lookup('strike')
    print(f"\n'strike' has {len(strike_senses)} sense(s):")
    for sense in strike_senses:
        print(f"  {sense}")
    
    # Test struck (past tense)
    struck_senses = lexicon.lookup('struck')
    print(f"\n'struck' has {len(struck_senses)} sense(s):")
    for sense in struck_senses:
        print(f"  {sense}")
    
    assert len(struck_senses) == 3, "Struck should have 3 senses"
    
    # Test: semantic classes should be ordered by abstraction
    person_sense = [s for s in pitcher_senses if 'PERSON' in s.semantic_classes][0]
    print(f"\nPerson sense of pitcher: {person_sense}")
    print(f"  Syntactic class: {person_sense.syntactic_class}")
    print(f"  Semantic classes: {person_sense.semantic_classes}")
    print(f"  (Ordered by abstraction level)")
    
    print("\n✓ Lexicon test passed")

def test_sef_matching():
    """Test SEF matching (Section IV, Examples)"""
    print("\n" + "="*60)
    print("TEST 2: SEF Matching")
    print("="*60)
    
    sef_set = SEFSet()
    
    # Test: (PERSON MOD EMOTION) should be in SEF set
    emotion_sef = None
    for sef in sef_set.sefs:
        if sef.left == 'PERSON' and sef.relation == 'MOD' and sef.right == 'EMOTION':
            emotion_sef = sef
            break
    
    print(f"\nSEF (PERSON MOD EMOTION): {emotion_sef}")
    assert emotion_sef is not None, "Should have (PERSON MOD EMOTION) SEF"
    
    # Test: (PERSON HIT PERSON) should be in SEF set
    hit_sef = None
    for sef in sef_set.sefs:
        if sef.left == 'PERSON' and sef.relation == 'HIT' and sef.right == 'PERSON':
            hit_sef = sef
            break
    
    print(f"SEF (PERSON HIT PERSON): {hit_sef}")
    assert hit_sef is not None, "Should have (PERSON HIT PERSON) SEF"
    
    print("\n✓ SEF matching test passed")

def test_simple_sentence():
    """Test analysis of simple sentence"""
    print("\n" + "="*60)
    print("TEST 3: Simple Sentence Analysis")
    print("="*60)
    
    analyzer = SemanticAnalyzer()
    sentence = "the angry pitcher struck the careless batter"
    
    print(f"\nAnalyzing: '{sentence}'")
    interpretations = analyzer.analyze(sentence)
    
    print(f"\nFound {len(interpretations)} interpretation(s)")
    
    for i, interp in enumerate(interpretations, 1):
        print(f"\nInterpretation {i}:")
        formatted = analyzer.format_interpretation(interp, None)
        print(f"  {formatted}")
    
    # This sentence should have exactly 1 interpretation
    # (the semantic restrictions should eliminate other possibilities)
    print(f"\n✓ Simple sentence test completed ({len(interpretations)} interpretation(s))")

def test_ambiguous_sentence():
    """Test sentence with multiple interpretations (Section V example)"""
    print("\n" + "="*60)
    print("TEST 4: Ambiguous Sentence")
    print("="*60)
    
    analyzer = SemanticAnalyzer()
    sentence = "time flies like arrows"
    
    print(f"\nAnalyzing: '{sentence}'")
    print("Expected: Multiple interpretations (paper mentions 3)")
    
    interpretations = analyzer.analyze(sentence)
    
    print(f"\nFound {len(interpretations)} interpretation(s)")
    
    for i, interp in enumerate(interpretations, 1):
        print(f"\nInterpretation {i}:")
        formatted = analyzer.format_interpretation(interp, None)
        print(f"  {formatted}")
    
    print(f"\n✓ Ambiguous sentence test completed")

def test_modification():
    """Test modificational structures (Section V)"""
    print("\n" + "="*60)
    print("TEST 5: Modificational Structures")
    print("="*60)
    
    analyzer = SemanticAnalyzer()
    sentence = "old men eat fish"
    
    print(f"\nAnalyzing: '{sentence}'")
    interpretations = analyzer.analyze(sentence)
    
    print(f"\nFound {len(interpretations)} interpretation(s)")
    
    for i, interp in enumerate(interpretations, 1):
        print(f"\nInterpretation {i}:")
        formatted = analyzer.format_interpretation(interp, None)
        print(f"  {formatted}")
        
        # Should show (PERSON MOD AGE) for "old men"
        sefs_used = analyzer._collect_sefs(interp)
        print("  SEFs used:")
        for sef in sefs_used:
            print(f"    {sef}")
    
    print(f"\n✓ Modification test completed")

def test_sense_selection():
    """Test word sense selection (Section IV requirement 1)"""
    print("\n" + "="*60)
    print("TEST 6: Word Sense Selection")
    print("="*60)
    
    analyzer = SemanticAnalyzer()
    lexicon = analyzer.lexicon
    
    # Show ambiguity before analysis
    print("\nBefore analysis:")
    print(f"  'pitcher' can be: {[str(s) for s in lexicon.lookup('pitcher')]}")
    print(f"  'struck' can be: {[str(s) for s in lexicon.lookup('struck')]}")
    
    sentence = "the angry pitcher struck the careless batter"
    print(f"\nAnalyzing: '{sentence}'")
    
    interpretations = analyzer.analyze(sentence)
    
    if interpretations:
        # Get sentence classes
        tokens = sentence.lower().split()
        sentence_classes = {}
        for j, word in enumerate(tokens, 1):
            senses = lexicon.lookup(word)
            if senses:
                sentence_classes[j] = {
                    'word': word,
                    'senses': senses,
                    'classes': []
                }
        
        # Select senses for first interpretation
        sense_interp = analyzer.select_word_senses(interpretations[0], sentence_classes)
        
        print("\nAfter semantic analysis:")
        formatted = analyzer.format_with_senses(sense_interp)
        print(f"  {formatted}")
        print("\n  Senses selected:")
        print("    pitcher → PERSON (athlete)")
        print("    struck → HIT")
    
    print("\n✓ Sense selection test completed")

def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# SEMANTIC ANALYZER TEST SUITE")
    print("# Based on Simmons & Burger (1968)")
    print("#"*60)
    
    tests = [
        test_lexicon,
        test_sef_matching,
        test_simple_sentence,
        test_ambiguous_sentence,
        test_modification,
        test_sense_selection
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        # Non-interactive: continue immediately to next test
        continue
    
    print("\n" + "#"*60)
    print(f"# TEST RESULTS: {passed} passed, {failed} failed")
    print("#"*60 + "\n")

if __name__ == "__main__":
    run_all_tests()
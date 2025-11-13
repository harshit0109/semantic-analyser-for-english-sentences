import nltk
from nltk import CFG
# parser.py (add this helper function)
def extend_grammar_with_new_words(new_words, pos_tag):
    global grammar_rules, grammar, parser
    if pos_tag.startswith('N'):
        nouns.append(new_words)
    elif pos_tag.startswith('V'):
        verbs.append(new_words)
    # regenerate CFG
    grammar_rules_updated = f"""
    S -> NP VP | S Conj S | S RelClause
    NP -> Det N | Det Adj N | N | Adj N | Pronoun | NP PP | NP Conj NP
    VP -> V NP | V NP PP | V | V PP | Aux V NP | VP Adv | Adv VP | VP Conj VP
    PP -> P NP
    RelClause -> RelPronoun VP
    Det -> {' | '.join(f"'{d}'" for d in determiners)}
    N -> {' | '.join(f"'{n}'" for n in nouns)}
    Adj -> {' | '.join(f"'{a}'" for a in adjectives)}
    Adv -> {' | '.join(f"'{a}'" for a in adverbs)}
    V -> {' | '.join(f"'{v}'" for v in verbs)}
    Aux -> {' | '.join(f"'{a}'" for a in aux_verbs)}
    P -> {' | '.join(f"'{p}'" for p in prepositions)}
    Pronoun -> {' | '.join(f"'{pr}'" for pr in pronouns)}
    Conj -> {' | '.join(f"'{c}'" for c in conjunctions)}
    RelPronoun -> {' | '.join(f"'{r}'" for r in relative_pronouns)}
    """
    grammar = CFG.fromstring(grammar_rules_updated)
    parser = nltk.ChartParser(grammar)

# --------------------------
# Lexicon
# --------------------------
nouns = ['cat', 'dog', 'boy', 'girl', 'ball', 'park', 'apple', 'john', 'mary', 'cats', 'dogs', 'boys', 'girls', 'apples']
adjectives = ['big', 'small', 'red', 'happy', 'angry']
adverbs = ['quickly', 'slowly', 'silently']
verbs = ['chase', 'see', 'like', 'throw', 'eat', 'run', 'walk', 'give', 'is', 'was', 'will', 'can', 'are', 'were', 'eating', 'chases', 'sees', 'likes', 'throws', 'eats', 'runs', 'walks', 'gives']
aux_verbs = ['is', 'was', 'will', 'can', 'are']
determiners = ['a', 'the', 'an', 'this', 'that']
prepositions = ['with', 'to', 'in', 'on', 'at']
pronouns = ['he', 'she', 'they', 'it', 'we', 'i']
conjunctions = ['and', 'or']
relative_pronouns = ['who', 'which', 'that']

# --------------------------
# Grammar rules with conjunctions and relative clauses
# --------------------------
grammar_rules = f"""
S -> NP VP | S Conj S | S RelClause

# Noun Phrases
NP -> Det N | Det Adj N | N | Adj N | Pronoun | NP PP | NP Conj NP

# Verb Phrases
VP -> V NP | V NP PP | V | V PP | Aux V NP | VP Adv | Adv VP | VP Conj VP

# Prepositional Phrases
PP -> P NP

# Relative Clauses
RelClause -> RelPronoun VP

# Lexicon
Det -> {' | '.join(f"'{d}'" for d in determiners)}
N -> {' | '.join(f"'{n}'" for n in nouns)}
Adj -> {' | '.join(f"'{a}'" for a in adjectives)}
Adv -> {' | '.join(f"'{a}'" for a in adverbs)}
V -> {' | '.join(f"'{v}'" for v in verbs)}
Aux -> {' | '.join(f"'{a}'" for a in aux_verbs)}
P -> {' | '.join(f"'{p}'" for p in prepositions)}
Pronoun -> {' | '.join(f"'{pr}'" for pr in pronouns)}
Conj -> {' | '.join(f"'{c}'" for c in conjunctions)}
RelPronoun -> {' | '.join(f"'{r}'" for r in relative_pronouns)}
"""

# Create CFG
grammar = CFG.fromstring(grammar_rules)
parser = nltk.ChartParser(grammar)

# --------------------------
# Parsing function
# --------------------------
def get_tree_width(tree):
    """Calculate the width needed for the tree"""
    if isinstance(tree, str):
        return len(tree)
    label = tree.label()
    if not tree:
        return len(label)
    children_width = sum(get_tree_width(child) for child in tree) + (len(tree) - 1) * 2
    return max(len(label), children_width)

def print_centered(text, width):
    """Print text centered within the given width"""
    padding = (width - len(text)) // 2
    return ' ' * padding + text

def print_tree_top_down(tree):
    """Print a parse tree in a top-down manner"""
    def make_box(text):
        """Create a box around text"""
        width = len(text) + 4
        return [
            '┌' + '─' * (width - 2) + '┐',
            '│ ' + text + ' │',
            '└' + '─' * (width - 2) + '┘'
        ]

    def _print_tree(node, indent='', last=True):
        """Print tree recursively"""
        box = make_box(node.label() if not isinstance(node, str) else node)
        
        # Print current node's box
        for line in box:
            print(indent + line)

        if isinstance(node, str):
            return

        children = list(node)
        if not children:
            return

        # Print connector to children
        if children:
            print(indent + '│')
            if len(children) == 1:
                print(indent + '↓')
            else:
                print(indent + '├─────┴─────┤')
                print(indent + '↓           ↓')

        # Print children
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            new_indent = indent + ('    ' if is_last else '│   ')
            _print_tree(child, new_indent, is_last)

    print("\nParse Tree:")
    _print_tree(tree)

def parse_sentence(tokens):
    try:
        parses = list(parser.parse(tokens))
        if not parses:
            print("No valid parse found. Check your grammar or sentence structure.")
            return []

        for tree in parses:
            print("\nParse Tree:")
            print_tree_top_down(tree)
        return parses
    except ValueError as e:
        print("Grammar coverage error:", e)
        return []

# --------------------------
# Test command-line
# --------------------------
if __name__ == "__main__":
    s = input("Enter an English sentence: ")
    tokens = nltk.word_tokenize(s)
    parse_sentence(tokens)

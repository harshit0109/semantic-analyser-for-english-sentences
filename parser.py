import nltk
from nltk import CFG

# --------------------------
# Lexicon
# --------------------------
nouns = ['cat', 'dog', 'boy', 'girl', 'ball', 'park', 'apple', 'john', 'mary']
adjectives = ['big', 'small', 'red', 'happy', 'angry']
adverbs = ['quickly', 'slowly', 'silently']
verbs = ['chases', 'sees', 'likes', 'throws', 'eats', 'runs', 'walks', 'eating', 'gives']
aux_verbs = ['is', 'was', 'will', 'can']
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
def parse_sentence(tokens):
    try:
        parses = list(parser.parse(tokens))
        if not parses:
            print("No valid parse found. Check your grammar or sentence structure.")
            return []

        for tree in parses:
            tree.pretty_print()
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

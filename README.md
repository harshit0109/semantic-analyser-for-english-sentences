# Semantic Analyser for English Sentences

A Python project that **tokenizes English sentences**, performs **POS tagging** using NLTK, parses sentences using a **Context-Free Grammar (CFG)**, and **extracts semantic roles**.

It supports:

- Noun Phrases (NP)
- Verb Phrases (VP)
- Prepositional Phrases (PP)
- Conjunctions
- Relative Clauses
- Nested Clauses and Multiple Modifiers
- Multi-to-Multi Semantic Role Extraction

---

## Semantic Roles Extracted

- **Agents**: Subjects performing the action  
- **Action**: Main verb phrase  
- **Patients**: Objects of the action  
- **Modifiers**: Prepositional phrases or adverbs  
- **Subclauses**: Nested clauses  

---

## Features

- Handles **nested clauses**, **multiple modifiers**, and **conjunctions**  
- Uses CFG with a **lexicon** of nouns, verbs, adjectives, adverbs, pronouns, determiners, prepositions, and conjunctions  
- Uses **lemmatization** to normalize verbs  
- Supports **multi-to-multi semantic role extraction**. Examples:


---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/semantic-analyser-for-english-sentences.git
cd semantic-analyser-for-english-sentences


Install dependecies
pip install -r requirements.txt

Run the main script
python main.py

Example input:
Enter an English sentence: the boy and the girl chase the dog

Output:

POS tags of the sentence

Tokenized words

Parse tree(s)

Extracted semantic roles in readable JSON format

Extending the Grammar and Lexicon

The current CFG and lexicon cover basic English sentences. To handle more complex sentences or specialized vocabulary:

Add new words to the lexicon in parser.py:
nouns += ['teacher', 'student', 'book']
verbs += ['teaches', 'reads', 'writes']
adjectives += ['intelligent', 'tall']


Update grammar rules if needed:
RelClause -> RelPronoun VP | RelPronoun VP Conj VP

Test new sentences by running main.py and verifying parse trees and semantic roles.

Tips

Keep the lexicon organized to avoid conflicts

Include both base and inflected verb forms or rely on lemmatization

Test conjunctions and nested clauses to ensure correct multi-to-multi mapping of Agents and Actions


Dependencies

Python 3.11+

NLTK



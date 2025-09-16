Semantic Analyser for English Sentences
Overview

This project tokenizes English sentences, performs POS tagging using NLTK, parses sentences using a Context-Free Grammar (CFG), and extracts semantic roles. It supports:

Noun phrases (NP)

Verb phrases (VP)

Prepositional phrases (PP)

Conjunctions

Relative clauses

Nested clauses and multiple modifiers

Multi-to-multi semantic role extraction

Semantic Roles Extracted

Agents: Subjects performing the action

Action: Main verb phrase

Patients: Objects of the action

Modifiers: Prepositional phrases or adverbs

Subclauses: Nested clauses

Features

Handles nested clauses, multiple modifiers, and conjunctions

Uses CFG with a lexicon of nouns, verbs, adjectives, adverbs, pronouns, determiners, prepositions, and conjunctions

Uses lemmatization to normalize verbs

Extracts semantic roles in a multi-to-multi manner, supporting sentences like:

"The boy and the girl chase the dog"

"The teacher who teaches math is running quickly"

Installation

Clone the repository:

git clone <your-repo-url>
cd semantic-analyser-for-english-sentences


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt

Usage

Run the main script:

python main.py


Enter an English sentence when prompted, e.g.:

Enter an English sentence: the boy and the girl chase the dog


The program will output:

POS tags of the sentence

Tokenized words

Parse tree(s)

Extracted semantic roles in a readable JSON format

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

Keep the lexicon organized to avoid conflicts.

Include both base and inflected verb forms or rely on lemmatization.

Test conjunctions and nested clauses to ensure correct multi-to-multi mapping of Agents and Actions.

Dependencies

Python 3.11+

NLTK
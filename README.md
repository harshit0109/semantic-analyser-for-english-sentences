# Semantic Analyzer for English Sentences

This project implements a **semantic analyzer** for English sentences. It parses sentences, identifies their grammatical structure, and extracts **semantic roles** such as Agents, Actions, Patients, Modifiers, and Subclauses.

---

## Features

- Tokenizes English sentences and performs POS tagging using **NLTK**.
- Parses sentences using a **Context-Free Grammar (CFG)** with support for:
  - Noun phrases (NP)
  - Verb phrases (VP)
  - Prepositional phrases (PP)
  - Conjunctions
  - Relative clauses
- Extracts semantic roles:
  - **Agents**: Subjects performing the action
  - **Action**: Main verb phrase
  - **Patients**: Objects of the action
  - **Modifiers**: Prepositional phrases or adverbs
  - **Subclauses**: Nested clauses
- Handles nested clauses, multiple modifiers, and conjunctions.

---


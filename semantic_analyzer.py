from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer
import json

lemmatizer = WordNetLemmatizer()

def lemmatize_tokens(tokens, pos_tags):
    lemmatized = []
    for word, tag in pos_tags:
        if tag.startswith('V'):
            lemmatized.append(lemmatizer.lemmatize(word, 'v'))  # verb → base form
        else:
            lemmatized.append(word)
    return lemmatized

def pretty_print_semantics(semantics):
    print("\nSemantic Roles:")
    print(json.dumps(semantics, indent=4))

def extract_semantics(tree):
    """
    Advanced semantic role extraction for nested clauses and conjunctions.
    Returns:
        Agent: list of subjects
        Action: main verb phrase
        Patients: list of objects
        Modifiers: list of PP/Adv
        Subclauses: list of dicts for nested clauses
    """
    roles = {
        "Agents": [],
        "Action": None,
        "Patients": [],
        "Modifiers": [],
        "Subclauses": []
    }

    def get_phrase_leaves(subtree):
        return " ".join(subtree.leaves())

    def traverse_VP(vp_tree):
        action_parts = []
        for child in vp_tree:
            if isinstance(child, Tree):
                if child.label() == "V":
                    action_parts.append(get_phrase_leaves(child))
                elif child.label() == "Aux":
                    action_parts.insert(0, get_phrase_leaves(child))
                elif child.label() == "NP":
                    roles["Patients"].append(get_phrase_leaves(child))
                elif child.label() == "PP":
                    roles["Modifiers"].append(get_phrase_leaves(child))
                elif child.label() == "Adv":
                    roles["Modifiers"].append(get_phrase_leaves(child))
                elif child.label() == "S":  # nested clause
                    sub_roles = extract_semantics(child)
                    roles["Subclauses"].append(sub_roles)
                else:
                    traverse_VP(child)
        if action_parts:
            roles["Action"] = " ".join(action_parts)

    def traverse_NP(np_tree, is_subject=True):
        # Handle conjunctions
        current_agents = []
        for child in np_tree:
            if isinstance(child, Tree):
                if child.label() == "N" or child.label() == "Pronoun" or child.label() == "Det":
                    continue
                elif child.label() == "NP":
                    traverse_NP(child, is_subject)
                elif child.label() == "PP":
                    roles["Modifiers"].append(get_phrase_leaves(child))
                elif child.label() == "Conj":
                    continue
        phrase = get_phrase_leaves(np_tree)
        if is_subject:
            roles["Agents"].append(phrase)
        else:
            roles["Patients"].append(phrase)

    if tree.label() == "S":
        for child in tree:
            if isinstance(child, Tree):
                if child.label() == "NP":
                    traverse_NP(child, is_subject=True)
                elif child.label() == "VP":
                    traverse_VP(child)

    return roles

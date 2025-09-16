from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer
import json

def pretty_print_semantics(semantics):
    print("\nSemantic Roles:")
    print(json.dumps(semantics, indent=4))

lemmatizer = WordNetLemmatizer()

def lemmatize_tokens(tokens, pos_tags):
    lemmatized = []
    for word, tag in pos_tags:
        if tag.startswith('V'):
            lemmatized.append(lemmatizer.lemmatize(word, 'v'))  # verb → base form
        else:
            lemmatized.append(word)
    return lemmatized

def extract_semantics(tree, pos_tags=None):
    """
    Semantic role extraction with tense detection for nested clauses and conjunctions.
    """
    roles = {
        "Agents": [],
        "Action": None,
        "Tense": None,
        "Patients": [],
        "Modifiers": [],
        "Subclauses": []
    }

    # Map words to POS tags for tense detection
    pos_dict = {word.lower(): tag for word, tag in pos_tags} if pos_tags else {}

    def get_phrase_leaves(subtree):
        return " ".join(subtree.leaves())

    def traverse_VP(vp_tree):
        action_parts = []
        for child in vp_tree:
            if isinstance(child, Tree):
                if child.label() == "V":
                    verb = get_phrase_leaves(child)
                    action_parts.append(verb)

                    # Detect tense
                    tag = pos_dict.get(verb.lower())
                    if tag in ['VBD', 'VBN']:
                        roles['Tense'] = 'Past'
                    elif tag in ['VBP', 'VBZ']:
                        roles['Tense'] = 'Present'
                    elif tag == 'VB':
                        roles['Tense'] = 'Base'
                    elif tag == 'VBG':
                        roles['Tense'] = 'Continuous'

                elif child.label() == "Aux":
                    action_parts.insert(0, get_phrase_leaves(child))
                elif child.label() == "NP":
                    roles["Patients"].append(get_phrase_leaves(child))
                elif child.label() == "PP":
                    roles["Modifiers"].append(get_phrase_leaves(child))
                elif child.label() == "Adv":
                    roles["Modifiers"].append(get_phrase_leaves(child))
                elif child.label() == "S":  # nested clause
                    sub_roles = extract_semantics(child, pos_tags)
                    roles["Subclauses"].append(sub_roles)
                else:
                    traverse_VP(child)
        if action_parts:
            roles["Action"] = " ".join(action_parts)

    def traverse_NP(np_tree, is_subject=True):
        for child in np_tree:
            if isinstance(child, Tree):
                if child.label() == "NP":
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

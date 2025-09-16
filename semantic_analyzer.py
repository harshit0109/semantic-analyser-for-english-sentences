from nltk.tree import Tree

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
                    continue  # terminal parts will be combined later
                elif child.label() == "NP":
                    traverse_NP(child, is_subject)
                elif child.label() == "PP":
                    roles["Modifiers"].append(get_phrase_leaves(child))
                elif child.label() == "Conj":  # handle 'and', 'or'
                    continue
        # Collect full phrase
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

# --------------------------
# Test examples
# --------------------------
if __name__ == "__main__":
    from nltk import Tree

    # Nested clause
    tree1 = Tree.fromstring(
        "(S (NP (Det The) (N boy)) (VP (V chases) (NP (Det the) (N dog)) (S (NP (Pronoun who)) (VP (Aux is) (V running)))))"
    )
    print("Nested clause example:", extract_semantics(tree1))

    # Conjunction
    tree2 = Tree.fromstring(
        "(S (NP (NP (Det The) (N cat)) (Conj and) (NP (Det the) (N dog))) (VP (V chase) (NP (Det the) (N ball))))"
    )
    print("Conjunction example:", extract_semantics(tree2))

    # Multiple modifiers
    tree3 = Tree.fromstring(
        "(S (NP (Det The) (N boy)) (VP (V runs) (Adv quickly) (PP (P in) (NP (Det the) (N park)))))"
    )
    print("Multiple modifiers example:", extract_semantics(tree3))

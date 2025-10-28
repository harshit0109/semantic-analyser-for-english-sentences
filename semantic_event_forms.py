"""
semantic_event_forms.py - SEF Implementation
Based on Simmons & Burger (1968) Section IV

SEFs are triples (E-R-E) where elements are syntactic or semantic class markers.
They serve as:
1. Phrase structure rules for syntactic combinations
2. Transformational components for deep structures
3. Sense selectors via semantic class restrictions
"""

class SEF:
    def __init__(self, left, relation, right, order_constraint=None):
        """
        Create a Semantic Event Form
        
        Args:
            left: Left element (syntactic or semantic class)
            relation: Relation (verb, preposition, MOD, etc.)
            right: Right element
            order_constraint: Function that checks word order validity
        """
        self.left = left
        self.relation = relation
        self.right = right
        self.order_constraint = order_constraint
    
    def __repr__(self):
        return f"({self.left} {self.relation} {self.right})"
    
    def matches(self, left_classes, right_classes):
        """Check if word classes match this SEF"""
        return (self.left in left_classes and self.right in right_classes)

class SEFSet:
    def __init__(self):
        self.sefs = []
        self._initialize_sefs()
    
    def _initialize_sefs(self):
        """Initialize SEFs as described in the paper"""
        
        # Syntactic SEFs (basic phrase structure)
        self.add_sef('N', 'V', 'N')  # Subject-Verb-Object
        self.add_sef('N', 'MOD', 'ADJ')  # Noun modified by adjective
        self.add_sef('N', 'MOD', 'ART')  # Noun modified by article
        self.add_sef('V', 'MOD', 'ADV')  # Verb modified by adverb
        self.add_sef('ADJ', 'MOD', 'ADV')  # Adjective modified by adverb
        self.add_sef('N', 'PREP', 'N')  # Prepositional phrase
        self.add_sef('V', 'PREP', 'N')  # Verb with prep phrase
        
        # Semantic SEFs from examples in paper
        # "The angry pitcher struck the careless batter"
        self.add_sef('PERSON', 'MOD', 'EMOTION')
        self.add_sef('PERSON', 'MOD', 'ATTITUDE')
        self.add_sef('PERSON', 'HIT', 'PERSON')
        
        # "Old men eat fish"
        self.add_sef('PERSON', 'MOD', 'AGE')
        self.add_sef('PERSON', 'CONSUME', 'FOOD')
        self.add_sef('PERSON', 'CONSUME', 'ANIMAL')
        
        # "Time flies like arrows"
        self.add_sef('DURATION', 'MOVE', 'WEAPON')
        self.add_sef('INSECT', 'SIMILAR', 'WEAPON')
        self.add_sef('DURATION', 'SIMILAR', 'WEAPON')
        
        # Condor example
        self.add_sef('BIRD', 'LOC', 'PLACE')
        self.add_sef('PLACE', 'PART', 'DIRECTION')
        self.add_sef('BIRD', 'NAME', 'BIRD')
        self.add_sef('BIRD', 'TYPE', 'PLACE')
        self.add_sef('BIRD', 'EQUIV', 'BIRD')
        self.add_sef('BIRD', 'MOD', 'SIZE')
        self.add_sef('ANIMAL', 'LOC', 'LANDMASS')
        
        # General semantic patterns
        self.add_sef('ANIMAL', 'CONSUME', 'ANIMAL')
        self.add_sef('PERSON', 'DISCOVER', 'OBJECT')
        self.add_sef('PERSON', 'BOYCOTT', 'OBJECT')
        
        # Learning and communication patterns
        self.add_sef('PERSON', 'LEARN', 'READABLE')
        self.add_sef('PERSON', 'CREATE', 'READABLE')
        self.add_sef('PERSON', 'COMMUNICATE', 'READABLE')
        self.add_sef('LEARNER', 'LEARN', 'READABLE')
        self.add_sef('EDUCATOR', 'TEACH', 'READABLE')
        
        # Movement patterns
        self.add_sef('PERSON', 'MOVE', 'PLACE')
        self.add_sef('PERSON', 'ARRIVE', 'PLACE')
        self.add_sef('PERSON', 'TRAVEL', 'PLACE')
        
        # Work and activity patterns
        self.add_sef('PERSON', 'LABOR', 'OBJECT')
        self.add_sef('PERSON', 'ENJOY', 'OBJECT')
        self.add_sef('PERSON', 'DO', 'WORK')
        self.add_sef('PERSON', 'DO', 'ACTIVITY')
        
        # Location patterns
        self.add_sef('PERSON', 'BE', 'PLACE')
        self.add_sef('OBJECT', 'BE', 'PLACE')
        self.add_sef('BUILDING', 'BE', 'PLACE')
        
        # Quality patterns
        self.add_sef('PERSON', 'MOD', 'COLOR')
        self.add_sef('OBJECT', 'MOD', 'COLOR')
        self.add_sef('PERSON', 'MOD', 'SIZE')
        self.add_sef('OBJECT', 'MOD', 'SIZE')
        self.add_sef('ACTION', 'MOD', 'SPEED')
        self.add_sef('ACTION', 'MOD', 'MANNER')
        
        # Device and technology patterns
        self.add_sef('PERSON', 'USE', 'DEVICE')
        self.add_sef('DEVICE', 'BE', 'OBJECT')
        
        # Modificational patterns
        self.add_sef('N', 'MOD', 'N')  # Noun-noun modification
        self.add_sef('OBJECT', 'MOD', 'QUALITY')
        self.add_sef('QUALITY', 'MOD', 'INTENSIFIER')
        
        # BE verb patterns
        self.add_sef('N', 'BE', 'N')
        self.add_sef('N', 'BE', 'ADJ')
        self.add_sef('N', 'EQUIV', 'N')
        
        # Relative clause patterns
        self.add_sef('N', 'R/P', 'WHO')
        self.add_sef('N', 'R/P', 'WHICH')
        self.add_sef('N', 'R/P', 'THAT')
        self.add_sef('PERSON', 'R/P', 'WHO')
    
    def add_sef(self, left, relation, right):
        """Add a SEF to the set"""
        self.sefs.append(SEF(left, relation, right))
    
    def get_relevant_sefs(self, word_classes_dict):
        """
        Get SEFs relevant to the sentence (Step 1-2 in paper)
        
        Args:
            word_classes_dict: {word_num: [classes]}
        
        Returns:
            List of relevant SEFs
        """
        all_classes = set()
        for classes in word_classes_dict.values():
            all_classes.update(classes)
        
        relevant = []
        for sef in self.sefs:
            if sef.left in all_classes or sef.right in all_classes:
                relevant.append(sef)
        
        # Filter: keep only SEFs that occur at least twice (Step 2)
        class_counts = {}
        for sef in relevant:
            key = (sef.left, sef.relation, sef.right)
            class_counts[key] = class_counts.get(key, 0) + 1
        
        # Count occurrences based on matching word classes
        sef_occurrences = []
        for sef in relevant:
            count = 0
            for classes in word_classes_dict.values():
                if sef.left in classes or sef.right in classes:
                    count += 1
            if count >= 2:
                sef_occurrences.append(sef)
        
        return sef_occurrences if sef_occurrences else relevant
    
    def create_complex_triples(self, relevant_sefs, sentence_classes):
        """
        Create complex triples with word order numbers (Step 3)
        
        Args:
            relevant_sefs: List of relevant SEFs
            sentence_classes: {word_num: {word: str, classes: [str]}}
        
        Returns:
            List of complex triples: (SEF, (left_num, rel_num, right_num), (left_word, rel_word, right_word))
        """
        complex_triples = []
        
        for sef in relevant_sefs:
            # Find all word positions that match the SEF elements
            left_positions = []
            right_positions = []
            relation_positions = []
            
            for num, info in sentence_classes.items():
                classes = info['classes']
                word = info['word']
                
                if sef.left in classes:
                    left_positions.append((num, word))
                if sef.right in classes:
                    right_positions.append((num, word))
                if sef.relation in classes or word.lower() == sef.relation.lower():
                    relation_positions.append((num, word))
            
            # Create complex triples for all valid combinations
            for left_num, left_word in left_positions:
                for right_num, right_word in right_positions:
                    if left_num != right_num:
                        # For MOD relations, relation position is 0 (implicit)
                        if sef.relation == 'MOD':
                            rel_num = 0
                            rel_word = 'MOD'
                        else:
                            # Try to find explicit relation word
                            rel_num = 0
                            rel_word = sef.relation
                            for rnum, rword in relation_positions:
                                if left_num < rnum < right_num or right_num < rnum < left_num:
                                    rel_num = rnum
                                    rel_word = rword
                                    break
                        
                        complex_triples.append({
                            'sef': sef,
                            'positions': (left_num, rel_num, right_num),
                            'words': (left_word, rel_word, right_word)
                        })
        
        return complex_triples
    
    def filter_by_order(self, complex_triples):
        """
        Filter complex triples by ordering rules (Step 4)
        
        Ordering rules from paper:
        - (N MOD ADJ): N > ADJ
        - (N1 MOD N2): N1 - N2 = 1
        - (N1 V1 N2): N1 < V1 AND NOT V1 < V2 < N2
        etc.
        """
        filtered = []
        
        for ct in complex_triples:
            sef = ct['sef']
            left_num, rel_num, right_num = ct['positions']
            
            valid = True
            
            # Apply ordering rules
            if sef.relation == 'MOD':
                if sef.right in ['ADJ', 'EMOTION', 'ATTITUDE', 'AGE']:
                    # Modifier (adjective) should come before the noun
                    valid = right_num < left_num
                elif sef.right == 'ART':
                    # Article should come before the noun
                    valid = right_num < left_num
                    
            elif sef.relation in ['V', 'HIT', 'CONSUME', 'BE', 'EQUIV']:
                # Subject-Verb-Object order
                valid = left_num < right_num and (rel_num == 0 or left_num < rel_num < right_num)
                
            elif sef.relation == 'SIMILAR':
                # For "like" comparisons
                valid = left_num < rel_num < right_num
            
            if valid:
                filtered.append(ct)
            
            # Rule: N MOD ADJ - noun comes after adjective
            if sef.relation == 'MOD' and sef.right == 'ADJ':
                if left_num < right_num:
                    valid = False
            
            # Rule: N MOD ART - noun comes after article
            elif sef.relation == 'MOD' and sef.right == 'ART':
                if left_num < right_num:
                    valid = False
            
            # Rule: N1 MOD N2 - adjacent nouns only
            elif sef.relation == 'MOD' and sef.left == 'N' and sef.right == 'N':
                if abs(left_num - right_num) != 1:
                    valid = False
            
            # Rule: N1 V N2 - subject before verb before object
            elif sef.left in ['N', 'PERSON', 'ANIMAL', 'OBJECT'] and \
                 sef.relation in ['V', 'HIT', 'CONSUME', 'MOVE', 'BE', 'EQUIV']:
                if not (left_num < rel_num < right_num):
                    valid = False
            
            # Rule: N PREP N - proper ordering
            elif sef.relation == 'PREP' or sef.relation in ['LOC', 'PART']:
                if not (left_num < right_num):
                    valid = False
            
            if valid:
                filtered.append(ct)
        
        return filtered
    
    def eliminate_abstract_duplicates(self, complex_triples):
        """
        Eliminate more abstract SEFs when specific ones exist (Step 5a)
        """
        # Group by positions
        position_groups = {}
        for ct in complex_triples:
            pos = ct['positions']
            if pos not in position_groups:
                position_groups[pos] = []
            position_groups[pos].append(ct)
        
        # For each position, keep only the most specific (least abstract)
        filtered = []
        for pos, cts in position_groups.items():
            if len(cts) == 1:
                filtered.extend(cts)
            else:
                # Prefer semantic classes over syntactic
                best = min(cts, key=lambda ct: self._abstraction_level(ct['sef']))
                filtered.append(best)
        
        return filtered
    
    def _abstraction_level(self, sef):
        """Calculate abstraction level (lower is more specific)"""
        syntactic_classes = {'N', 'V', 'ADJ', 'ADV', 'ART', 'PREP'}
        
        score = 0
        if sef.left in syntactic_classes:
            score += 10
        if sef.right in syntactic_classes:
            score += 10
        if sef.relation in syntactic_classes:
            score += 10
        
        return score
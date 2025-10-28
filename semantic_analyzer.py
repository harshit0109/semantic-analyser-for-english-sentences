"""
semantic_analyzer.py - Main Analysis Algorithm
Based on Simmons & Burger (1968) Section IV

The analyzer:
1. Looks up words in lexicon
2. Selects relevant SEFs
3. Creates complex triples with word order
4. Filters by ordering rules
5. Generates parse structures
6. Produces deep structure interpretations
"""

from lexicon import Lexicon
from semantic_event_forms import SEFSet

class SemanticAnalyzer:
    def __init__(self):
        self.lexicon = Lexicon()
        self.sef_set = SEFSet()
    
    def analyze(self, sentence):
        """
        Main analysis procedure
        
        Args:
            sentence: String or list of tokens
        
        Returns:
            List of semantic interpretations (deep structures)
        """
        # Step 0: Tokenize and clean if needed
        if isinstance(sentence, str):
            # Remove punctuation and convert to lowercase
            cleaned = ''.join(c.lower() for c in sentence if c.isalnum() or c.isspace())
            tokens = cleaned.split()
        else:
            # Clean individual tokens
            tokens = [''.join(c.lower() for c in t if c.isalnum()) for t in sentence]
            tokens = [t for t in tokens if t]  # Remove empty tokens
        
        print(f"\n{'='*60}")
        print(f"Analyzing: {sentence}")
        print(f"{'='*60}\n")
        
        # Step 1: Look up words and associate classes
        sentence_classes = {}
        for i, word in enumerate(tokens, 1):
            senses = self.lexicon.lookup(word)
            # If the word isn't in the lexicon, try simple normalization
            # (plural/tense stripping) before falling back to a generic sense.
            if not senses:
                tried = []
                # common surface forms -> base form candidates
                if word.endswith("'s"):
                    tried.append(word[:-2])
                if word.endswith('s') and len(word) > 3:
                    tried.append(word[:-1])
                if word.endswith('es') and len(word) > 4:
                    tried.append(word[:-2])
                if word.endswith('ed') and len(word) > 3:
                    tried.append(word[:-2])
                if word.endswith('ing') and len(word) > 4:
                    tried.append(word[:-3])
                if word.endswith('ly') and len(word) > 3:
                    # maybe an adverb; try removing ly to find an adjective/verb
                    tried.append(word[:-2])

                for cand in tried:
                    if not cand:
                        continue
                    cand = cand.lower()
                    senses = self.lexicon.lookup(cand)
                    if senses:
                        # prefer the candidate's senses but keep original token text
                        print(f"Auto-mapped '{word}' -> '{cand}' (heuristic)")
                        break

            # If still no senses, add a generic noun/object sense so analysis can continue
            if not senses:
                print(f"Unknown word '{word}': adding generic noun sense as fallback")
                senses = self.lexicon.add_generic_sense(word, persist=False)
            
            # Collect all syntactic and semantic classes
            classes = set()
            for sense in senses:
                classes.add(sense.syntactic_class)
                classes.update(sense.semantic_classes)
            
            sentence_classes[i] = {
                'word': word,
                'senses': senses,
                'classes': list(classes)
            }
            
        
        print("Word Classes:")
        for num, info in sentence_classes.items():
            print(f"  {num}. {info['word']}: {info['classes']}")
        print()
        
        # Step 2: Select relevant SEFs
        word_classes_only = {k: v['classes'] for k, v in sentence_classes.items()}
        relevant_sefs = self.sef_set.get_relevant_sefs(word_classes_only)
        
        print(f"Relevant SEFs ({len(relevant_sefs)}):")
        for sef in relevant_sefs:
            print(f"  {sef}")
        print()
        
        # Step 3: Create complex triples
        complex_triples = self.sef_set.create_complex_triples(relevant_sefs, sentence_classes)
        
        print(f"Complex Triples (before filtering): {len(complex_triples)}")
        for ct in complex_triples[:10]:  # Show first 10
            print(f"  {ct['sef']} -> {ct['positions']} -> {ct['words']}")
        if len(complex_triples) > 10:
            print(f"  ... and {len(complex_triples) - 10} more")
        print()
        
        # Step 4: Filter by ordering rules
        filtered_triples = self.sef_set.filter_by_order(complex_triples)
        
        print(f"After ordering filter: {len(filtered_triples)}")
        for ct in filtered_triples:
            print(f"  {ct['sef']} -> {ct['positions']} -> {ct['words']}")
        print()
        
        # Step 5: Eliminate abstract duplicates
        final_triples = self.sef_set.eliminate_abstract_duplicates(filtered_triples)
        
        print(f"Final Grammar ({len(final_triples)} triples):")
        for ct in final_triples:
            print(f"  {ct['sef']} -> {ct['positions']} -> {ct['words']}")
        print()
        
        # Step 6: Generate parse structures
        print("Attempting to generate structures...")
        interpretations = self.generate_structures(final_triples, sentence_classes)
        print(f"Generated {len(interpretations)} interpretation(s)\n")
        
        return interpretations
    
    def generate_structures(self, complex_triples, sentence_classes):
        """
        Generate all valid parse structures (Step 6 in paper)
        
        Simplified approach: Find the main verb triple, then recursively add modifiers
        """
        if not complex_triples:
            return []
        
        # Find main predication triples (those with verb relations)
        candidate_triples = []
        for ct in complex_triples:
            sef = ct['sef']
            # Consider triples with verb-like relations as candidates
            if sef.relation in ['V', 'HIT', 'CONSUME', 'MOVE', 'BE', 'EQUIV', 'DISCOVER', 'BOYCOTT', 'SIMILAR', 'RESEMBLE']:
                candidate_triples.append(ct)

        # Score candidate triples by how well they match available word senses
        # Prefer triples where the relation matches a verb sense and arguments match semantic classes
        main_triples = []
        if candidate_triples:
            scored = []
            for ct in candidate_triples:
                sef = ct['sef']
                left_num, rel_num, right_num = ct['positions']
                score = 0
                # Verb match (higher weight). Prefer matches to more specific (earlier) semantic classes
                if rel_num and rel_num in sentence_classes:
                    verb_word = sentence_classes[rel_num]['word']
                    verb_senses = sentence_classes[rel_num].get('senses', self.lexicon.lookup(verb_word))
                    for vs in verb_senses:
                        if sef.relation in vs.semantic_classes:
                            try:
                                idx = vs.semantic_classes.index(sef.relation)
                                score += 3 + max(0, 1 - idx)  # small boost for earlier (more specific) classes
                            except ValueError:
                                score += 3
                            break

                # Left/right argument semantic match
                if left_num and left_num in sentence_classes:
                    left_word_senses = sentence_classes[left_num].get('senses', self.lexicon.lookup(sentence_classes[left_num]['word']))
                    # Prefer matches to more specific semantic classes (earlier in list)
                    for ls in left_word_senses:
                        if ls.matches_class(sef.left):
                            try:
                                idx = ls.semantic_classes.index(sef.left)
                                score += 2 + max(0, 1 - idx)
                            except ValueError:
                                score += 2
                            break
                if right_num and right_num in sentence_classes:
                    right_word_senses = sentence_classes[right_num].get('senses', self.lexicon.lookup(sentence_classes[right_num]['word']))
                    for rs in right_word_senses:
                        if rs.matches_class(sef.right):
                            try:
                                idx = rs.semantic_classes.index(sef.right)
                                score += 2 + max(0, 1 - idx)
                            except ValueError:
                                score += 2
                            break

                scored.append((score, ct))

            # Keep only triples with the maximal score (and positive score if available)
            scored.sort(key=lambda x: x[0], reverse=True)
            if scored:
                max_score = scored[0][0]
                if max_score > 0:
                    candidates = [ct for sc, ct in scored if sc == max_score]
                    # Tie-breaker: prefer least abstract (most specific) SEFs
                    try:
                        min_abs = min(self.sef_set._abstraction_level(ct['sef']) for ct in candidates)
                        main_triples = [ct for ct in candidates if self.sef_set._abstraction_level(ct['sef']) == min_abs]
                    except Exception:
                        main_triples = candidates
                else:
                    # no good matches; fall back to all candidates
                    main_triples = candidate_triples[:]
        
        if not main_triples:
            # If no verb found, try any triple as starting point
            main_triples = complex_triples[:1]
        
        interpretations = []
        
        for main_triple in main_triples:
            # Build structure starting from main triple
            structure = self._build_structure_iterative(main_triple, complex_triples)

            # If structure covers all words, accept it; otherwise still record it
            # (more sophisticated merging/repair can be added later)
            try:
                complete = self._is_complete(structure, sentence_classes)
            except Exception:
                complete = False

            interpretations.append(structure)
        return interpretations
    
    def _build_structure_iterative(self, root_triple, all_triples, seen_positions=None):
        """
        Build structure iteratively by finding and attaching modifiers
        """
        if seen_positions is None:
            seen_positions = set()
        
        # Start with root
        structure = {
            'sef': root_triple['sef'],
            'positions': root_triple['positions'],
            'words': root_triple['words'],
            'left': None,
            'right': None
        }
        
        # Add current positions to seen set
        root_positions = tuple(p for p in root_triple['positions'] if p > 0)
        seen_positions.update(root_positions)
        
        root_left, root_rel, root_right = root_triple['positions']
        
        # Find all triples that modify the left element
        left_modifiers = []
        for ct in all_triples:
            if ct == root_triple:
                continue
                
            ct_positions = tuple(p for p in ct['positions'] if p > 0)
            if any(p in seen_positions for p in ct_positions):
                continue
                
            if ct['sef'].relation == 'MOD' and ct['positions'][0] == root_left:
                left_modifiers.append(ct)
        
        # Find all triples that modify the right element
        right_modifiers = []
        for ct in all_triples:
            if ct == root_triple:
                continue
                
            ct_positions = tuple(p for p in ct['positions'] if p > 0)
            if any(p in seen_positions for p in ct_positions):
                continue
                
            if ct['sef'].relation == 'MOD' and ct['positions'][0] == root_right:
                right_modifiers.append(ct)
        
        # Attach left modifiers (recursively)
        if left_modifiers:
            best_left = self._choose_best_modifier(left_modifiers)
            structure['left'] = self._build_structure_iterative(best_left, all_triples, seen_positions.copy())
        
        # Attach right modifiers (recursively)
        if right_modifiers:
            best_right = self._choose_best_modifier(right_modifiers)
            structure['right'] = self._build_structure_iterative(best_right, all_triples, seen_positions.copy())
        
        return structure
    
    def _choose_best_modifier(self, modifiers):
        """Choose the most specific (least abstract) modifier"""
        if len(modifiers) == 1:
            return modifiers[0]
        
        # Prefer semantic classes over syntactic
        best = modifiers[0]
        best_score = self.sef_set._abstraction_level(best['sef'])
        
        for mod in modifiers[1:]:
            score = self.sef_set._abstraction_level(mod['sef'])
            if score < best_score:
                best = mod
                best_score = score
        
        return best
    
    
    def _get_all_positions(self, structure):
        """Get all word positions used in a structure"""
        positions = set()
        if structure['positions'][0] != 0:
            positions.add(structure['positions'][0])
        if structure['positions'][1] != 0:
            positions.add(structure['positions'][1])
        if structure['positions'][2] != 0:
            positions.add(structure['positions'][2])
        
        if structure['left']:
            positions.update(self._get_all_positions(structure['left']))
        if structure['right']:
            positions.update(self._get_all_positions(structure['right']))
        
        return positions
    
    def _is_complete(self, structure, sentence_classes):
        """Check if structure accounts for all words"""
        used_positions = self._get_all_positions(structure)
        all_positions = set(sentence_classes.keys())
        return used_positions == all_positions
    
    def format_interpretation(self, interpretation, sentence_classes):
        """
        Format interpretation as nested triple structure
        Similar to the paper's output format
        """
        if not interpretation:
            return "NO INTERPRETATION"
        
        return self._format_structure(interpretation, sentence_classes)
    
    def _format_structure(self, struct, sentence_classes):
        """Recursively format structure"""
        if not struct:
            return ""
        
        left_num, rel_num, right_num = struct['positions']
        left_word, rel_word, right_word = struct['words']
        
        # Format left
        if struct['left']:
            left_str = self._format_structure(struct['left'], sentence_classes)
        else:
            left_str = left_word.upper()
        
        # Format right
        if struct['right']:
            right_str = self._format_structure(struct['right'], sentence_classes)
        else:
            right_str = right_word.upper()
        
        # Format relation
        rel_str = rel_word.upper()
        
        return f"({left_str} {rel_str} {right_str})"
    
    def select_word_senses(self, interpretation, sentence_classes):
        """Select word senses based on semantic restrictions"""
        if not interpretation or not sentence_classes:
            return None
            
        # Collect all SEFs used in the interpretation
        sefs_used = self._collect_sefs(interpretation)
        
        # Map word positions to selected senses
        sense_map = {}
        
        # For each word position
        for pos, info in sentence_classes.items():
            word = info['word']
            senses = info['senses']
            
            # Find SEFs that use this word position
            relevant_sefs = []
            for sef_struct in sefs_used:
                sef = sef_struct['sef']
                positions = sef_struct['positions']
                if pos in positions:
                    relevant_sefs.append((sef, positions))
            
            # Score each sense based on SEF matches
            best_sense = None
            best_score = -1
            
            for sense in senses:
                score = 0
                for sef, positions in relevant_sefs:
                    left_num, rel_num, right_num = positions
                    if pos == left_num and sense.matches_class(sef.left):
                        score += 1
                    elif pos == right_num and sense.matches_class(sef.right):
                        score += 1
                        
                if score > best_score:
                    best_score = score
                    best_sense = sense
            
            if best_sense:
                sense_map[pos] = best_sense
        
        # Create a new structure with selected senses
        return self._add_senses_to_structure(interpretation, sense_map)
        """
        Select specific word senses based on the interpretation
        Returns structure with sense identifiers
        """
        if not interpretation:
            return None
        
        # Get all SEFs used in interpretation
        sefs_used = self._collect_sefs(interpretation)
        
        # For each word position, select the sense that matches the SEFs
        sense_map = {}
        for num, info in sentence_classes.items():
            word = info['word']
            senses = info['senses']
            
            # Find which SEFs involve this word
            relevant_sefs = []
            for sef in sefs_used:
                # Check if this word participates in this SEF
                for sense in senses:
                    if sense.matches_class(sef.left) or sense.matches_class(sef.right):
                        relevant_sefs.append(sef)
                        break
            
            # Select the most specific sense that matches
            if senses:
                best_sense = senses[0]
                for sense in senses:
                    # Prefer senses with more specific semantic classes
                    if len(sense.semantic_classes) > len(best_sense.semantic_classes):
                        best_sense = sense
                
                sense_map[num] = best_sense
        
        # Rebuild interpretation with sense identifiers
        return self._add_senses_to_structure(interpretation, sense_map)
    
    def _collect_sefs(self, structure):
        """Collect all SEFs used in a structure"""
        sefs = [{
            'sef': structure['sef'],
            'positions': structure['positions']
        }]
        
        if structure['left']:
            sefs.extend(self._collect_sefs(structure['left']))
        if structure['right']:
            sefs.extend(self._collect_sefs(structure['right']))
            
        return sefs
    
    def _add_senses_to_structure(self, struct, sense_map):
        """Add sense identifiers to structure"""
        result = struct.copy()
        
        left_num = struct['positions'][0]
        right_num = struct['positions'][2]
        
        # Add sense info to words
        words = list(struct['words'])
        if left_num in sense_map:
            sense = sense_map[left_num]
            words[0] = f"{sense.word}_{sense.sense_num}"
        if right_num in sense_map:
            sense = sense_map[right_num]
            words[2] = f"{sense.word}_{sense.sense_num}"
        
        result['words_with_senses'] = tuple(words)
        
        if struct['left']:
            result['left'] = self._add_senses_to_structure(struct['left'], sense_map)
        if struct['right']:
            result['right'] = self._add_senses_to_structure(struct['right'], sense_map)
        
        return result
    
    def format_with_senses(self, interpretation):
        """Format interpretation showing word senses"""
        if not interpretation:
            return "NO INTERPRETATION"
        
        return self._format_with_senses_recursive(interpretation)
    
    def _format_with_senses_recursive(self, struct):
        """Recursively format with sense numbers"""
        if not struct:
            return ""
        
        # Store sentence classes for tree generation
        self._last_sentence_classes = {}
            
        # Use sense-annotated words if available
        if 'words_with_senses' in struct:
            left_word, rel_word, right_word = struct['words_with_senses']
        else:
            left_word, rel_word, right_word = struct['words']
        
        # Format left
        if struct['left']:
            left_str = self._format_with_senses_recursive(struct['left'])
        else:
            left_str = left_word.upper()
        
        # Format right
        if struct['right']:
            right_str = self._format_with_senses_recursive(struct['right'])
        else:
            right_str = right_word.upper()
        
        rel_str = rel_word.upper()
        
        return f"({left_str} {rel_str} {right_str})"
        
    def format_syntax_tree(self, interpretation, sentence_classes=None):
        """Generate and format a syntactic phrase structure tree."""
        if not interpretation or not sentence_classes:
            return "NO PARSE TREE"
        try:
            # Get sentence parts
            left_num, rel_num, right_num = interpretation['positions']
            left_word, rel_word, right_word = interpretation['words']
            
            # Basic tree structure
            tree = ["[S"]
            
            # Subject phrase
            tree.append("  [NP")
            subj_det = sentence_classes.get(left_num - 1, {})
            if subj_det and 'ART' in subj_det.get('classes', []):
                tree.append(f"    [DET {subj_det['word'].title()}]")
            subj_adj = sentence_classes.get(left_num - 1, {})
            if subj_adj and any(c in subj_adj.get('classes', []) for c in ['ADJ', 'EMOTION', 'SIZE']):
                tree.append(f"    [ADJ {subj_adj['word']}]")
            tree.append(f"    [N {left_word}]")
            tree.append("  ]")
            
            # Verb phrase
            tree.append("  [VP")
            tree.append(f"    [V {rel_word}]")
            
            # Check for PP
            prep_pos = None
            prep_word = None
            
            # Look for preposition between verb and object
            for pos in range(rel_num + 1, right_num):
                word_info = sentence_classes.get(pos, {})
                if 'PREP' in word_info.get('classes', []):
                    prep_pos = pos
                    prep_word = word_info['word']
                    break
            
            # Handle PP if found
            if prep_pos:
                tree.append("    [PP")
                tree.append(f"      [P {prep_word}]")
                tree.append("      [NP")
                
                # Object determiner
                obj_det = sentence_classes.get(right_num - 1, {})
                if obj_det and 'ART' in obj_det.get('classes', []):
                    tree.append(f"        [DET {obj_det['word'].title()}]")
                
                # Object adjective
                obj_adj = sentence_classes.get(right_num - 2, {})
                if obj_adj and any(c in obj_adj.get('classes', []) for c in ['ADJ', 'EMOTION', 'SIZE']):
                    tree.append(f"        [ADJ {obj_adj['word']}]")
                
                tree.append(f"        [N {right_word}]")
                tree.append("      ]")
                tree.append("    ]")
            else:
                # Direct object
                tree.append("    [NP")
                obj_det = sentence_classes.get(right_num - 1, {})
                if obj_det and 'ART' in obj_det.get('classes', []):
                    tree.append(f"      [DET {obj_det['word'].title()}]")
                obj_adj = sentence_classes.get(right_num - 2, {})
                if obj_adj and any(c in obj_adj.get('classes', []) for c in ['ADJ', 'EMOTION', 'SIZE']):
                    tree.append(f"      [ADJ {obj_adj['word']}]")
                tree.append(f"      [N {right_word}]")
                tree.append("    ]")
            
            tree.append("  ]")
            tree.append("]")
            
            return "\n".join(tree)
        except Exception as e:
            return f"ERROR: {str(e)}"
            return "NO PARSE TREE - Generation failed"
    
    def _format_tree_recursive(self, struct, level=0):
        """Format syntax tree recursively, adding phrase nodes with proper indentation."""
        if not struct:
            return ""

        indent = "  " * level
        
        # Get the SEF and word positions
        sef = struct.get('sef')
        positions = struct.get('positions', ())
        words = struct.get('words', ())
        
        if not positions or not words:
            return ""
            
        left_num, rel_num, right_num = positions
        left_word, rel_word, right_word = words
        
        # Get class information for all words
        rel_info = self._last_sentence_classes.get(rel_num, {})
        left_info = self._last_sentence_classes.get(left_num, {})
        right_info = self._last_sentence_classes.get(right_num, {})
        
        result = []
        
        # Determine if this is a sentence-level structure
        is_sentence = any('V' in self._last_sentence_classes.get(p, {}).get('classes', []) 
                         for p in range(1, max(positions)+1))
        
        # Add sentence node at top level only
        if level == 0 and is_sentence:
            result.append(f"[S")
            level += 1
            indent = "  " * level
            
        # Handle subject noun phrase
        if 'PERSON' in left_info.get('classes', []) or 'N' in left_info.get('classes', []):
            result.append(f"{indent}[NP")
            inner_indent = "  " * (level + 1)
            
            # Add determiner if present
            prev_word = self._last_sentence_classes.get(left_num - 1, {})
            if 'ART' in prev_word.get('classes', []):
                result.append(f"{inner_indent}[DET {prev_word['word']}]")
                
            # Add adjective if present
            if any(c in prev_word.get('classes', []) for c in ['ADJ', 'EMOTION', 'QUALITY', 'COLOR']):
                result.append(f"{inner_indent}[ADJ {prev_word['word']}]")
                
            result.append(f"{inner_indent}[N {left_word}]")
            result.append(f"{indent}]")
            
        # Handle verb phrase
        if 'V' in rel_info.get('classes', []):
            result.append(f"{indent}[VP")
            result.append(f"{indent}  [V {rel_word}]")
            
            # Handle object within VP if present
            if right_num > 0 and right_info:
                inner_indent = "  " * (level + 2)
                if any(c in right_info.get('classes', []) for c in ['N', 'OBJECT']):
                    result.append(f"{indent}  [NP")
                    
                    # Add determiner for object if present
                    prev_word = self._last_sentence_classes.get(right_num - 1, {})
                    if 'ART' in prev_word.get('classes', []):
                        result.append(f"{inner_indent}[DET {prev_word['word']}]")
                    
                    # Add adjective for object if present
                    if any(c in prev_word.get('classes', []) for c in ['ADJ', 'QUALITY', 'COLOR']):
                        result.append(f"{inner_indent}[ADJ {prev_word['word']}]")
                    
                    result.append(f"{inner_indent}[N {right_word}]")
                    result.append(f"{indent}  ]")
                    
            result.append(f"{indent}]")
            
        # Close sentence node if needed
        if level == 1 and is_sentence:
            result.append("]")
            
        return "\n".join(result) if result else ""
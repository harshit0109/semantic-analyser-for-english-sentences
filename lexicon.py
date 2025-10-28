"""
lexicon.py - Lexical Structure Implementation
Based on Simmons & Burger (1968) Section IV

Each word has multiple senses, each with:
- Syntactic class (N, V, ADJ, etc.)
- Syntactic features (SING, PL, PAST, etc.)
- Semantic classes (ordered by abstraction level)
"""

class WordSense:
    def __init__(self, word, sense_num, syntactic_class, features, semantic_classes):
        self.word = word
        self.sense_num = sense_num
        self.syntactic_class = syntactic_class
        self.features = features  # e.g., ['SING'], ['PL', 'PAST']
        self.semantic_classes = semantic_classes  # ordered by abstraction
        
    def __repr__(self):
        return f"{self.word}_{self.sense_num}({self.syntactic_class}, {self.semantic_classes})"
    
    def matches_class(self, word_class):
        """Check if this sense matches a syntactic or semantic class"""
        if word_class == self.syntactic_class:
            return True
        return word_class in self.semantic_classes

import os
import json


class Lexicon:
    def __init__(self):
        self.entries = {}  # word -> list of WordSense
        # path for custom additions
        self._custom_path = os.path.join(os.path.dirname(__file__), 'custom_lexicon.json')
        self._initialize_lexicon()
        # load any user-added entries
        self._load_custom_lexicon()
    
    def _initialize_lexicon(self):
        """Initialize with example vocabulary from the paper"""
        
        # Common verbs
        self.add_sense('read', 1, 'V', ['PRES'], ['COMMUNICATE', 'LEARN'])
        self.add_sense('reads', 1, 'V', ['PRES', 'SING'], ['COMMUNICATE', 'LEARN'])
        self.add_sense('teach', 1, 'V', ['PRES'], ['TEACH', 'COMMUNICATE'])
        self.add_sense('teaches', 1, 'V', ['PRES', 'SING'], ['TEACH', 'COMMUNICATE'])
        self.add_sense('walk', 1, 'V', ['PRES'], ['MOVE', 'TRAVEL'])
        self.add_sense('walks', 1, 'V', ['PRES', 'SING'], ['MOVE', 'TRAVEL'])
        self.add_sense('work', 1, 'V', ['PRES'], ['LABOR', 'DO'])
        self.add_sense('works', 1, 'V', ['PRES', 'SING'], ['LABOR', 'DO'])
        self.add_sense('study', 1, 'V', ['PRES'], ['LEARN', 'DO'])
        self.add_sense('studies', 1, 'V', ['PRES', 'SING'], ['LEARN', 'DO'])
        self.add_sense('move', 1, 'V', ['PRES'], ['MOVE'])
        self.add_sense('moves', 1, 'V', ['PRES', 'SING'], ['MOVE'])
        self.add_sense('is', 1, 'V', ['PRES', 'SING'], ['BE', 'EQUIV'])
        self.add_sense('are', 1, 'V', ['PRES', 'PL'], ['BE', 'EQUIV'])
        
        # Common nouns - People
        self.add_sense('pitcher', 1, 'N', ['SING'], ['PERSON', 'ATHLETE'])
        self.add_sense('pitcher', 2, 'N', ['SING'], ['CONTAINER', 'OBJECT'])
        self.add_sense('person', 1, 'N', ['SING'], ['PERSON'])
        self.add_sense('people', 1, 'N', ['PL'], ['PERSON'])
        self.add_sense('student', 1, 'N', ['SING'], ['PERSON', 'LEARNER'])
        self.add_sense('students', 1, 'N', ['PL'], ['PERSON', 'LEARNER'])
        self.add_sense('teacher', 1, 'N', ['SING'], ['PERSON', 'EDUCATOR'])
        self.add_sense('teachers', 1, 'N', ['PL'], ['PERSON', 'EDUCATOR'])
        self.add_sense('doctor', 1, 'N', ['SING'], ['PERSON', 'PROFESSIONAL'])
        self.add_sense('child', 1, 'N', ['SING'], ['PERSON', 'YOUNG'])
        self.add_sense('children', 1, 'N', ['PL'], ['PERSON', 'YOUNG'])
        self.add_sense('parent', 1, 'N', ['SING'], ['PERSON', 'FAMILY'])
        self.add_sense('parents', 1, 'N', ['PL'], ['PERSON', 'FAMILY'])
        self.add_sense('friend', 1, 'N', ['SING'], ['PERSON', 'RELATION'])
        self.add_sense('friends', 1, 'N', ['PL'], ['PERSON', 'RELATION'])
        
        self.add_sense('batter', 1, 'N', ['SING'], ['PERSON', 'ATHLETE'])
        self.add_sense('batter', 2, 'N', ['SING'], ['LIQUID', 'SUBSTANCE'])
        
        self.add_sense('umpire', 1, 'N', ['SING'], ['PERSON', 'OFFICIAL'])
        
        # Common nouns - Objects and Academic Subjects
        self.add_sense('book', 1, 'N', ['SING'], ['OBJECT', 'READABLE'])
        self.add_sense('books', 1, 'N', ['PL'], ['OBJECT', 'READABLE'])
        self.add_sense('table', 1, 'N', ['SING'], ['OBJECT', 'FURNITURE'])
        self.add_sense('chair', 1, 'N', ['SING'], ['OBJECT', 'FURNITURE'])
        self.add_sense('computer', 1, 'N', ['SING'], ['OBJECT', 'DEVICE'])
        self.add_sense('phone', 1, 'N', ['SING'], ['OBJECT', 'DEVICE'])
        self.add_sense('car', 1, 'N', ['SING'], ['OBJECT', 'VEHICLE'])
        self.add_sense('cars', 1, 'N', ['PL'], ['OBJECT', 'VEHICLE'])
        self.add_sense('mathematics', 1, 'N', ['SING'], ['SUBJECT', 'ACADEMIC'])
        self.add_sense('mathematics', 1, 'N', ['SING'], ['SUBJECT', 'READABLE'])
        
        # Common nouns - Places
        self.add_sense('house', 1, 'N', ['SING'], ['PLACE', 'BUILDING'])
        self.add_sense('school', 1, 'N', ['SING'], ['PLACE', 'BUILDING', 'EDUCATION'])
        self.add_sense('office', 1, 'N', ['SING'], ['PLACE', 'BUILDING', 'WORK'])
        self.add_sense('park', 1, 'N', ['SING'], ['PLACE', 'OUTDOOR', 'RECREATION'])
        self.add_sense('city', 1, 'N', ['SING'], ['PLACE', 'URBAN'])
        self.add_sense('country', 1, 'N', ['SING'], ['PLACE', 'NATION'])
        
        self.add_sense('condor', 1, 'N', ['SING'], ['BIRD', 'ANIMAL'])
        self.add_sense('landbird', 1, 'N', ['SING'], ['BIRD', 'ANIMAL'])
        self.add_sense('continent', 1, 'N', ['SING'], ['PLACE', 'LANDMASS'])
        
        self.add_sense('man', 1, 'N', ['SING'], ['PERSON', 'MALE', 'MAMMAL'])
        self.add_sense('men', 1, 'N', ['PL'], ['PERSON', 'MALE', 'MAMMAL'])
        
        self.add_sense('fish', 1, 'N', ['SING'], ['ANIMAL', 'AQUATIC'])
        self.add_sense('fish', 2, 'N', ['PL'], ['ANIMAL', 'AQUATIC'])
        self.add_sense('fish', 3, 'N', ['SING'], ['FOOD'])
        
        self.add_sense('time', 1, 'N', ['SING'], ['DURATION', 'CONCEPT'])
        self.add_sense('flies', 1, 'N', ['PL'], ['INSECT', 'ANIMAL'])
        self.add_sense('arrow', 1, 'N', ['SING'], ['WEAPON', 'OBJECT'])
        self.add_sense('arrows', 1, 'N', ['PL'], ['WEAPON', 'OBJECT'])
        
        # Verbs
        self.add_sense('strike', 1, 'V', ['PL', 'PAST'], ['DISCOVER', 'FIND'])
        self.add_sense('strike', 2, 'V', ['PL', 'PAST'], ['BOYCOTT', 'REFUSE'])
        self.add_sense('strike', 3, 'V', ['PL', 'PAST'], ['HIT', 'TOUCH'])
        
        self.add_sense('struck', 1, 'V', ['SING', 'PAST'], ['DISCOVER', 'FIND'])
        self.add_sense('struck', 2, 'V', ['SING', 'PAST'], ['BOYCOTT', 'REFUSE'])
        self.add_sense('struck', 3, 'V', ['SING', 'PAST'], ['HIT', 'TOUCH'])
        
        self.add_sense('eat', 1, 'V', ['PL', 'PR'], ['CONSUME', 'INGEST'])
        self.add_sense('ate', 1, 'V', ['SING', 'PAST'], ['CONSUME', 'INGEST'])
        
        self.add_sense('fly', 1, 'V', ['PL', 'PR'], ['MOVE', 'TRAVEL'])
        self.add_sense('flies', 2, 'V', ['SING', 'PR'], ['MOVE', 'TRAVEL'])
        
        self.add_sense('like', 1, 'V', ['PL', 'PR'], ['SIMILAR', 'RESEMBLE'])
        self.add_sense('like', 2, 'PREP', [], ['SIMILAR'])
        
        # Common verbs - Being
        self.add_sense('is', 1, 'V', ['SING', 'PR'], ['BE', 'EQUIV'])
        self.add_sense('are', 1, 'V', ['PL', 'PR'], ['BE', 'EQUIV'])
        self.add_sense('was', 1, 'V', ['SING', 'PAST'], ['BE', 'EQUIV'])
        self.add_sense('were', 1, 'V', ['PL', 'PAST'], ['BE', 'EQUIV'])
        
        # Common verbs - Action
        self.add_sense('read', 1, 'V', ['PL', 'PR'], ['CONSUME', 'LEARN'])
        self.add_sense('reads', 1, 'V', ['SING', 'PR'], ['CONSUME', 'LEARN'])
        self.add_sense('write', 1, 'V', ['PL', 'PR'], ['CREATE', 'COMMUNICATE'])
        self.add_sense('writes', 1, 'V', ['SING', 'PR'], ['CREATE', 'COMMUNICATE'])
        self.add_sense('study', 1, 'V', ['PL', 'PR'], ['LEARN', 'THINK'])
        self.add_sense('studies', 1, 'V', ['SING', 'PR'], ['LEARN', 'THINK'])
        self.add_sense('work', 1, 'V', ['PL', 'PR'], ['DO', 'LABOR'])
        self.add_sense('works', 1, 'V', ['SING', 'PR'], ['DO', 'LABOR'])
        self.add_sense('play', 1, 'V', ['PL', 'PR'], ['DO', 'ENJOY'])
        self.add_sense('plays', 1, 'V', ['SING', 'PR'], ['DO', 'ENJOY'])
        
        # Common verbs - Motion
        self.add_sense('go', 1, 'V', ['PL', 'PR'], ['MOVE', 'TRAVEL'])
        self.add_sense('goes', 1, 'V', ['SING', 'PR'], ['MOVE', 'TRAVEL'])
        self.add_sense('come', 1, 'V', ['PL', 'PR'], ['MOVE', 'ARRIVE'])
        self.add_sense('comes', 1, 'V', ['SING', 'PR'], ['MOVE', 'ARRIVE'])
        self.add_sense('walk', 1, 'V', ['PL', 'PR'], ['MOVE', 'SELF'])
        self.add_sense('walks', 1, 'V', ['SING', 'PR'], ['MOVE', 'SELF'])
        self.add_sense('run', 1, 'V', ['PL', 'PR'], ['MOVE', 'FAST'])
        self.add_sense('runs', 1, 'V', ['SING', 'PR'], ['MOVE', 'FAST'])
        
        # Adjectives - Emotions and Attitudes
        self.add_sense('angry', 1, 'ADJ', [], ['EMOTION', 'FEELING'])
        self.add_sense('happy', 1, 'ADJ', [], ['EMOTION', 'FEELING'])
        self.add_sense('sad', 1, 'ADJ', [], ['EMOTION', 'FEELING'])
        self.add_sense('excited', 1, 'ADJ', [], ['EMOTION', 'FEELING'])
        self.add_sense('careless', 1, 'ADJ', [], ['ATTITUDE', 'QUALITY'])
        self.add_sense('careful', 1, 'ADJ', [], ['ATTITUDE', 'QUALITY'])
        self.add_sense('smart', 1, 'ADJ', [], ['ATTITUDE', 'QUALITY'])
        self.add_sense('clever', 1, 'ADJ', [], ['ATTITUDE', 'QUALITY'])
        
        # Adjectives - Physical Qualities
        self.add_sense('old', 1, 'ADJ', [], ['AGE', 'QUALITY'])
        self.add_sense('young', 1, 'ADJ', [], ['AGE', 'QUALITY'])
        self.add_sense('new', 1, 'ADJ', [], ['AGE', 'QUALITY'])
        self.add_sense('big', 1, 'ADJ', [], ['SIZE', 'QUALITY'])
        self.add_sense('small', 1, 'ADJ', [], ['SIZE', 'QUALITY'])
        self.add_sense('tall', 1, 'ADJ', [], ['SIZE', 'QUALITY'])
        self.add_sense('short', 1, 'ADJ', [], ['SIZE', 'QUALITY'])
        self.add_sense('largest', 1, 'ADJ', [], ['SIZE', 'SUPERLATIVE'])
        self.add_sense('smallest', 1, 'ADJ', [], ['SIZE', 'SUPERLATIVE'])
        self.add_sense('beautiful', 1, 'ADJ', [], ['APPEARANCE', 'QUALITY'])
        
        # Adjectives - Colors
        self.add_sense('red', 1, 'ADJ', [], ['COLOR', 'QUALITY'])
        self.add_sense('blue', 1, 'ADJ', [], ['COLOR', 'QUALITY'])
        self.add_sense('green', 1, 'ADJ', [], ['COLOR', 'QUALITY'])
        self.add_sense('yellow', 1, 'ADJ', [], ['COLOR', 'QUALITY'])
        
        # Adverbs
        self.add_sense('very', 1, 'ADV', [], ['INTENSIFIER'])
        self.add_sense('really', 1, 'ADV', [], ['INTENSIFIER'])
        self.add_sense('quickly', 1, 'ADV', [], ['SPEED', 'MANNER', 'FAST'])
        self.add_sense('slowly', 1, 'ADV', [], ['SPEED', 'MANNER', 'SLOW'])
        self.add_sense('well', 1, 'ADV', [], ['QUALITY', 'MANNER', 'GOOD'])
        self.add_sense('badly', 1, 'ADV', [], ['QUALITY', 'MANNER', 'BAD'])
        
        # Articles and Determiners
        self.add_sense('the', 1, 'ART', ['DEF'], ['DEFINITE'])
        self.add_sense('a', 1, 'ART', ['INDEF'], ['INDEFINITE'])
        self.add_sense('an', 1, 'ART', ['INDEF'], ['INDEFINITE'])
        
        # Prepositions
        self.add_sense('of', 1, 'PREP', [], ['POSSESSION', 'RELATION'])
        self.add_sense('on', 1, 'PREP', [], ['LOCATION', 'POSITION'])
        self.add_sense('in', 1, 'PREP', [], ['LOCATION', 'POSITION'])
        self.add_sense('at', 1, 'PREP', [], ['LOCATION', 'POSITION'])
        self.add_sense('to', 1, 'PREP', [], ['DIRECTION', 'GOAL'])
        
        # Relative Pronouns
        self.add_sense('who', 1, 'R/P', [], ['PERSON'])
        self.add_sense('which', 1, 'R/P', [], ['THING'])
        self.add_sense('that', 1, 'R/P', [], ['ANY'])
        
        # Proper nouns
        self.add_sense('California', 1, 'N', ['SING', 'PROPER'], ['PLACE', 'STATE'])
        self.add_sense('North', 1, 'ADJ', [], ['DIRECTION'])
        self.add_sense('America', 1, 'N', ['SING', 'PROPER'], ['PLACE', 'CONTINENT'])
        
        # Verb "called" for passive constructions
        self.add_sense('called', 1, 'V', ['SING', 'PAST'], ['NAME', 'DESIGNATE'])
        
        # Personal pronouns
        self.add_sense('she', 1, 'PRO', ['SING', 'FEM'], ['PERSON'])
        self.add_sense('he', 1, 'PRO', ['SING', 'MASC'], ['PERSON'])
        self.add_sense('i', 1, 'PRO', ['SING'], ['PERSON'])
        self.add_sense('you', 1, 'PRO', [], ['PERSON'])
        self.add_sense('we', 1, 'PRO', ['PL'], ['PERSON'])
        self.add_sense('they', 1, 'PRO', ['PL'], ['PERSON'])

        # Common auxiliaries and small verbs
        self.add_sense('am', 1, 'V', ['SING', 'PR'], ['BE', 'EQUIV'])
        self.add_sense('have', 1, 'V', ['PR'], ['HAVE'])
        self.add_sense('has', 1, 'V', ['SING', 'PR'], ['HAVE'])
        self.add_sense('do', 1, 'V', ['PR'], ['DO'])
        self.add_sense('does', 1, 'V', ['SING', 'PR'], ['DO'])

        # Simple conversational words
        self.add_sense('hello', 1, 'N', [], ['OBJECT'])
        self.add_sense('world', 1, 'N', [], ['PLACE', 'OBJECT'])

        # Additional adjectives and modifiers
        self.add_sense('beautiful', 1, 'ADJ', [], ['APPEARANCE', 'QUALITY', 'POSITIVE'])
    
    def add_sense(self, word, sense_num, syn_class, features, sem_classes):
        """Add a word sense to the lexicon"""
        word_lower = word.lower()
        sense = WordSense(word_lower, sense_num, syn_class, features, sem_classes)
        
        if word_lower not in self.entries:
            self.entries[word_lower] = []
        self.entries[word_lower].append(sense)

    def add_generic_sense(self, word, persist=False):
        """Add a generic noun sense for an unknown word.

        This provides a graceful fallback for interactive input so the analyzer
        can continue. If persist=True the entry is saved to
        `custom_lexicon.json` next to the lexicon module.
        """
        w = word.lower()
        senses = self.entries.get(w, [])
        sense_num = len(senses) + 1
        # default to noun/object sense
        self.add_sense(w, sense_num, 'N', [], ['OBJECT'])
        if persist:
            self._save_custom_entry(w, sense_num, 'N', [], ['OBJECT'])
        return self.entries.get(w, [])

    def _load_custom_lexicon(self):
        """Load custom lexicon additions from a JSON file if present."""
        try:
            if os.path.exists(self._custom_path):
                with open(self._custom_path, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
                for word, senses in data.items():
                    for s in senses:
                        # s expected to be dict with keys: sense_num, syn_class, features, sem_classes
                        self.add_sense(word, s.get('sense_num', 1), s.get('syn_class', 'N'), s.get('features', []), s.get('sem_classes', ['OBJECT']))
        except Exception:
            # ignore errors loading custom lexicon so analysis still works
            pass

    def _save_custom_entry(self, word, sense_num, syn_class, features, sem_classes):
        """Append a custom sense to the JSON file (creates file if necessary)."""
        try:
            data = {}
            if os.path.exists(self._custom_path):
                with open(self._custom_path, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
            if word not in data:
                data[word] = []
            data[word].append({
                'sense_num': sense_num,
                'syn_class': syn_class,
                'features': features,
                'sem_classes': sem_classes
            })
            with open(self._custom_path, 'w', encoding='utf-8') as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def lookup(self, word):
        """Get all senses for a word"""
        return self.entries.get(word.lower(), [])
    
    def get_classes_for_word(self, word):
        """Get all syntactic and semantic classes for a word"""
        senses = self.lookup(word)
        classes = set()
        for sense in senses:
            classes.add(sense.syntactic_class)
            classes.update(sense.semantic_classes)
        return list(classes)
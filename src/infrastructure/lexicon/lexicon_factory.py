
from src.domain.services.presentation import LexiconBase

from .randomized_dict_lexicon import RandomizedDictLexicon
from .dicts import fq, fq_variants, friendship, keyboards, menu


def create_lexicon() -> LexiconBase:
    return RandomizedDictLexicon(dicts=(fq.lexicon,
                                        fq_variants.lexicon,
                                        friendship.lexicon,
                                        keyboards.lexicon,
                                        menu.lexicon))

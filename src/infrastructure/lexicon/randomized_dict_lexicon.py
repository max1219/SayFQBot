import random
from collections.abc import Mapping, Sequence
from typing import Optional

from src.domain.services.presentation import LexiconBase


class RandomizedDictLexicon(LexiconBase):
    def __init__(self, dicts: Mapping[str, str | Sequence[str]] | Sequence[Mapping[str, str | Sequence[str]]]):
        if isinstance(dicts, Mapping):
            self._dicts = [dicts]
        else:
            self._dicts = dicts

    def get_or_none(self, key: str) -> Optional[str]:
        for d in self._dicts:
            if key in d:
                if isinstance(d[key], str):
                    return d[key]
                return d[key][random.randint(0, len(d[key]) - 1)]
        return None

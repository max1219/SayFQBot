from typing import Sequence, Optional

from src.domain.services.presentation import LexiconBase

class ProxyLexicon(LexiconBase):
    def __init__(self, lexicons: Sequence[LexiconBase]):
        self._lexicons = lexicons

    def get_or_none(self, key: str) -> Optional[str]:
        for l in self._lexicons:
            value = l.get_or_none(key)
            if value is not None:
                return value
        return None


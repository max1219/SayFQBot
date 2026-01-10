from abc import ABC, abstractmethod
from typing import Optional


class LexiconBase(ABC):
    def get(self, key: str) -> str:
        value = self.get_or_none(key)
        if value is None:
            raise KeyError(f"Key {key} not found in lexicon")
        return value

    @abstractmethod
    def get_or_none(self, key: str) -> Optional[str]:
        pass

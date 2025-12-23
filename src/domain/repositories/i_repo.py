import asyncio

from abc import ABC, abstractmethod


class IRepo(ABC):
    @abstractmethod
    def get_lock(self) -> asyncio.Lock:
        pass
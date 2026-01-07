from enum import Enum


class TransactionType(Enum):
    Deferred = 0,  # Никаких ограничений до первой записи (потом переходит в другой режим)
    Immediate = 1,  # Не позволяет записывать другим сразу
    Exclusive = 2   # Не позволяет другим и читать
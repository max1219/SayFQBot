from typing import Sequence

class IsAdminService:
    def __init__(self, admin_ids: Sequence[int]):
        self._admin_ids = admin_ids

    def check(self, user_id: int) -> bool:
        return user_id in self._admin_ids
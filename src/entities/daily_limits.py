from dataclasses import dataclass

@dataclass(slots=True)
class DailyLimits:
    user_id: int
    friendship_requests: int
    fqs: int
    fqs_all: int
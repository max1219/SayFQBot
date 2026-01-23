from enum import Enum

class ResponseFqStatus(Enum):
    Success = 0,
    NotFriend = 1,
    CannotSendMessage = 2,
    UserNotFound = 3,
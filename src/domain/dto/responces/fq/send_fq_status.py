from enum import Enum

class SendFqStatus(Enum):
    Success = 0,
    NotFriend = 1,
    CannotSendMessage = 2,
    TotalLimitExceeded = 3,
    ToThisFriendLimitExceeded = 4,
    UserNotFound = 5,
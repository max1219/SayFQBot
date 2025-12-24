from enum import Enum

class RequestFriendshipStatus(Enum):
    Success = 0,
    AlreadyRequested = 1,
    AlreadyFriend = 2,
    AutoAccepted = 3,
    UserNotFound = 4,
    CannotSendMessage = 5,
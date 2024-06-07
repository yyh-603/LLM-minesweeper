from enum import Enum

class ActionFeedback(Enum):
    SUCCESS = 0
    FORMAT_ERROR = 1
    INVALID_CELL = 2
    OPEN_NUMBER_CELL = 3
    OPEN_FLAGGED_CELL = 4
    FLAG_NUMBER_CELL = 5
    GAME_HAS_ENDED = 6
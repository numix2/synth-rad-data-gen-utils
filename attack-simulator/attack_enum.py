"""
This enum denotes the possible attack types.
"""
from enum import Enum, auto

class Attack(Enum):
    INSERT_ONE_EVENT = auto()
    MODIFY_X_TO_EVENT = auto()
    MODIFY_X_TO_ZERO = auto()
    MODIFY_X_TO_MEAN = auto()
    MODIFY_WITH_OWN_PATTERN = auto()
    MODIFY_WITH_PAST_PATTERN = auto()
    MODIFY_WITH_GENERATED = auto()

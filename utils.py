from enum import Enum


class State(Enum):
    SHORT = -1
    NONE = 0
    LONG = 1

class Action(Enum):
    SHORT = -1
    NONE = 0
    LONG = 1
    SQUARE_OFF = 2


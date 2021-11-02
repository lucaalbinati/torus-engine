from enum import Enum, auto

class Status(Enum):
    STOP = auto()
    PAUSE = auto()
    RUN = auto()

    def pressed_pause(self):
        if self == Status.RUN:
            return Status.PAUSE
        elif self == Status.PAUSE:
            return Status.RUN
        else:
            return self
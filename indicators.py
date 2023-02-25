from utils import State, Action


class EMA:
    value_went_above_ema_actions = {
        State.SHORT: Action.SQUARE_OFF,
        State.LONG: Action.NONE,
        State.NONE: Action.LONG
    }
    value_went_below_ema_actions = {
        State.SHORT: Action.NONE,
        State.LONG: Action.SQUARE_OFF,
        State.NONE: Action.NONE
    }

    def __init__(self, period, ema_init=0) -> None:
        self.period = period
        self.alpha = 2 / (period + 1)
        self.ema = ema_init


    def update(self, value):
        self.ema = (value * self.alpha) + (self.ema * (1 - self.alpha))


    def indicate(self, value, state: State):
        if self.ema > value:
            return self.value_went_below_ema_actions[state]
        elif self.ema < value:
            return self.value_went_above_ema_actions[state]
        else:
            return Action.NONE

    
    def __call__(self, value, state: State):
        self.update(value)
        return self.indicate(value, state)
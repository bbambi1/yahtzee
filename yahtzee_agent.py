import utils

class YahtzeeAgent:
    """General agent interface for the Yahtzee game."""

    def __init__(self):
        self.scorecard = utils.BLANK_SCORECARD
        self.opponent_scorecard = utils.BLANK_SCORECARD

    def roll_dice(self, dice_values, nrolls)->list:
        """Returns a list of booleans indicating which dice to re-roll."""
        raise NotImplementedError

    def choose_decision(self, dice_values)->str:
        """Returns a decision from utils.ALL_DECISIONS."""
        raise NotImplementedError

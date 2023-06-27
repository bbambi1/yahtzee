from collections import Counter
import utils
from yahtzee_agent import YahtzeeAgent


class BasicAgent(YahtzeeAgent):
    """Agent that applies a basic strategy."""

    def __init__(self, name="Bienvenu_basic"):
        super().__init__(name)
        self.name = name

    def roll_dice(self, dice_values, nrolls)->list:
        if nrolls == 0:
            return [False]*5  # Don't re-roll on the last roll

        dice_values_sorted = sorted(dice_values)

        # Check for potential large straight
        if dice_values_sorted in [[1,2,3,4],[2,3,4,5],[3,4,5,6]]:
            return [dice not in dice_values_sorted for dice in dice_values]

        # Check for potential four-of-a-kind or Yahtzee
        dice_counts = Counter(dice_values)
        for dice, count in dice_counts.items():
            if count >= 3:
                return [dice != v for v in dice_values]

        # If none of the above, keep high numbers and re-roll low numbers
        return [dice < 4 for dice in dice_values]

    def choose_decision(self, dice_values)->str:
        """
        For the decision, we should choose the category that maximizes our score based on the current dice.
        """
        max_score = -1
        best_decision = None

        # Iterate over all possible decisions
        for decision in utils.ALL_DECISIONS:
            if self.scorecard[decision] is not None:
                continue  # Skip filled decisions

            # Compute potential score
            score = utils.compute_score(dice_values, decision)
            if score > max_score:
                max_score = score
                best_decision = decision

        return best_decision

import utils
from yahtzee_agent import YahtzeeAgent
import itertools
import numpy as np

class Yah(YahtzeeAgent):
    all_rolls = list(itertools.product(*[[False, True]]*utils.N_DICE))

    def __init__(self, name='yah'):
        super().__init__(name)

    def roll_dice(self, dice_values, nrolls)->list:
        return max(Yah.all_rolls, key = lambda roll: self.mean_score(dice_values, roll, nrolls))

    def choose_decision(self, dice_values)->str:
        return self.best_decscore(dice_values)[0]
    
    def mean_score(self, dice_values, rolls, nrolls):
        fixed_dice = [dice_values[i] for i, r in enumerate(rolls) if not r]
        rerolls = [range(1, utils.N_FACES + 1)]*(utils.N_DICE - len(fixed_dice))
        scores = [
            self.best_decscore(fixed_dice + list(rolled_dice))[1]
            for rolled_dice in itertools.product(*rerolls)
        ]
        return np.average(scores)

    def best_decscore(self, dice_values):
        dec_scores = [
            (dec, utils.compute_score(dice_values, dec, False))
            for dec in utils.ALL_DECISIONS
            if utils.is_valid_decision(dec, self.scorecard, False, dice_values)
        ]
        return max(dec_scores, key = lambda x : x[1])

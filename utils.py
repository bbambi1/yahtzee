from math import *
from random import *

# Basic parameters for Yahtzee
N_DICE = 5
N_FACES = 6

# Possible decisions
UPPER_SECTION = {'Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes'}
LOWER_SECTION = {'3_of_a_Kind', '4_of_a_Kind', 'Full_House', 'Small_Straight', 'Large_Straight', 'Yahtzee', 'Chance'}
ALL_DECISIONS = set().union(UPPER_SECTION, LOWER_SECTION)
N_TURNS = len(UPPER_SECTION) + len(LOWER_SECTION)
BLANK_SCORECARD = {'Ones': None, 'Twos': None, 'Threes': None, 'Fours': None,
                   'Fives': None, 'Sixes': None, '3_of_a_Kind': None,
                   '4_of_a_Kind': None, 'Full_House': None,
                   'Small_Straight': None, 'Large_Straight': None, 'Yahtzee': None,
                   'Chance': None, 'Yahtzee_Bonus': 0}
NUM_TO_LETTER = {1: 'Ones', 2: 'Twos', 3: 'Threes', 4: 'Fours', 5: 'Fives', 6: 'Sixes'}
LETTER_TO_NUM = {'Ones': 1, 'Twos': 2, 'Threes': 3, 'Fours': 4, 'Fives': 5, 'Sixes': 6}

# Scoring values
UPPER_BONUS_THRESHOLD = 63
UPPER_BONUS_VALUE = 35
FULL_HOUSE_VALUE = 25
SMALL_STRAIGHT_VALUE = 30
LARGE_STRAIGHT_VALUE = 40
YAHTZEE_VALUE = 50
YAHTZEE_BONUS_VALUE = 100

def is_valid_decision(decision, scorecard, is_yahtzee_bonus=False, dice_values=None):
    """Determines if a decision satisfies the rules of the game."""

    # If the scorecard already has a value for the decision and this is not a bonus Yahtzee, the decision is invalid.
    if scorecard[decision] is not None and not is_yahtzee_bonus:
        return False

    # If this is a bonus Yahtzee,
    if is_yahtzee_bonus:
        # And the number on the dice corresponds to an empty box in the upper section,
        corresponding_number = NUM_TO_LETTER[dice_values[0]]
        if scorecard[corresponding_number] is None:
            # Then the decision is valid if it corresponds to the number on the dice.
            return decision == corresponding_number

        # If the corresponding box in the upper section is filled,
        else:
            # And there's an empty box in the lower section,
            if any(scorecard[dec] is None for dec in LOWER_SECTION):
                # Then the decision is valid if it's in the lower section.
                return decision in LOWER_SECTION

            # If there are no empty boxes in the lower section,
            else:
                # Then the decision is valid if it's in the upper section.
                return decision in UPPER_SECTION

    # If this is not a bonus Yahtzee, the decision is valid as long as the scorecard doesn't already have a value for it.
    else:
        return scorecard[decision] is None

def compute_score(dice_values, decision, is_yahtzee_bonus=False):
    """Computes the score obtained at the end of a turn given a particular decision."""
    occurrences = [0 for _ in range(N_FACES)]
    for dice in range(N_DICE):
        occurrences[dice_values[dice] - 1] += 1
    if decision in UPPER_SECTION:
        num = LETTER_TO_NUM[decision]
        return occurrences[num - 1] * num
    else:
        total_dice = sum(dice_values)
        if decision == '3_of_a_Kind':
            return (max(occurrences) >= 3) * total_dice
        elif decision == '4_of_a_Kind':
            return (max(occurrences) >= 4) * total_dice
        elif decision == 'Full_House':
            return ((any([occurrences[j] == 3 for j in range(6)])
                    and any([occurrences[j] == 2 for j in range(6)]))
                    or is_yahtzee_bonus) * FULL_HOUSE_VALUE
        elif decision == 'Small_Straight':
            return (all([occurrences[j] > 0 for j in range(0, 4)])
                    or all([occurrences[j] > 0 for j in range(1, 5)])
                    or all([occurrences[j] > 0 for j in range(2, 6)])
                    or is_yahtzee_bonus) * SMALL_STRAIGHT_VALUE
        elif decision == 'Large_Straight':
            return (all([occurrences[j] > 0 for j in range(0, 5)])
                    or all([occurrences[j] > 0 for j in range(1, 6)])
                    or is_yahtzee_bonus) * LARGE_STRAIGHT_VALUE
        elif decision == 'Yahtzee':
            return (max(occurrences) >= 5) * YAHTZEE_VALUE
        else:
            return total_dice

def totalScore(scorecard):
    upper_section_sum = sum([scorecard[box] for box in UPPER_SECTION])
    if upper_section_sum >= UPPER_BONUS_THRESHOLD:
        upper_section_sum += UPPER_BONUS_VALUE
    lower_section_sum = sum([scorecard[box] for box in LOWER_SECTION])
    return upper_section_sum + lower_section_sum + scorecard['Yahtzee_Bonus']

def random_dice_to_roll()->list:
    """Arbitrarily choose the dice to be re-rolled"""
    return [2 * random() > 1 for _ in range(N_DICE)]

def arbitraty_decision(dice_values, scorecard)->str:
    """Returns an arbitrary, but still valid decision."""
    if scorecard['Yahtzee'] is None or any([dice_values[dice] != dice_values[0] for dice in range(1, N_DICE)]):
        possible_decisions = set()
        for decision in ALL_DECISIONS:
            if scorecard[decision] is None:
                possible_decisions.add(decision)
        return list(possible_decisions)[floor(len(possible_decisions) * random())]
    else:
        chiffre = NUM_TO_LETTER[dice_values[0]]
        if scorecard[chiffre] is None:
            return chiffre
        else:
            possible_decisions = set()
            for decision in LOWER_SECTION:
                if scorecard[decision] is None:
                    possible_decisions.add(decision)
            if len(possible_decisions) > 0:
                return list(possible_decisions)[floor(len(possible_decisions) * random())]
            else:
                possible_decisions = set()
                for decision in UPPER_SECTION:
                    if scorecard[decision] is None:
                        possible_decisions.add(decision)
                return list(possible_decisions)[floor(len(possible_decisions) * random())]

def random_decision()->str:
    """Returns a random decision"""
    return list(ALL_DECISIONS)[floor(len(ALL_DECISIONS) * random())]

class Penalty(Exception):
    def __init__(self, penalty_type):
        super().__init__(penalty_type)
        self.penalty_type = penalty_type

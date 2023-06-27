import utils
from yahtzee_agent import YahtzeeAgent

ALL_DECISIONS_LIST = ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', '3_of_a_Kind', '4_of_a_Kind', 'Full_House', 'Small_Straight', 'Large_Straight', 'Yahtzee', 'Chance']
VALUES = range(1, utils.N_FACES + 1)
PROBABILITIES = {
    "1_of_a_Kind": {
        "FirstRoll": [0.95, 1.0, 1.0, 1.0, 1.0, 1.0], 
        "SecondRoll": [0.9, 1.0, 1.0, 1.0, 1.0, 1.0]
    },
    "2_of_a_Kind": {
        "FirstRoll": [0.4, 0.9, 1.0, 1.0, 1.0, 1.0], 
        "SecondRoll": [0.2, 0.7, 1.0, 1.0, 1.0, 1.0]
    },
    "3_of_a_Kind": {
        "FirstRoll": [0.2, 0.4, 0.9, 1.0, 1.0, 1.0], 
        "SecondRoll": [0.05, 0.15, 0.6, 1.0, 1.0, 1.0]
    },
    "4_of_a_Kind": {
        "FirstRoll": [0.05, 0.2, 0.35, 0.7, 1.0, 1.0], 
        "SecondRoll": [0.0, 0.05, 0.1, 0.4, 1.0, 1.0]
    },
    "5_of_a_Kind": {
        "FirstRoll": [0.0, 0.0, 0.1, 0.2, 0.4, 1.0], 
        "SecondRoll": [0.0, 0.0, 0.05, 0.1, 0.2, 1.0]
    },
    "Full_House": {
        "FirstRoll": [0.2, 0.3, 0.4, 0.6, 0.7, 1.0], 
        "SecondRoll": [0.1, 0.2, 0.25, 0.3, 0.4, 1.0]
    }, 
    "Small_Straight": {
        "FirstRoll": [0.3, 0.5, 0.7, 0.9, 1.0, 1.0], 
        "SecondRoll": [0.05, 0.1, 0.3, 0.7, 1.0, 1.0]
    }, 
    "Large_Straight": {
        "FirstRoll": [0.05, 0.1, 0.2, 0.4, 0.6, 1.0], 
        "SecondRoll": [0.0, 0.02, 0.05, 0.15, 0.3, 1.0]
    }
}
NROLLS_TO_ROLL = ["", "SecondRoll", "FirstRoll"]
STRAIGHTS = ['Small_Straight', 'Large_Straight']

def dice_to_roll(decision, dice_values, nrolls):
    decision_index = ALL_DECISIONS_LIST.index(decision)
    if decision_index == 0: #Ones
        return roll_except_values(dice_values, [1])
    elif decision_index == 1: #Twos
        return roll_except_values(dice_values, [2])
    elif decision_index == 2: #Threes
        return roll_except_values(dice_values, [3])
    elif decision_index == 3: #Fours
        return roll_except_values(dice_values, [4])
    elif decision_index == 4: #Fives
        return roll_except_values(dice_values, [5])
    elif decision_index == 5: #Sixes
        return roll_except_values(dice_values, [6])
    elif decision_index == 6: #3_of_a_Kind
        return roll_except_values(dice_values, [best_value_for_X_of_a_Kind(dice_values, nrolls)])
    elif decision_index == 7: #4_of_a_Kind
        return roll_except_values(dice_values, [best_value_for_X_of_a_Kind(dice_values, nrolls)])
    elif decision_index == 8: #Full_House
        return roll_except_values_full_house(dice_values)
    elif decision_index == 9: #Small_Straight
        return roll_except_values_unique(dice_values, best_values_for_straight(dice_values, "small"))
    elif decision_index == 10: #Large_Straight
        return roll_except_values_unique(dice_values, best_values_for_straight(dice_values, "large"))
    elif decision_index == 11: #Yahtzee
        return roll_except_values(dice_values, best_values_for_Yahtzee(dice_values))
    elif decision_index == 12: #Chance
        return roll_except_values(dice_values, [4, 5, 6])
    else:
        return utils.random_dice_to_roll()
    
def nb_dice_to_roll(decision, dice_values, nrolls):
    return sum(dice_to_roll(decision, dice_values, nrolls))

def nb_dice_fixed(decision, dice_values, nrolls):
    return utils.N_DICE - nb_dice_to_roll(decision, dice_values, nrolls)
        
def roll_except_values(dice_values, except_values):
    return [dice_values[i] not in except_values for i in range(utils.N_DICE)]

def roll_except_values_unique(dice_values, except_values):
    roll_values = []
    for i in range(utils.N_DICE):
        value = dice_values[i]
        if value in except_values:
            roll_values.append(False)
            except_values.remove(value)
        else:
            roll_values.append(True)
    return roll_values

def roll_except_values_full_house(dice_values):
    roll_values = []
    visited_values = dict.fromkeys(VALUES, 0)
    for i in range(utils.N_DICE):
        value = dice_values[i]
        count_value = dice_values.count(value)
        if count_value < 2: roll_values.append(True)
        elif count_value < 4: roll_values.append(False)
        else: roll_values.append(visited_values[value] >= 3)
        visited_values[value] += 1
    return roll_values

def best_value_for_X_of_a_Kind(dice_values, nrolls):
    max_most_rolled = max(most_rolled_values(dice_values))
    if nrolls == 2:
        return max_most_rolled if max_most_rolled >= 4 else highest_value_rolled(dice_values)
    else:
        return max_most_rolled
    
def best_values_for_Yahtzee(dice_values):
    max_most_rolled = max(most_rolled_values(dice_values))
    return [max_most_rolled] if (dice_values.count(max_most_rolled) > 1) else []

def best_values_for_straight(dice_values, size):
    mandatory_values = {3, 4} if size == "small" else {2, 3, 4, 5}
    return longest_straight(dice_values, mandatory_values) if all(v in dice_values for v in mandatory_values) else mandatory_values

def highest_value_rolled(dice_values):
    return max(dice_values)

def most_rolled_values(dice_values):
    max_count = max(dice_values.count(v) for v in VALUES)
    return {v for v in VALUES if dice_values.count(v) == max_count}

def most_X_of_a_Kind(dice_values): 
    return dice_values.count(max(most_rolled_values(dice_values)))

def longest_straight(dice_values, mandatory_values = []):
    longest_straight = mandatory_values
    current_chain = []
    for v in VALUES:
        if v in dice_values: 
            current_chain.append(v)
        else: 
            if (len(longest_straight) < len(current_chain)): longest_straight = current_chain
            current_chain = []
    if (len(longest_straight) < len(current_chain)): longest_straight = current_chain
    return longest_straight

def count_high_values(dice_values):
    return len(list(filter(lambda v: v in [4, 5, 6], dice_values)))

def compute_decision_factor(influences):
    return sum(influences[i]["weight"] * influences[i]["value"] for i in influences) / sum(influences[i]["weight"] for i in influences)

def score_normalized(score):
    return score / utils.YAHTZEE_VALUE

def probability_for_decision(tentative, decision, dice_values, nrolls):
    return PROBABILITIES[tentative][NROLLS_TO_ROLL[nrolls]][nb_dice_fixed(decision, dice_values, nrolls)]


class LucasTheBestAgent(YahtzeeAgent):
    current_decision = None
    decision_factors = dict.fromkeys(utils.ALL_DECISIONS, 0.)

    def __init__(self, name):
        super().__init__(name)
        self.strategy = 'maxpoints'
        self.verbosity = 0
        self.print("\n################# New Game ######################")

    def print(self, text):
        if self.verbosity >= 2: print(text)

    def str_decision_factors(self, dice_values, nrolls):
        if self.verbosity < 2: return ""
        elif self.verbosity == 2: return str(sorted(self.decision_factors.items()))
        else: return str(sorted(self.detailed_decision_factors(dice_values, nrolls).items()))

    def has_bonus(self):
        upper_section_sum = sum([self.scorecard[box] for box in utils.UPPER_SECTION])
        return upper_section_sum >= utils.UPPER_BONUS_THRESHOLD

    def roll_dice(self, dice_values, nrolls)->list[bool]:
        if nrolls == 2: 
            self.print("\n### Round " + str(self.get_round()) + " (" + self.strategy + ")" + " ###")

        self.print("Current dice values: " + str(dice_values))
        self.update_current_decision(dice_values, nrolls)
        self.print("Trying to fill: " + self.current_decision + " (" + self.str_decision_factors(dice_values, nrolls) + ")")
        dices = dice_to_roll(self.current_decision, dice_values, nrolls)
        self.print("Rolling dices: " + str(dices))
        return dices

    def choose_decision(self, dice_values)->str:
        self.print("Current dice values: " + str(dice_values))
        self.update_current_decision(dice_values, 0)
        self.print("Filling finally: " + self.current_decision + " (" + self.str_decision_factors(dice_values, 0) + ")")
        if not utils.is_valid_decision(self.current_decision, self.scorecard, False, dice_values): return utils.arbitraty_decision(dice_values, self.scorecard)
        else: return self.current_decision

    def get_round(self):
        return self.get_nb_rounds() - self.get_nb_rounds_remaining() + 1
    
    def get_nb_rounds_remaining(self):
        return len(self.valid_decisions())
    
    def get_nb_rounds(self):
        return len(self.scorecard) - 1
    
    def get_nb_upper_remaining(self):
        return len(list(filter(lambda d: self.is_decision_valid(d) and d in utils.UPPER_SECTION, self.scorecard)))
    
    def get_nb_lower_remaining(self):
        return len(list(filter(lambda d: self.is_decision_valid(d) and d in utils.LOWER_SECTION, self.scorecard)))
    
    def get_nb_straights_remaining(self):
        return len(list(filter(lambda d: self.is_decision_valid(d) and d in STRAIGHTS, self.scorecard)))

    def update_current_decision(self, dice_values, nrolls):
        for decision in ALL_DECISIONS_LIST:
            self.update_decision_factor_2(decision, dice_values, nrolls)

        max_decision_factor = max(self.decision_factors.values())
        if max_decision_factor < 0.2: 
            free_decision_gen = (decision for decision in self.free_decisions() if decision == '' or self.is_decision_valid(decision))
            next_free_decision = next(free_decision_gen)
            if next_free_decision != '':
                self.current_decision = next_free_decision
                return
        self.current_decision = next(decision for (decision, factor) in self.decision_factors.items() if factor == max_decision_factor)

    def current_score(self, decision, dice_values):
        return utils.compute_score(dice_values, decision)
    
    def minimum_possible_score(self, dice_values):
        return min([self.current_score(decision, dice_values) for decision in utils.ALL_DECISIONS])
    
    def current_score_penalized(self, decision, dice_values, nrolls):
        if self.expected_score(decision, dice_values, nrolls) > self.current_score(decision, dice_values):
            return self.minimum_possible_score(dice_values)
        return self.current_score(decision, dice_values)

    def expected_total_score(self, decision, dice_values, nrolls):
        return self.expected_score(decision, dice_values, nrolls) + self.expected_bonus(decision, dice_values)
    
    def expected_score(self, decision, dice_values, nrolls):
        decision_index = ALL_DECISIONS_LIST.index(decision)
        if decision_index <= 5:
            return 3 * (decision_index + 1)
        elif decision_index == 6: #3_of_a_Kind
            return 3 * best_value_for_X_of_a_Kind(dice_values, nrolls) + 6
        elif decision_index == 7: #4_of_a_Kind
            return 4 * best_value_for_X_of_a_Kind(dice_values, nrolls) + 3
        elif decision_index == 8: #Full_House
            return utils.FULL_HOUSE_VALUE
        elif decision_index == 9: #Small_Straight
            return utils.SMALL_STRAIGHT_VALUE
        elif decision_index == 10: #Large_Straight
            return utils.LARGE_STRAIGHT_VALUE
        elif decision_index == 11: #Yahtzee
            return utils.YAHTZEE_VALUE
        elif decision_index == 12: #Chance
            return 20
        else:
            return 0
        
    def minimum_acceptable_score(self, decision):
        decision_index = ALL_DECISIONS_LIST.index(decision)
        if decision_index <= 5:
            return 3 * (decision_index + 1) - max(0, self.current_upper_bonus_advance())
        elif decision_index == 6: #3_of_a_Kind
            return 12
        elif decision_index == 7: #4_of_a_Kind
            return 12
        elif decision_index == 8: #Full_House
            return utils.FULL_HOUSE_VALUE
        elif decision_index == 9: #Small_Straight
            return utils.SMALL_STRAIGHT_VALUE
        elif decision_index == 10: #Large_Straight
            return utils.LARGE_STRAIGHT_VALUE
        elif decision_index == 11: #Yahtzee
            return utils.YAHTZEE_VALUE
        elif decision_index == 12: #Chance
            return 15
        else:
            return 0

    def expected_bonus(self, decision, dice_values):
        return self.expected_upper_bonus(decision, dice_values)
    
    def expected_upper_bonus(self, decision, dice_values):
        upper_section_sum = sum([self.scorecard[box] for box in utils.UPPER_SECTION])
        if (decision in utils.UPPER_SECTION): upper_section_sum += self.expected_score(decision, dice_values)
        return utils.UPPER_BONUS_VALUE if upper_section_sum >= utils.UPPER_BONUS_THRESHOLD else 0

    # def update_decision_factor(self, decision, dice_values, nrolls):
    #     decision_index = ALL_DECISIONS_LIST.index(decision)
    #     if decision_index == 0: #Ones
    #         factor = 0.2 * dice_values.count(1)
    #     elif decision_index == 1: #Twos
    #         factor = 0.2 * dice_values.count(2)
    #     elif decision_index == 2: #Threes
    #         factor = 0.2 * dice_values.count(3)
    #     elif decision_index == 3: #Fours
    #         factor = 0.2 * dice_values.count(4)
    #     elif decision_index == 4: #Fives
    #         factor = 0.2 * dice_values.count(5)
    #     elif decision_index == 5: #Sixes
    #         factor = 0.2 * dice_values.count(6)
    #     elif decision_index == 6: #3_of_a_Kind
    #         factor = 0.2 * most_X_of_a_Kind(dice_values)
    #     elif decision_index == 7: #4_of_a_Kind
    #         factor = 0.2 * most_X_of_a_Kind(dice_values)
    #     elif decision_index == 8: #Full_House
    #         factor = 0
    #     elif decision_index == 9: #Small_Straight
    #         factor = 0.2 * len(longest_straight(dice_values))
    #     elif decision_index == 10: #Large_Straight
    #         factor = 0.2 * len(longest_straight(dice_values))
    #     elif decision_index == 11: #Yahtzee
    #         factor = 0.2 * most_X_of_a_Kind(dice_values)
    #     elif decision_index == 12: #Chance
    #         factor = 0.2 * count_high_values(dice_values)
    #     else:
    #         factor = 0

    #     self.decision_factors[decision] = self.zero_if_invalid(decision_index, factor)

    def update_decision_factor_2(self, decision, dice_values, nrolls):
        decision_index = ALL_DECISIONS_LIST.index(decision)
        influences = self.compute_influences(decision, dice_values, nrolls)
        factor = compute_decision_factor(influences)
        self.decision_factors[decision] = self.zero_if_invalid(decision_index, factor)

    def compute_influences(self, decision, dice_values, nrolls):
        return {
            "proba": {
                "weight": 0.3,
                "value": self.evaluate_probability(decision, dice_values, nrolls)
            }, 
            "ptsSucc": {
                "weight": 0.2,
                "value": score_normalized(self.expected_score(decision, dice_values, nrolls))
            }, 
            "ptsFail": {
                "weight": 0.3,
                "value": score_normalized(self.current_score_penalized(decision, dice_values, nrolls))
            }, 
            "opponent": {
                "weight": 0.2,
                "value": 0
            }, 
            "progress": {
                "weight": 0.2,
                "value": round(self.evaluate_progression(decision, dice_values, nrolls), 3)
            }
        }
    
    def evaluate_progression(self, decision, dice_values, nrolls):
        decision_index = ALL_DECISIONS_LIST.index(decision)
        if decision_index <= 5:
            return self.stress_factor_upper_bonus(decision, dice_values, nrolls)
        elif decision_index == 9 or decision_index == 10:
            return self.stress_factor_straights()
        else:
            return 0

    def detailed_decision_factors(self, dice_values, nrolls):
        ddf = {}
        for d in utils.ALL_DECISIONS:
            decision_index = ALL_DECISIONS_LIST.index(d)
            influences = self.compute_influences(d, dice_values, nrolls)
            ddf[d] = [float("{:.2f}".format(self.zero_if_invalid(decision_index, compute_decision_factor(influences)))), {i: influences[i]["value"] for i in influences}]
        return ddf

    def evaluate_probability(self, decision, dice_values, nrolls):
        if (nrolls == 0): return self.current_score(decision, dice_values) >= self.minimum_acceptable_score(decision)

        decision_index = ALL_DECISIONS_LIST.index(decision)
        if decision_index <= 5:
            return probability_for_decision("3_of_a_Kind", decision, dice_values, nrolls)
        elif decision_index == 6: #3_of_a_Kind
            return probability_for_decision("3_of_a_Kind", decision, dice_values, nrolls)
        elif decision_index == 7: #4_of_a_Kind
            return probability_for_decision("4_of_a_Kind", decision, dice_values, nrolls)
        elif decision_index == 8: #Full_House
            return probability_for_decision("Full_House", decision, dice_values, nrolls)
        elif decision_index == 9: #Small_Straight
            return probability_for_decision("Small_Straight", decision, dice_values, nrolls)
        elif decision_index == 10: #Large_Straight
            return probability_for_decision("Large_Straight", decision, dice_values, nrolls)
        elif decision_index == 11: #Yahtzee
            return probability_for_decision("5_of_a_Kind", decision, dice_values, nrolls)
        elif decision_index == 12: #Chance
            return 0
        else:
            return 0.0
    
    def current_upper_bonus_advance(self):        
        return sum(self.scorecard[d] - 3 * utils.LETTER_TO_NUM[d] if self.scorecard[d] is not None else 0 for d in utils.UPPER_SECTION)
    
    def upper_bonus_advance_with_decision(self, decision, dice_values):
        return self.current_score(decision, dice_values) - 3 * utils.LETTER_TO_NUM[decision]

    def stress_factor_upper_bonus(self, decision, dice_values, nrolls):
        # if self.current_upper_bonus_advance() + self.upper_bonus_advance_with_decision(decision, dice_values) > 0:
        #     return 0
        
        if nrolls == 0 and self.expected_score(decision, dice_values, nrolls) > self.current_score(decision, dice_values):
            return 0
        
        #return 0 (abandonner) si bonus impossible

        stress_factor_rounds = 1 - ((self.get_nb_rounds_remaining() - self.get_nb_upper_remaining()) / (self.get_nb_rounds() - len(utils.UPPER_SECTION)))
        min_stress_factor = 0.5
        return stress_factor_rounds * (1 - min_stress_factor) + min_stress_factor
    
    def stress_factor_straights(self):
        stress_factor = 1 - ((self.get_nb_rounds_remaining() - self.get_nb_straights_remaining()) / (self.get_nb_rounds() - len(STRAIGHTS)))
        min_stress_factor = 0
        max_stress_factor = 0.5
        return stress_factor * (1 - max_stress_factor) + min_stress_factor

    def zero_if_invalid(self, decision_index, factor):
        return factor if self.is_decision_valid(ALL_DECISIONS_LIST[decision_index]) else 0
    
    def reset_decision_factors(self):
        self.decision_factors = dict.fromkeys(self.decision_factors, 0.)
        
    def is_decision_valid(self, decision):
        return self.scorecard[decision] is None
    
    def valid_decisions(self):
        return list(filter(lambda x: self.is_decision_valid(x), self.scorecard))
    
    def free_decisions(self):
        return ['Chance', 'Ones', 'Yahtzee', '']






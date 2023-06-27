from itertools import combinations
import utils
from yahtzee_agent import YahtzeeAgent

class Victor(YahtzeeAgent):
    """Agent that plays randomly."""

    def __init__(self, name = "Victor", sacrifices = None):
        super().__init__(name)
        self.ALL_DICE_ROLLS = self.compute_all_dice_rolls()
        self.UPPER_SECTION = {'Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes'}
        self.LOWER_SECTION = {'Full_House', 'Small_Straight', 'Large_Straight', 'Yahtzee'}
        self.CHANCES = {'4_of_a_Kind', '3_of_a_Kind', 'Chance'}
        self.SACRIFICES = ['Chance', 'Yahtzee', 'Ones', 'Twos', '4_of_a_Kind', '3_of_a_Kind', 'Threes', 'Fours', 'Fives', 'Sixes', 'Full_House', 'Small_Straight', 'Large_Straight']
        
        if sacrifices == None:
            sacrifices = range(len(self.SACRIFICES))
        self.sacrifices_order = sacrifices

    def compute_all_dice_rolls(self):
        dice_values = []
        for i in range(6):
            cbs = combinations(range(5), i)
            for cb in cbs:
                dice_value = [0, 0, 0, 0, 0]
                for x in cb:
                    dice_value[x] = 1
                dice_values.append(dice_value)
        return dice_values

    def roll_dice(self, dice_values, nrolls)->list:
        occurences = [(sum(v == dice for v in dice_values), dice) for dice in range(1, 7)]
        occurences.sort(reverse=True)
        if occurences[0][0] == 5:
            return [0 for i in range(5)]
            
        if occurences[0][0] == 4:
            if utils.is_valid_decision("Yahtzee", self.scorecard) or occurences[1][1] <= 3:
                return [dice_values[i] == occurences[1][1] for i in range(5)]
            return [0, 0, 0, 0, 0]
            
        if occurences[0][0] == 3:
            if occurences[1][0] == 2:
                if utils.is_valid_decision("Full_House", self.scorecard):
                    return [0 for i in range(5)]
                
            # sinon on pourrait faire autre chose
            return [dice_values[i] != occurences[0][1] for i in range(5)]
                
        if occurences[0][0] == 2:
            if occurences[1][0] == 1:
                if utils.is_valid_decision("Large_Straight", self.scorecard) or utils.is_valid_decision("Small_Straight", self.scorecard):
                    if not 1 in dice_values and not 6 in dice_values:
                        for d in range(5):
                            if dice_values[d] == occurences[0][1]:
                                return [i == d for i in range(5)]
                    
                    if utils.is_valid_decision("Small_Straight", self.scorecard):
                        if max(v for v in dice_values) - min(v for v in dice_values) == 4:
                            for d in range(5):
                                if dice_values[d] == occurences[0][1]:
                                    return [i == d for i in range(5)]
                    #gère mal les suites en soi
                    #for d in range(5):
                     #   if dice_values[d] == occurences[0][1]:
                      #      return [i == d for i in range(5)]
                
            for o in occurences:
                if utils.is_valid_decision(utils.NUM_TO_LETTER[o[1]], self.scorecard):
                    return [dice_values[i] != o[1] for i in range(5)]
                    
            return [dice_values[i] != occurences[0][1] for i in range(5)]
            
        if utils.is_valid_decision("Large_Straight", self.scorecard) or utils.is_valid_decision("Small_Straight", self.scorecard):
            if 1 in dice_values and 6 in dice_values:
                missing = occurences[5][1]
                if missing == 2:
                    return [dice_values[i] == 1 for i in range(5)]
                if missing == 5:
                    return [dice_values[i] == 6 for i in range(5)]
                
                """
                if utils.is_valid_decision("Small_Straight", self.scorecard):
                    if missing == 3:
                        return [dice_values[i] == 1 or dice_values[i] == 2 for i in range(5)]
                    if missing == 4:
                        return [dice_values[i] == 6 or dice_values[i] == 5 for i in range(5)]
                """       
                return [dice_values[i] == 1 for i in range(5)]
            return [0, 0, 0, 0, 0]
        
        for o in occurences:
            if utils.is_valid_decision(utils.NUM_TO_LETTER[o[1]], self.scorecard):
                return [dice_values[i] != o[1] for i in range(5)]
                
        return [0, 1, 1, 1, 1]

    def choose_decision(self, dice_values)->str:
        bestLowerScore = -1
        bestLowerDecision = None
        for decision in self.LOWER_SECTION:
            if utils.is_valid_decision(decision, self.scorecard):
                score = utils.compute_score(dice_values, decision)
                if score > bestLowerScore:
                    bestLowerScore = score
                    bestLowerDecision = decision
                    
        if bestLowerScore > 0:
            return bestLowerDecision
            
        occurences = [(sum(v == dice for v in dice_values), dice) for dice in range(1, 7)]
        occurences.sort(reverse=True)
        if occurences[0][0] >= 4 and occurences[0][1] >= 4 and utils.is_valid_decision('4_of_a_Kind', self.scorecard):
            return '4_of_a_Kind'
            
        currentTardiness = sum(i * 3 - self.scorecard[utils.NUM_TO_LETTER[i]] if self.scorecard[utils.NUM_TO_LETTER[i]] != None else 0 for i in range(1, 7))
        retrievable = sum(i if self.scorecard[utils.NUM_TO_LETTER[i]] == None else 0 for i in range(1, 7))
        bestTardiness = 10000
        bestUpperDecision = None
        for decision in self.UPPER_SECTION:
            if utils.is_valid_decision(decision, self.scorecard):
                x = utils.LETTER_TO_NUM[decision]
                n = sum(x if v == x else 0 for v in dice_values)
                tardiness = currentTardiness + x * 3 - n
                if tardiness < bestTardiness:
                    bestTardiness = tardiness
                    bestUpperDecision = decision
        
        #print("Current tardiness = " + str(currentTardiness) + ", Retrievable = " + str(retrievable) + ", Best tardiness = " + str(bestTardiness))

        if bestTardiness <= 0:
            return bestUpperDecision
            
        bestChanceScore = -1
        bestChanceDecision = None
        for decision in self.CHANCES:
            if utils.is_valid_decision(decision, self.scorecard):
                score = utils.compute_score(dice_values, decision)
                if score > bestChanceScore:
                    bestChanceScore = score
                    bestChanceDecision = decision
                    
        if bestChanceScore > 0:
            return bestChanceDecision
        
        if bestTardiness <= 6 and bestTardiness - retrievable <= 0:
            return bestUpperDecision
            
        for i in self.sacrifices_order:
            decision = self.SACRIFICES[i]
            if utils.is_valid_decision(decision, self.scorecard):
                return decision
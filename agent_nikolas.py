import yahtzee_agent
import localsolver.modeler

def list_available_squares(scorecard):
    squares = []
    for s in scorecard:
        if scorecard[s] is None:
            squares.append(s)
    return squares

class AgentNikolas(yahtzee_agent.YahtzeeAgent):

    def __init__(self, name):
        super().__init__(name)

    def roll_dice(self, dice_values, nrolls)->list[bool]:
        perm = sorted(range(len(dice_values)), key=lambda k: dice_values[k])
        inverse_perm = [ None for _ in range(len(perm)) ]
        for i in range(len(perm)):
            inverse_perm[perm[i]] = i
        saved_dice = list(dice_values)
        dice_values = sorted(dice_values)
        available_squares = list_available_squares(self.scorecard)
        with localsolver.modeler.LSPModeler() as modeler:
            module = modeler.load_module("nikolas.lsp")
            dice_string = ",".join([str(d) for d in dice_values])
            squares_string = ",".join(available_squares)
            module.run_main("reroll", dice_string, squares_string)
            rerolls = list(module["reroll"])
            rerolls = [ rerolls[inverse_perm[i]] for i in range(5) ]
            return [ r[1] == 1 for r in rerolls ]

    def choose_decision(self, dice_values) -> str:
        dice_values = sorted(dice_values)
        available_squares = list_available_squares(self.scorecard)
        with localsolver.modeler.LSPModeler() as modeler:
            module = modeler.load_module("nikolas.lsp")
            dice_string = ",".join([str(d) for d in dice_values])
            squares_string = ",".join(available_squares)
            module.run_main("decision", dice_string, squares_string)
            decision = module["decision"]
            return decision
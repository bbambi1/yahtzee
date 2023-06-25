import csv
import utils
import yahtzee_agent as yAgent
import yahtzee_game as yGame

class Tournament:
    """Class to manage a tournament of multiple games of Yahtzee."""

    def __init__(self, agent1: yAgent.YahtzeeAgent, agent2: yAgent.YahtzeeAgent, n_games):
        self.agents = [agent1, agent2]
        self.n_games = n_games

    def run_games(self, file_name:str):
        """Runs the tournament and populates the results."""
        results = []

        for i in range(self.n_games):
            game = yGame.Game(self.agents[0], self.agents[1])
            try:
                game.play()
                winner = game.get_winner()
                if winner:
                    results.append({
                        "agent1": self.agents[0].name,
                        "agent2": self.agents[1].name,
                        "game_number": i + 1,
                        "score_agent1": utils.totalScore(self.agents[0].scorecard),
                        "score_agent2": utils.totalScore(self.agents[1].scorecard),
                        "penalty": "No",
                        "winner": winner.name
                    })
                else:
                    results.append({
                        "agent1": self.agents[0].name,
                        "agent2": self.agents[1].name,
                        "game_number": i + 1,
                        "score_agent1": utils.totalScore(self.agents[0].scorecard),
                        "score_agent2": utils.totalScore(self.agents[1].scorecard),
                        "penalty": "No",
                        "winner": "Draw"
                    })
            except utils.Penalty as e:
                winner = (game.current_agent_index + 1) % 2
                results.append({
                    "agent1": self.agents[0].name,
                    "agent2": self.agents[1].name,
                    "game_number": i + 1,
                    "score_agent1": utils.totalScore(self.agents[0].scorecard),
                    "score_agent2": utils.totalScore(self.agents[1].scorecard),
                    "penalty": e.penalty_type,
                    "winner": self.agents[winner].name
                })

        # Writing results to csv
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ["agent1", "agent2", "game_number", "score_agent1", "score_agent2", "penalty", "winner"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
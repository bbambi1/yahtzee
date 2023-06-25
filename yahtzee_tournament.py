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
        wins_agent1 = 0
        wins_agent2 = 0
        total_score_agent1 = 0
        total_score_agent2 = 0
        draws = 0

        for i in range(self.n_games):
            game = yGame.Game(self.agents[0], self.agents[1])
            try:
                game.play()
                winner = game.get_winner()
                score_agent1 = utils.totalScore(self.agents[0].scorecard)
                score_agent2 = utils.totalScore(self.agents[1].scorecard)
                total_score_agent1 += score_agent1
                total_score_agent2 += score_agent2
                
                if winner:
                    results.append({
                        "agent1": self.agents[0].name,
                        "agent2": self.agents[1].name,
                        "game_number": i + 1,
                        "score_agent1": score_agent1,
                        "score_agent2": score_agent2,
                        "penalty": "No",
                        "winner": winner.name
                    })
                    if winner == self.agents[0]:
                        wins_agent1 += 1
                    else:
                        wins_agent2 += 1
                else:
                    draws += 1
                    results.append({
                        "agent1": self.agents[0].name,
                        "agent2": self.agents[1].name,
                        "game_number": i + 1,
                        "score_agent1": score_agent1,
                        "score_agent2": score_agent2,
                        "penalty": "No",
                        "winner": "Draw"
                    })
            except utils.Penalty as e:
                winner = (game.current_agent_index + 1) % 2
                if winner == 0:
                    wins_agent1 += 1
                else:
                    wins_agent2 += 1
                results.append({
                    "agent1": self.agents[0].name,
                    "agent2": self.agents[1].name,
                    "game_number": i + 1,
                    "score_agent1": score_agent1,
                    "score_agent2": score_agent2,
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

        # Compute averages, win rates, and draw rate
        avg_score_agent1 = round(total_score_agent1 / self.n_games)
        avg_score_agent2 = round(total_score_agent2 / self.n_games)
        win_rate_agent1 = round((wins_agent1 / self.n_games) * 100, 2)  # Percentage with 2 decimal places
        win_rate_agent2 = round((wins_agent2 / self.n_games) * 100, 2)  # Percentage with 2 decimal places
        draw_rate = round((draws / self.n_games) * 100, 2)  # Percentage with 2 decimal places

        # Determine the ultimate winner
        if wins_agent1 > wins_agent2:
            ultimate_winner = self.agents[0].name
        elif wins_agent2 > wins_agent1:
            ultimate_winner = self.agents[1].name
        else:
            ultimate_winner = "It's a Draw"

        # Print the statistics
        print(f"Win rate of {self.agents[0].name}: {win_rate_agent1}%")
        print(f"Win rate of {self.agents[1].name}: {win_rate_agent2}%")
        print(f"Draw rate: {draw_rate}%")
        print(f"Mean score of {self.agents[0].name}: {avg_score_agent1}")
        print(f"Mean score of {self.agents[1].name}: {avg_score_agent2}")
        print(f"Ultimate winner of the tournament: {ultimate_winner}")

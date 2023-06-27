import csv
import utils
import yahtzee_agent as yAgent
import yahtzee_game as yGame

class Tournament:
    """Class to manage a tournament of multiple games of Yahtzee."""

    def __init__(self, agents: list[yAgent.YahtzeeAgent], n_games):
        self.agents = agents
        self.n_games = n_games
        self.results = []
        self.stats = {agent.name: {'wins': 0, 'total_score': 0, 'draws': 0, 'games_played': 0} for agent in agents}

    def run_games(self, file_name="tournament_results.csv"):
        """Runs the tournament and populates the results."""
        for i in range(len(self.agents)):
            for j in range(i + 1, len(self.agents)):
                wins_agent1 = 0
                wins_agent2 = 0
                total_score_agent1 = 0
                total_score_agent2 = 0
                draws = 0
                for _ in range(self.n_games):
                    game = yGame.Game(self.agents[i], self.agents[j])
                    try:
                        game.play()
                        winner = game.get_winner()
                        score_agent1 = utils.totalScore(self.agents[i].scorecard)
                        score_agent2 = utils.totalScore(self.agents[j].scorecard)
                        total_score_agent1 += score_agent1
                        total_score_agent2 += score_agent2

                        if winner:
                            self.results.append({
                                "agent1": self.agents[i].name,
                                "agent2": self.agents[j].name,
                                "game_number": i + 1,
                                "score_agent1": score_agent1,
                                "score_agent2": score_agent2,
                                "penalty": "No",
                                "winner": winner.name
                            })
                            if winner == self.agents[i]:
                                wins_agent1 += 1
                            else:
                                wins_agent2 += 1
                        else:
                            draws += 1
                            self.results.append({
                                "agent1": self.agents[i].name,
                                "agent2": self.agents[j].name,
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
                        self.results.append({
                            "agent1": self.agents[i].name,
                            "agent2": self.agents[j].name,
                            "game_number": i + 1,
                            "score_agent1": score_agent1,
                            "score_agent2": score_agent2,
                            "penalty": e.penalty_type,
                            "winner": self.agents[winner].name
                        })

                    # Update stats
                    score_agent1 = utils.totalScore(self.agents[i].scorecard)
                    score_agent2 = utils.totalScore(self.agents[j].scorecard)
                    self.stats[self.agents[i].name]['total_score'] += score_agent1
                    self.stats[self.agents[j].name]['total_score'] += score_agent2
                    self.stats[self.agents[i].name]['games_played'] += 1
                    self.stats[self.agents[j].name]['games_played'] += 1

                    winner = game.get_winner()
                    if winner == self.agents[i]:
                        self.stats[self.agents[i].name]['wins'] += 1
                    elif winner == self.agents[j]:
                        self.stats[self.agents[j].name]['wins'] += 1
                    else:
                        self.stats[self.agents[i].name]['draws'] += 1
                        self.stats[self.agents[j].name]['draws'] += 1

        # After all games, compute average scores and win rates for each agent
        for agent_name, data in self.stats.items():
            data['avg_score'] = round(data['total_score'] / data['games_played'])
            data['win_rate'] = round((data['wins'] / data['games_played']) * 100, 2)
            data['draw_rate'] = round((data['draws'] / data['games_played']) * 100, 2)

        # Write results to CSV
        self.write_to_csv(file_name)

        # Print the statistics
        self.print_statistics()

        # Calculate and print the rankings
        self.calculate_rankings()

    def write_to_csv(self, file_name):
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ["agent1", "agent2", "game_number", "score_agent1", "score_agent2", "penalty", "winner"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.results:
                writer.writerow(row)

    def print_statistics(self):
        for agent_name, data in self.stats.items():
            print(f"Statistics for {agent_name}:")
            print(f"\tWin rate: {data['win_rate']}%")
            print(f"\tMean score: {data['avg_score']}")
            print(f"\tDraw rate: {data['draw_rate']}%\n")

    def calculate_rankings(self):
        """Calculates the rankings of the agents based on their scores."""
        rankings = []
        for agent in self.agents:
            victories = sum(1 for result in self.results if result['winner'] == agent.name)
            total_points = 0
            for result in self.results:
                if result["agent1"] == agent.name:
                    total_points += result["score_agent1"]
                elif result["agent2"] == agent.name:
                    total_points += result["score_agent2"]
            opponents_beaten = len(set(result['agent1'] if result['agent2'] == agent.name else result['agent2'] for result in self.results if result['winner'] == agent.name))

            rankings.append({
                'agent': agent.name,
                'victories': victories,
                'total_points': total_points,
                'opponents_beaten': opponents_beaten
            })

        # Sort based on the criteria: number of opponents beaten, number of victories, total points
        rankings.sort(key=lambda x: (-x['opponents_beaten'], -x['victories'], -x['total_points']))

        # Print the rankings
        for i, ranking in enumerate(rankings, start=1):
            print(f"{i}. {ranking['agent']} - Opponents beaten: {ranking['opponents_beaten']}, Victories: {ranking['victories']}, Total Points: {ranking['total_points']}")
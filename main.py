import random_agent
from yahtzee_tournament import Tournament

def main():

    # Create the agents
    agent1 = random_agent.RandomAgent("random1")
    agent2 = random_agent.RandomAgent("random2")

    # Create the tournament
    tournament = Tournament(agent1, agent2, n_games=100)

    # Run the tournament
    tournament.run_games(file_name="game_results.csv")
    return

if __name__ == '__main__':
    main()
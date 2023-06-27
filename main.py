from agent_nikolas import AgentNikolas
from bienvenu_basic_agent import BasicAgent
from lucas_the_best_agent import LucasTheBestAgent
import random_agent
from ulysse import Yah
from victor import Victor
from yahtzee_tournament import Tournament

def main():
    # Create the agents
    agent_random = random_agent.RandomAgent("Random")
    agent_bienvenu = BasicAgent("Bienvenu")
    agent_lucas = LucasTheBestAgent("Lucas")
    agent_nikolas = AgentNikolas("Nikolas")
    agent_victor = Victor("Victor")
    agent_ulysse = Yah("Ulysse")
    agents = [agent_random, agent_bienvenu, agent_lucas, agent_nikolas, agent_victor, agent_ulysse]

    # Create the tournament
    tournament = Tournament(agents, n_games=100)

    # Run the tournament
    tournament.run_games()

if __name__ == '__main__':
    main()
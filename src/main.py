from games.game_simulator import GameSimulator
from games.stac.simulator import StacSimulator

"""
IMPORT PLAYERS
"""
from games.stac.players.human import HumanStacPlayer
from games.stac.players.random import RandomStacPlayer
from games.stac.players.montecarlo import MonteCarloStacPlayer


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print(f"Results for the game:")
    simulator.print_stats()


def main():
    print("ESTG IA Games Simulator")

    num_iterations = 1
    display_game = True

    sim = {
        "name": "Stac - HUMAN VS ROBO",
        "player1": HumanStacPlayer("HUMAN"),
        "player2": MonteCarloStacPlayer("ROBO")
    }

    run_simulation(sim["name"], StacSimulator(sim["player1"], sim["player2"], display_game), num_iterations)


if __name__ == "__main__":
    main()

from games.game_simulator import GameSimulator
from games.stac.players.human import HumanStacPlayer
from games.stac.simulator import StacSimulator
"""
IMPORT PLAYERS
"""
from games.stac.players.human import HumanStacPlayer


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

    sim ={
            "name": "Stac - TESTE VS TESTE",
            "player1": HumanStacPlayer("TESTE1"),
            "player2": HumanStacPlayer("TESTE2")
        }

    run_simulation(sim["name"], StacSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()

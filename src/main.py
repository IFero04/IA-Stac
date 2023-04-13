from game.game_simulator import GameSimulator
from game.stac.simulator import StacSimulator
from game.stac.state import StacState


def run_simulation(desc: str, simulator: GameSimulator, iterations: int, board_dimension: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print(f"Results for the game (Dimension = {board_dimension}):")
    simulator.print_stats()


def main():
    print("ESTG IA Games Simulator")

    num_iterations = 10000
    board_dimension = 5

    sim ={
            "name": "TicTacToe - Offensive VS MinimaxV2",
            "player1": ("Offensive"),
            "player2": ("Defensive")
        }

    run_simulation(sim["name"], StacSimulator(sim["player1"], sim["player2"], board_dimension), num_iterations,
                   board_dimension)


if __name__ == "__main__":
    main()

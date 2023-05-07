import re
import pygame
from ast import literal_eval
from src.games.stac.action import StacAction
from src.games.stac.state import StacState


def read_file(path):
    history_plays = []
    with open(path, 'r') as file:
        lines = file.read()
        lines = lines.split('\n')
        for line in lines:
            history_plays.append(line.split('$'))

    history_plays = [play for play in history_plays if play]
    return history_plays


def add_history(path, new_play=None):
    if new_play:
        with open(path, 'a') as file:
            file.write(new_play)


def str_to_action(str_action):
    pattern = r"Row: (\d+) \| Col: (\d+) \| Move: (\d+)"

    match = re.search(pattern, str_action)
    if match:
        row = int(match.group(1))
        col = int(match.group(2))
        move_piece = int(match.group(3))

        return StacAction(row, col, move_piece)

    return None


def str_to_state(str_state):
    pattern = r"Player: (\d), Grid: (.+), Lord: (.+), CanMove: (.+)"

    match = re.search(pattern, str_state)

    if match:
        player = int(match.group(1))
        grid = literal_eval(match.group(2))
        lord_grid = literal_eval(match.group(3))
        can_move = literal_eval(match.group(4))

        state = StacState(True)
        state.set_grid(grid)
        state.set_lord_grid(lord_grid)

        return state, (player, can_move)

    return None


def check_play(play):
    if pygame.display.get_init():
        display_state = str_to_state(play[0])
        display_state[0].display()
        print(f"{play[1]}{display_state[1]}")
        """ ANTI BREAK PYGAME """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        """ ANTI BREAK PYGAME """
        flag = input("Queres adcionar a jogada: ")
        print()
        if flag == 's':
            return True

        return False

    return True

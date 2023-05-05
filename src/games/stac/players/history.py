import re
from src.games.stac.action import StacAction


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

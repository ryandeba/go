import numpy as np

WHITE = 2
BLACK = 1

class Board:
    def __init__(self, size=9):
        self.grid = np.zeros((size, size))
        self.turn_count = 0

    def place_stone(self, x, y):
        if self.grid[y][x] != 0:
            raise Exception("Something went wrong")
        # TODO: only allow legal moves
        color = BLACK if self.turn_count % 2 == 0 else WHITE

        self.grid[y][x] = color

        self.turn_count += 1

        return color

    def print(self):
        print(self.grid)

if __name__ == '__main__':
    board = Board(size=3)

    board.place_stone(0, 0)
    board.place_stone(1, 0)
    board.place_stone(2, 0)

    board.print()

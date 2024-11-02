import pygame


# [X, Y]
pawn = [[0, 1], [1, 1], [-1, 1]]

knight = [[1, 2], [-1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, 1], [-2, -1]]


class Piece:

    def __init__(self, kind: str, color: str, coords: tuple[int, int]):
        self.kind = kind
        self.color = color
        self.coords = coords


class Knight(Piece):
    def get_possible_moves(self):
        x, y = self.coords
        return [(x + 2, y + 1), (x + 2, y - 1),
                (x - 2, y + 1), (x - 2, y - 1),
                (x + 1, y + 2), (x + 1, y - 2),
                (x - 1, y + 2), (x - 1, y - 2)]


class Square:

    def __init__(self, coords: tuple[int, int], name: str):
        self.coords = coords
        self.name = name

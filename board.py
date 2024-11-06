import sys
import pygame
from pygame import Surface

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gameDisplay = pygame.display.set_mode((1200, 800))
gameExit = True

bg = pygame.image.load('resources/img/bg.png')
brownBoard = pygame.image.load('resources/img/square_brown.png')
lightBrownBoard = pygame.image.load('resources/img/square_brown_light.png')
w_pawn = pygame.image.load('resources/img/style1/w_pawn.png')
w_rook = pygame.image.load('resources/img/style1/w_rook.png')
w_knight = pygame.image.load('resources/img/style1/w_knight.png')
w_bishop = pygame.image.load('resources/img/style1/w_bishop.png')
w_king = pygame.image.load('resources/img/style1/w_king.png')
w_queen = pygame.image.load('resources/img/style1/w_queen.png')

b_pawn = pygame.image.load('resources/img/style1/b_pawn.png')
b_rook = pygame.image.load('resources/img/style1/b_rook.png')
b_knight = pygame.image.load('resources/img/style1/b_knight.png')
b_bishop = pygame.image.load('resources/img/style1/b_bishop.png')
b_king = pygame.image.load('resources/img/style1/b_king.png')
b_queen = pygame.image.load('resources/img/style1/b_queen.png')

if not pygame.get_init():
    pygame.init()

if not pygame.font.get_init():
    pygame.font.init()


class Piece:

    def __init__(self, kind: str, color: str, img: Surface, coords: tuple[int, int]):
        self.kind = kind
        self.color = color
        self.img = img
        self.coords = coords
        self.pressed = False


class Knight(Piece):
    def get_possible_moves(self):
        x, y = self.coords
        return [(x + 2, y + 1), (x + 2, y - 1),
                (x - 2, y + 1), (x - 2, y - 1),
                (x + 1, y + 2), (x + 1, y - 2),
                (x - 1, y + 2), (x - 1, y - 2)]


class Rook(Piece):
    def get_possible_moves(self):
        x, y = self.coords
        moves = []

        # Vertical and horizontal moves
        for i in range(8):
            if i != x:  # Horizontal moves
                moves.append((i, y))
            if i != y:  # Vertical moves
                moves.append((x, i))

        return moves


class Bishop(Piece):
    def get_possible_moves(self):
        x, y = self.coords
        moves = []

        # Diagonal moves
        for i in range(1, 8):
            moves.append((x + i, y + i))  # Down-right
            moves.append((x + i, y - i))  # Up-right
            moves.append((x - i, y + i))  # Down-left
            moves.append((x - i, y - i))  # Up-left

        return moves


class Queen(Piece):
    def get_possible_moves(self):
        x, y = self.coords
        moves = []

        # Vertical and horizontal moves
        for i in range(8):
            if i != x:  # Horizontal moves
                moves.append((i, y))
            if i != y:  # Vertical moves
                moves.append((i, y))

        # Diagonal moves
        for i in range(1, 8):
            moves.append((x + i, y + i))  # Down-right
            moves.append((x + i, y - i))  # Up-right
            moves.append((x - i, y + i))  # Down-left
            moves.append((x - i, y - i))  # Up-left

        return moves


class Pawn(Piece):
    def get_possible_moves(self):
        x, y = self.coords
        return [(x, y + 1), (x + 1, y + 1), (x - 1, y + 1)]


class Square:

    def __init__(self, coords: tuple[int, int], color: str):
        self.coords = coords
        self.color = color


gameDisplay.fill(black)
gameDisplay.blit(bg, (300, 100))

pawn_b_1 = Pawn('Pawn', 'black', b_pawn, (300, 176))
pawn_b_2 = Pawn('Pawn', 'black', b_pawn, (375, 176))
pawn_b_3 = Pawn('Pawn', 'black', b_pawn, (450, 176))
pawn_b_4 = Pawn('Pawn', 'black', b_pawn, (525, 176))
pawn_b_5 = Pawn('Pawn', 'black', b_pawn, (600, 176))
pawn_b_6 = Pawn('Pawn', 'black', b_pawn, (675, 176))
pawn_b_7 = Pawn('Pawn', 'black', b_pawn, (750, 176))
pawn_b_8 = Pawn('Pawn', 'black', b_pawn, (825, 176))
rook_b_1 = Rook('Rook', 'black', b_rook, (300, 101))
rook_b_2 = Rook('Rook', 'black', b_rook, (825, 101))
knight_b_1 = Knight('Knight', 'black', b_knight, (375, 100))
knight_b_2 = Knight('Knight', 'black', b_knight, (750, 100))
bishop_b_1 = Bishop('Bishop', 'black', b_bishop, (450, 100))
bishop_b_2 = Bishop('Bishop', 'black', b_bishop, (675, 100))
king_b = Bishop('King', 'black', b_king, (600, 100))
queen_b = Bishop('Queen', 'black', b_queen, (525, 100))

pawn_w_1 = Pawn('Pawn', 'white', w_pawn, (300, 551))
pawn_w_2 = Pawn('Pawn', 'white', w_pawn, (375, 551))
pawn_w_3 = Pawn('Pawn', 'white', w_pawn, (450, 551))
pawn_w_4 = Pawn('Pawn', 'white', w_pawn, (525, 551))
pawn_w_5 = Pawn('Pawn', 'white', w_pawn, (600, 551))
pawn_w_6 = Pawn('Pawn', 'white', w_pawn, (675, 551))
pawn_w_7 = Pawn('Pawn', 'white', w_pawn, (750, 551))
pawn_w_8 = Pawn('Pawn', 'white', w_pawn, (825, 551))
rook_w_1 = Rook('Rook', 'white', w_rook, (300, 626))
rook_w_2 = Rook('Rook', 'white', w_rook, (825, 626))
knight_w_1 = Knight('Knight', 'white', w_knight, (375, 626))
knight_w_2 = Knight('Knight', 'white', w_knight, (750, 626))
bishop_w_1 = Bishop('Bishop', 'white', w_bishop, (450, 626))
bishop_w_2 = Bishop('Bishop', 'white', w_bishop, (675, 626))
king_w = Bishop('King', 'white', w_king, (600, 626))
queen_w = Bishop('Queen', 'white', w_queen, (525, 626))

square1 = Square((300, 100), 'brown')
square2 = Square((375, 100), 'light')
square3 = Square((450, 100), 'brown')
square4 = Square((525, 100), 'light')
square5 = Square((600, 100), 'brown')
square6 = Square((675, 100), 'light')
square7 = Square((750, 100), 'brown')
square8 = Square((825, 100), 'light')

square9 = Square((300, 175), 'light')
square10 = Square((375, 175), 'brown')
square11 = Square((450, 175), 'light')
square12 = Square((525, 175), 'brown')
square13 = Square((600, 175), 'light')
square14 = Square((675, 175), 'brown')
square15 = Square((750, 175), 'light')
square16 = Square((825, 175), 'brown')

square17 = Square((300, 250), 'brown')
square18 = Square((375, 250), 'light')
square19 = Square((450, 250), 'brown')
square20 = Square((525, 250), 'light')
square21 = Square((600, 250), 'brown')
square22 = Square((675, 250), 'light')
square23 = Square((750, 250), 'brown')
square24 = Square((825, 250), 'light')

square25 = Square((300, 325), 'light')
square26 = Square((375, 325), 'brown')
square27 = Square((450, 325), 'light')
square28 = Square((525, 325), 'brown')
square29 = Square((600, 325), 'light')
square30 = Square((675, 325), 'brown')
square31 = Square((750, 325), 'light')
square32 = Square((825, 325), 'brown')

square33 = Square((300, 400), 'brown')
square34 = Square((375, 400), 'light')
square35 = Square((450, 400), 'brown')
square36 = Square((525, 400), 'light')
square37 = Square((600, 400), 'brown')
square38 = Square((675, 400), 'light')
square39 = Square((750, 400), 'brown')
square40 = Square((825, 400), 'light')

square41 = Square((300, 475), 'light')
square42 = Square((375, 475), 'brown')
square43 = Square((450, 475), 'light')
square44 = Square((525, 475), 'brown')
square45 = Square((600, 475), 'light')
square46 = Square((675, 475), 'brown')
square47 = Square((750, 475), 'light')
square48 = Square((825, 475), 'brown')

square49 = Square((300, 550), 'brown')
square50 = Square((375, 550), 'light')
square51 = Square((450, 550), 'brown')
square52 = Square((525, 550), 'light')
square53 = Square((600, 550), 'brown')
square54 = Square((675, 550), 'light')
square55 = Square((750, 550), 'brown')
square56 = Square((825, 550), 'light')

square57 = Square((300, 625), 'light')
square58 = Square((375, 625), 'brown')
square59 = Square((450, 625), 'light')
square60 = Square((525, 625), 'brown')
square61 = Square((600, 625), 'light')
square62 = Square((675, 625), 'brown')
square63 = Square((750, 625), 'light')
square64 = Square((825, 625), 'brown')


square_list = [square1, square2, square3, square4, square5, square6, square7, square8, square9,
               square10, square11, square12, square13, square14, square15, square16, square17,
               square18, square19, square20, square21, square22, square23, square24, square25,
               square26, square27, square28, square29, square30, square31, square32, square33,
               square34, square35, square36, square37, square38, square39, square40, square41,
               square42, square43, square44, square45, square46, square47, square48, square49,
               square50, square51, square52, square53, square54, square55, square56, square57,
               square58, square59, square60, square61, square62, square63, square64]

for i in square_list:
    if i.color == 'light':
        gameDisplay.blit(brownBoard, (i.coords[0], i.coords[1], 10, 10))
    elif i.color == 'brown':
        gameDisplay.blit(lightBrownBoard, (i.coords[0], i.coords[1], 10, 10))

whites = [pawn_w_1, pawn_w_2, pawn_w_3, pawn_w_4, pawn_w_5, pawn_w_6, pawn_w_7, pawn_w_8,
          rook_w_1, rook_w_2, knight_w_1, knight_w_2, bishop_w_1, bishop_w_2, queen_w, king_w]
blacks = [pawn_b_1, pawn_b_2, pawn_b_3, pawn_b_4, pawn_b_5, pawn_b_6, pawn_b_7, pawn_b_8,
          rook_b_1, rook_b_2, knight_b_1, knight_b_2, bishop_b_1, bishop_b_2, queen_b, king_b]

for i in blacks:
    gameDisplay.blit(i.img, (i.coords[0], i.coords[1], 10, 10))

for i in whites:
    gameDisplay.blit(i.img, (i.coords[0], i.coords[1], 10, 10))

pygame.display.update()

while gameExit:

    # CHECKS IF QUIT BUTTON IS PRESSED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

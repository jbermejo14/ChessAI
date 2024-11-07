import sys
import pygame
from pygame import Surface

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gameDisplay = pygame.display.set_mode((1200, 800))
gameExit = True

bg = pygame.image.load('resources/img/bg.png')
brownBoard = pygame.image.load('resources/img/light.png')
lightBrownBoard = pygame.image.load('resources/img/dark.png')
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
    moves = []

    def __init__(self, kind: str, color: str, img: Surface, coords: str):
        self.kind = kind
        self.color = color
        self.img = img
        self.coords = coords
        self.pressed = False
        self.int_coords = self.get_gui_coords()  # Get coordinates from your method
        self.top_rect = pygame.Rect(self.int_coords, (75, 75))

    def get_gui_coords(self, square_size=75):
        # Map board position (e.g., "a8") to GUI coordinates
        row, col = self.coords[0], int(self.coords[1])
        x = (ord(row) - ord('a')) * square_size + 300
        y = (8 - col) * square_size + 100
        return (x, y)

    # def check_click(self):
    #     posm = pygame.mouse.get_pos()
    #     if self.top_rect.collidepoint(posm):
    #         if pygame.mouse.get_pressed()[0] is True:
    #             self.selected()

    def __repr__(self):
        return f"Piece(name={self.kind!r}, color={self.color!r}, position={self.coords!r})"


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

    def __init__(self, coords: 'str', color: str):
        self.coords = coords
        self.color = color
        self.int_coords = self.get_gui_coords()

    def get_gui_coords(self, square_size=75):
        # Map board position (e.g., "a8") to GUI coordinates
        row, col = self.coords[0], int(self.coords[1])
        x = (ord(row) - ord('a')) * square_size + 300
        y = (8 - col) * square_size + 100
        return (x, y)


gameDisplay.fill(black)
gameDisplay.blit(bg, (300, 100))

pawn_b_1 = Pawn('Pawn', 'black', b_pawn, 'a7')
pawn_b_2 = Pawn('Pawn', 'black', b_pawn, 'b7')
pawn_b_3 = Pawn('Pawn', 'black', b_pawn, 'c7')
pawn_b_4 = Pawn('Pawn', 'black', b_pawn, 'd7')
pawn_b_5 = Pawn('Pawn', 'black', b_pawn, 'e7')
pawn_b_6 = Pawn('Pawn', 'black', b_pawn, 'f7')
pawn_b_7 = Pawn('Pawn', 'black', b_pawn, 'g7')
pawn_b_8 = Pawn('Pawn', 'black', b_pawn, 'h7')

rook_b_1 = Rook('Rook', 'black', b_rook, 'a8')
knight_b_1 = Knight('Knight', 'black', b_knight, 'b8')
bishop_b_1 = Bishop('Bishop', 'black', b_bishop, 'c8')
king_b = Bishop('King', 'black', b_king, 'd8')
queen_b = Bishop('Queen', 'black', b_queen, 'e8')
bishop_b_2 = Bishop('Bishop', 'black', b_bishop, 'f8')
knight_b_2 = Knight('Knight', 'black', b_knight, 'g8')
rook_b_2 = Rook('Rook', 'black', b_rook, 'h8')

pawn_w_1 = Pawn('Pawn', 'white', w_pawn, 'a2')
pawn_w_2 = Pawn('Pawn', 'white', w_pawn, 'b2')
pawn_w_3 = Pawn('Pawn', 'white', w_pawn, 'c2')
pawn_w_4 = Pawn('Pawn', 'white', w_pawn, 'd2')
pawn_w_5 = Pawn('Pawn', 'white', w_pawn, 'e2')
pawn_w_6 = Pawn('Pawn', 'white', w_pawn, 'f2')
pawn_w_7 = Pawn('Pawn', 'white', w_pawn, 'g2')
pawn_w_8 = Pawn('Pawn', 'white', w_pawn, 'h2')

rook_w_1 = Rook('Rook', 'white', w_rook, 'a1')
knight_w_1 = Knight('Knight', 'white', w_knight, 'b1')
bishop_w_1 = Bishop('Bishop', 'white', w_bishop, 'c1')
king_w = Bishop('King', 'white', w_king, 'd1')
queen_w = Bishop('Queen', 'white', w_queen, 'e1')
bishop_w_2 = Bishop('Bishop', 'white', w_bishop, 'f1')
knight_w_2 = Knight('Knight', 'white', w_knight, 'g1')
rook_w_2 = Rook('Rook', 'white', w_rook, 'h1')

# TODO
#   CHANGE THE COORDS OF THE SQUARES (LIKE IN PIECES)
square1 = Square('a1', 'brown')
square2 = Square('a2', 'light')
square3 = Square('a3', 'brown')
square4 = Square('a4', 'light')
square5 = Square('a5', 'brown')
square6 = Square('a6', 'light')
square7 = Square('a7', 'brown')
square8 = Square('a8', 'light')

square9 = Square('b1', 'light')
square10 = Square('b2', 'brown')
square11 = Square('b3', 'light')
square12 = Square('b4', 'brown')
square13 = Square('b5', 'light')
square14 = Square('b6', 'brown')
square15 = Square('b7', 'light')
square16 = Square('b8', 'brown')

square17 = Square('c1', 'brown')
square18 = Square('c2', 'light')
square19 = Square('c3', 'brown')
square20 = Square('c4', 'light')
square21 = Square('c5', 'brown')
square22 = Square('c6', 'light')
square23 = Square('c7', 'brown')
square24 = Square('c8', 'light')

square25 = Square('d1', 'light')
square26 = Square('d2', 'brown')
square27 = Square('d3', 'light')
square28 = Square('d4', 'brown')
square29 = Square('d5', 'light')
square30 = Square('d6', 'brown')
square31 = Square('d7', 'light')
square32 = Square('d8', 'brown')

square33 = Square('e1', 'brown')
square34 = Square('e2', 'light')
square35 = Square('e3', 'brown')
square36 = Square('e4', 'light')
square37 = Square('e5', 'brown')
square38 = Square('e6', 'light')
square39 = Square('e7', 'brown')
square40 = Square('e8', 'light')

square41 = Square('f1', 'light')
square42 = Square('f2', 'brown')
square43 = Square('f3', 'light')
square44 = Square('f4', 'brown')
square45 = Square('f5', 'light')
square46 = Square('f6', 'brown')
square47 = Square('f7', 'light')
square48 = Square('f8', 'brown')

square49 = Square('g1', 'brown')
square50 = Square('g2', 'light')
square51 = Square('g3', 'brown')
square52 = Square('g4', 'light')
square53 = Square('g5', 'brown')
square54 = Square('g6', 'light')
square55 = Square('g7', 'brown')
square56 = Square('g8', 'light')

square57 = Square('h1', 'light')
square58 = Square('h2', 'brown')
square59 = Square('h3', 'light')
square60 = Square('h4', 'brown')
square61 = Square('h5', 'light')
square62 = Square('h6', 'brown')
square63 = Square('h7', 'light')
square64 = Square('h8', 'brown')

square_list = [square1, square2, square3, square4, square5, square6, square7, square8, square9,
               square10, square11, square12, square13, square14, square15, square16, square17,
               square18, square19, square20, square21, square22, square23, square24, square25,
               square26, square27, square28, square29, square30, square31, square32, square33,
               square34, square35, square36, square37, square38, square39, square40, square41,
               square42, square43, square44, square45, square46, square47, square48, square49,
               square50, square51, square52, square53, square54, square55, square56, square57,
               square58, square59, square60, square61, square62, square63, square64]

# TODO
#   MAKE A BLACK INITIAL ALSO, BE ABLE TO CHOOSE TO START WITH WHITE, BLACK OR RANDOM
#   MAKE A main_dict FOR BLACK
main_dict = {
    'a8': rook_b_1, 'b8': knight_b_1, 'c8': bishop_b_2, 'd8': queen_b, 'e8': king_b, 'f8': bishop_b_2, 'g8': knight_b_2,
    'h8': rook_b_2,
    'a7': pawn_b_1, 'b7': pawn_b_2, 'c7': pawn_b_3, 'd7': pawn_b_4, 'e7': pawn_b_5, 'f7': pawn_b_6, 'g7': pawn_b_7,
    'h7': pawn_b_8,
    'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None,
    'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None,
    'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None,
    'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None,
    'a2': pawn_w_1, 'b2': pawn_w_2, 'c2': pawn_w_3, 'd2': pawn_w_4, 'e2': pawn_w_5, 'f2': pawn_w_6, 'g2': pawn_w_7,
    'h2': pawn_w_8,
    'a1': rook_w_1, 'b1': knight_w_1, 'c1': bishop_w_1, 'd1': queen_w, 'e1': king_w, 'f1': bishop_w_2, 'g1': knight_w_2,
    'h1': rook_w_2
}

for i in square_list:
    if i.color == 'light':
        gameDisplay.blit(brownBoard, (i.int_coords[0], i.int_coords[1], 10, 10))
    elif i.color == 'brown':
        gameDisplay.blit(lightBrownBoard, (i.int_coords[0], i.int_coords[1], 10, 10))

whites = [pawn_w_1, pawn_w_2, pawn_w_3, pawn_w_4, pawn_w_5, pawn_w_6, pawn_w_7, pawn_w_8,
          rook_w_1, rook_w_2, knight_w_1, knight_w_2, bishop_w_1, bishop_w_2, queen_w, king_w]
blacks = [pawn_b_1, pawn_b_2, pawn_b_3, pawn_b_4, pawn_b_5, pawn_b_6, pawn_b_7, pawn_b_8,
          rook_b_1, rook_b_2, knight_b_1, knight_b_2, bishop_b_1, bishop_b_2, queen_b, king_b]

for i in blacks:
    gameDisplay.blit(i.img, (i.int_coords[0], i.int_coords[1], 10, 10))

for i in whites:
    gameDisplay.blit(i.img, (i.int_coords[0], i.int_coords[1], 10, 10))

pygame.display.update()

while gameExit:
    # CHECKS IF QUIT BUTTON IS PRESSED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

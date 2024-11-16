import sys
import pygame
from pygame import Surface

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gameDisplay = pygame.display.set_mode((1200, 800))
gameExit = True

selected_piece = None
turn = 'white'

bg = pygame.image.load('resources/img/bg.png')
brownBoard = pygame.image.load('resources/img/light.png')
lightBrownBoard = pygame.image.load('resources/img/dark.png')
selectedBrownBoard = pygame.image.load('resources/img/dark_selected.png')
selectedLightBrownBoard = pygame.image.load('resources/img/light_selected.png')
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

    def __init__(self, kind: str, color: str, img: Surface, pos: tuple):
        self.kind = kind
        self.color = color
        self.img = img
        self.pos = pos
        self.pressed = False
        self.int_coords = self.get_gui_pos()  # Get coordinates from your method
        self.top_rect = pygame.Rect(self.int_coords, (75, 75))

    def get_gui_pos(self, square_size=75):
        x, y = self.pos
        return x * square_size + 300, (7 - y) * square_size + 100  # Adjust for GUI positions

    def selected_action(self, possible_moves):
        for square in square_list:
            square.for_selection = False
        for i in possible_moves:
            a = main_dict.get(i)
            if 0 <= i[0] < 8 and 0 <= i[1] < 8:
                for square in square_list:
                    if square.has_piece is False:
                        if square.pos == i:
                            square.for_selection = True
                            if square.color == 'brown':
                                square.img = selectedLightBrownBoard
                            elif square.color == 'light':
                                square.img = selectedBrownBoard

    def __repr__(self):
        return f"Piece(name={self.kind!r}, color={self.color!r}, position={self.pos!r})"


class Knight(Piece):
    def get_possible_moves(self):
        x, y = self.pos
        return [(x + 2, y + 1), (x + 2, y - 1),
                (x - 2, y + 1), (x - 2, y - 1),
                (x + 1, y + 2), (x + 1, y - 2),
                (x - 1, y + 2), (x - 1, y - 2)]


class Rook(Piece):
    def get_possible_moves(self):
        x, y = self.pos
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
        x, y = self.pos
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
        x, y = self.pos
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


# TODO
#   EDIT WITH THE KING MOVES ETC
class King(Piece):
    def get_possible_moves(self):
        x, y = self.pos
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
        x, y = self.pos
        return [(x, y + 1), (x + 1, y + 1), (x - 1, y + 1)]


class Square:
    def __init__(self, pos: tuple, color: str, has_piece: bool):
        self.for_selection = False
        self.has_piece = has_piece
        self.pos = pos
        self.color = color
        self.int_coords = self.get_gui_pos()
        self.top_rect = pygame.Rect(self.int_coords, (75, 75))
        if self.color == 'light':
            self.img = lightBrownBoard
        elif self.color == 'brown':
            self.img = brownBoard

    def get_gui_pos(self, square_size=75):
        x, y = self.pos
        return x * square_size + 300, (7 - y) * square_size + 100  # Adjust for GUI positions

    def selected_action(self):
        if selected_piece is not None:
            moves_list = selected_piece.get_possible_moves()
            for move in moves_list:
                if move == self.pos:
                    for square in square_list:  #   Has_piece set to False for the square where the piece was
                        if square.pos == selected_piece.pos:
                            square.has_piece = False
                    selected_piece.pos = self.pos
                    selected_piece.int_coords = self.int_coords
                    selected_piece.top_rect = pygame.Rect(self.int_coords, (75, 75))
                    self.has_piece = True


gameDisplay.fill(black)
gameDisplay.blit(bg, (300, 100))

pawn_b_1 = Pawn('Pawn', 'black', b_pawn, (0, 6))
pawn_b_2 = Pawn('Pawn', 'black', b_pawn, (1, 6))
pawn_b_3 = Pawn('Pawn', 'black', b_pawn, (2, 6))
pawn_b_4 = Pawn('Pawn', 'black', b_pawn, (3, 6))
pawn_b_5 = Pawn('Pawn', 'black', b_pawn, (4, 6))
pawn_b_6 = Pawn('Pawn', 'black', b_pawn, (5, 6))
pawn_b_7 = Pawn('Pawn', 'black', b_pawn, (6, 6))
pawn_b_8 = Pawn('Pawn', 'black', b_pawn, (7, 6))

rook_b_1 = Rook('Rook', 'black', b_rook, (0, 7))
knight_b_1 = Knight('Knight', 'black', b_knight, (1, 7))
bishop_b_1 = Bishop('Bishop', 'black', b_bishop, (2, 7))
king_b = King('King', 'black', b_king, (3, 7))
queen_b = Queen('Queen', 'black', b_queen, (4, 7))
bishop_b_2 = Bishop('Bishop', 'black', b_bishop, (5, 7))
knight_b_2 = Knight('Knight', 'black', b_knight, (6, 7))
rook_b_2 = Rook('Rook', 'black', b_rook, (7, 7))

pawn_w_1 = Pawn('Pawn', 'white', w_pawn, (0, 1))
pawn_w_2 = Pawn('Pawn', 'white', w_pawn, (1, 1))
pawn_w_3 = Pawn('Pawn', 'white', w_pawn, (2, 1))
pawn_w_4 = Pawn('Pawn', 'white', w_pawn, (3, 1))
pawn_w_5 = Pawn('Pawn', 'white', w_pawn, (4, 1))
pawn_w_6 = Pawn('Pawn', 'white', w_pawn, (5, 1))
pawn_w_7 = Pawn('Pawn', 'white', w_pawn, (6, 1))
pawn_w_8 = Pawn('Pawn', 'white', w_pawn, (7, 1))

rook_w_1 = Rook('Rook', 'white', w_rook, (0, 0))
knight_w_1 = Knight('Knight', 'white', w_knight, (1, 0))
bishop_w_1 = Bishop('Bishop', 'white', w_bishop, (2, 0))
king_w = King('King', 'white', w_king, (3, 0))
queen_w = Queen('Queen', 'white', w_queen, (4, 0))
bishop_w_2 = Bishop('Bishop', 'white', w_bishop, (5, 0))
knight_w_2 = Knight('Knight', 'white', w_knight, (6, 0))
rook_w_2 = Rook('Rook', 'white', w_rook, (7, 0))

square1 = Square((0, 0), 'brown', True)
square2 = Square((0, 1), 'light', True)
square3 = Square((0, 2), 'brown', False)
square4 = Square((0, 3), 'light', False)
square5 = Square((0, 4), 'brown', False)
square6 = Square((0, 5), 'light', False)
square7 = Square((0, 6), 'brown', True)
square8 = Square((0, 7), 'light', True)

square9 = Square((1, 0), 'light', True)
square10 = Square((1, 1), 'brown', True)
square11 = Square((1, 2), 'light', False)
square12 = Square((1, 3), 'brown', False)
square13 = Square((1, 4), 'light', False)
square14 = Square((1, 5), 'brown', False)
square15 = Square((1, 6), 'light', True)
square16 = Square((1, 7), 'brown', True)

square17 = Square((2, 0), 'brown', True)
square18 = Square((2, 1), 'light', True)
square19 = Square((2, 2), 'brown', False)
square20 = Square((2, 3), 'light', False)
square21 = Square((2, 4), 'brown', False)
square22 = Square((2, 5), 'light', False)
square23 = Square((2, 6), 'brown', True)
square24 = Square((2, 7), 'light', True)

square25 = Square((3, 0), 'light', True)
square26 = Square((3, 1), 'brown', True)
square27 = Square((3, 2), 'light', False)
square28 = Square((3, 3), 'brown', False)
square29 = Square((3, 4), 'light', False)
square30 = Square((3, 5), 'brown', False)
square31 = Square((3, 6), 'light', True)
square32 = Square((3, 7), 'brown', True)

square33 = Square((4, 0), 'brown', True)
square34 = Square((4, 1), 'light', True)
square35 = Square((4, 2), 'brown', False)
square36 = Square((4, 3), 'light', False)
square37 = Square((4, 4), 'brown', False)
square38 = Square((4, 5), 'light', False)
square39 = Square((4, 6), 'brown', True)
square40 = Square((4, 7), 'light', True)

square41 = Square((5, 0), 'light', True)
square42 = Square((5, 1), 'brown', True)
square43 = Square((5, 2), 'light', False)
square44 = Square((5, 3), 'brown', False)
square45 = Square((5, 4), 'light', False)
square46 = Square((5, 5), 'brown', False)
square47 = Square((5, 6), 'light', True)
square48 = Square((5, 7), 'brown', True)

square49 = Square((6, 0), 'brown', True)
square50 = Square((6, 1), 'light', True)
square51 = Square((6, 2), 'brown', False)
square52 = Square((6, 3), 'light', False)
square53 = Square((6, 4), 'brown', False)
square54 = Square((6, 5), 'light', False)
square55 = Square((6, 6), 'brown', True)
square56 = Square((6, 7), 'light', True)

square57 = Square((7, 0), 'light', True)
square58 = Square((7, 1), 'brown', True)
square59 = Square((7, 2), 'light', False)
square60 = Square((7, 3), 'brown', False)
square61 = Square((7, 4), 'light', False)
square62 = Square((7, 5), 'brown', False)
square63 = Square((7, 6), 'light', True)
square64 = Square((7, 7), 'brown', True)

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
    (0, 0): rook_w_1, (1, 0): knight_w_1, (2, 0): bishop_w_1, (3, 0): queen_w, (4, 0): king_w, (5, 0): bishop_w_2,
    (6, 0): knight_w_2, (7, 0): rook_w_2,
    (0, 1): pawn_w_1, (1, 1): pawn_w_2, (2, 1): pawn_w_3, (3, 1): pawn_w_4, (4, 1): pawn_w_5, (5, 1): pawn_w_6,
    (6, 1): pawn_w_7, (7, 1): pawn_w_8,
    (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None, (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
    (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None, (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
    (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None, (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
    (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None, (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,
    (0, 6): pawn_b_1, (1, 6): pawn_b_2, (2, 6): pawn_b_3, (3, 6): pawn_b_4, (4, 6): pawn_b_5, (5, 6): pawn_b_6,
    (6, 6): pawn_b_7, (7, 6): pawn_b_8,
    (0, 7): rook_b_1, (1, 7): knight_b_1, (2, 7): bishop_b_2, (3, 7): queen_b, (4, 7): king_b, (5, 7): bishop_b_2,
    (6, 7): knight_b_2, (7, 7): rook_b_2
}

whites = [pawn_w_1, pawn_w_2, pawn_w_3, pawn_w_4, pawn_w_5, pawn_w_6, pawn_w_7, pawn_w_8,
          rook_w_1, rook_w_2, knight_w_1, knight_w_2, bishop_w_1, bishop_w_2, queen_w, king_w]
blacks = [pawn_b_1, pawn_b_2, pawn_b_3, pawn_b_4, pawn_b_5, pawn_b_6, pawn_b_7, pawn_b_8,
          rook_b_1, rook_b_2, knight_b_1, knight_b_2, bishop_b_1, bishop_b_2, queen_b, king_b]


def check_click(click_pos):  # Checks which piece has been pressed
    global selected_piece
    # if turn == 'white':
    for w_piece in whites:
        if w_piece.top_rect.collidepoint(click_pos):
            selected_piece = w_piece
            w_piece.selected_action(w_piece.get_possible_moves())

    # elif turn == 'black':
    for b_piece in blacks:
        if b_piece.top_rect.collidepoint(click_pos):
            selected_piece = b_piece
            b_piece.selected_action(b_piece.get_possible_moves())

    for square in square_list:
        if square.has_piece is False:
            if square.top_rect.collidepoint(click_pos):
                for i in square_list:
                    i.selected = False
                square.selected = True
                square.selected_action()


def refresh_screen():
    for square in square_list:
        # If square IS for selection (in the piece movement) it has the 'for selection'
        if square.for_selection:
            gameDisplay.blit(square.img, (square.int_coords[0], square.int_coords[1], 10, 10))

        # If square IS NOT for selection (in the piece movement) it has the normal img
        elif not square.for_selection:
            if square.color == 'light':
                square.img = lightBrownBoard
            elif square.color == 'brown':
                square.img = brownBoard

            gameDisplay.blit(square.img, (square.int_coords[0], square.int_coords[1], 10, 10))

    for i in blacks:
        gameDisplay.blit(i.img, (i.int_coords[0], i.int_coords[1], 10, 10))
    for i in whites:
        gameDisplay.blit(i.img, (i.int_coords[0], i.int_coords[1], 10, 10))

    pygame.display.update()


# MAIN LOOP
while gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Checks if mouse is pressed
            check_click(event.pos)
    refresh_screen()

import sys
import pygame
from pygame import Surface

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gameDisplay = pygame.display.set_mode((1200, 800))
gameExit = True

halfmove_clock = 0

move = 0
turn = 'w'

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

    def __init__(self, name: str, color: str, img: Surface, pos: tuple):
        self.name = name
        self.color = color
        self.img = img
        self.pos = pos
        self.pressed = False
        self.int_coords = self.get_gui_pos()  # Get coordinates from your method
        self.top_rect = pygame.Rect(self.int_coords, (75, 75))

    def get_gui_pos(self, square_size=75):
        x, y = self.pos
        return x * square_size + 300, (7 - y) * square_size + 100  # Adjust for GUI positions

    @staticmethod
    def selected_action(possible_moves):
        for square in square_list:
            square.for_selection = False

        for i in possible_moves:
            if type(i) is str:
                if i == 'K':
                    for square in square_list:
                        if square.pos == (6, 0):
                            square.for_selection = True
                            square.img = selectedBrownBoard
                elif i == 'Q':
                    for square in square_list:
                        if square.pos == (2, 0):
                            square.for_selection = True
                            square.img = selectedBrownBoard

            #     TODO
            #       ADD BLACKS 'k' and 'q' square selection

            elif type(i) is not str:
                if 0 <= i[0] < 8 and 0 <= i[1] < 8:
                    for square in square_list:
                        if square.has_piece is False:
                            if square.pos == i:
                                square.for_selection = True
                                if square.color == 'brown':
                                    square.img = selectedLightBrownBoard
                                elif square.color == 'light':
                                    square.img = selectedBrownBoard

    # def lambda_move(self):
    #     url = f"{API_GATEWAY_URL}/move"
    #
    #     payload = {
    #         "turn": turn,
    #     }
    #
    #     headers = {"Content-Type": "application/json"}
    #     response = requests.post(url, data=json.dumps(payload), headers=headers)
    #     return response.json()

    def __repr__(self):
        return f"Piece(name={self.name!r}, color={self.color!r}, position={self.pos!r})"


selected_piece: Piece or None


class Knight(Piece):
    def get_possible_moves(self):
        x, y = self.pos
        return [(x + 2, y + 1), (x + 2, y - 1),
                (x - 2, y + 1), (x - 2, y - 1),
                (x + 1, y + 2), (x + 1, y - 2),
                (x - 1, y + 2), (x - 1, y - 2)]


class Rook(Piece):

    def __init__(self, name: str, color: str, img: Surface, pos: tuple, initial_move: tuple):
        super().__init__(name, color, img, pos)
        self.initial_move = initial_move
        self.moved = False

    def check_moved(self):
        if self.pos != self.initial_move:
            self.moved = True

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
                moves.append((x, i))

        # Diagonal moves
        for i in range(1, 8):
            moves.append((x + i, y + i))  # Down-right
            moves.append((x + i, y - i))  # Up-right
            moves.append((x - i, y + i))  # Down-left
            moves.append((x - i, y - i))  # Up-left

        return moves


class King(Piece):

    def __init__(self, name: str, color: str, img: Surface, pos: tuple, initial_move: tuple, rooks: tuple):
        super().__init__(name, color, img, pos)
        self.rooks = rooks
        self.initial_move = initial_move
        self.moved = False

    def check_moved(self):
        if self.pos != self.initial_move:
            self.moved = True

    def check_castling(self):
        castling = ''
        if self.moved is False:
            if self.color == 'white':
                # Adjusted for white pieces
                if main_dict.get((7, 0)) is not None:
                    if main_dict.get((7, 0)).name == 'Rook':
                        if main_dict.get((5, 0)) is None and main_dict.get((6, 0)) is None:  # Empty squares switched
                            castling = castling + 'K'

                if main_dict.get((0, 0)) is not None:  # Rook position switched
                    if main_dict.get((0, 0)).name == 'Rook':
                        if main_dict.get((1, 0)) is None and main_dict.get((2, 0)) is None and main_dict.get(
                                (3, 0)) is None:  # Empty squares switched
                            castling = castling + 'Q'

            elif self.color == 'black':
                # Adjusted for black pieces
                if main_dict.get((7, 7)) is not None:  # Rook position switched
                    if main_dict.get((7, 7)).name == 'Rook':
                        if main_dict.get((5, 7)) is None and main_dict.get((6, 7)) is None:  # Empty squares switched
                            castling = castling + 'k'

                if main_dict.get((0, 7)) is not None:  # Rook position switched
                    if main_dict.get((0, 7)).name == 'Rook':
                        if main_dict.get((1, 7)) is None and main_dict.get((2, 7)) is None and main_dict.get(
                                (3, 7)) is None:  # Empty squares switched
                            castling = castling + 'q'

        return castling

    def get_possible_moves(self):
        x, y = self.pos
        move_list = [(x, y + 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y), (x - 1, y), (x, y - 1),
                     (x + 1, y - 1), (x - 1, y - 1)]

        castling = self.check_castling()
        if self.moved is False:
            if self.color == 'white':
                if 'K' in castling:
                    move_list.append('K')
                if 'Q' in castling:
                    move_list.append('Q')
            elif self.color == 'black':
                if 'k' in castling:
                    move_list.append('k')
                if 'q' in castling:
                    move_list.append('q')

        return move_list


class Pawn(Piece):

    def __init__(self, name: str, color: str, img: Surface, pos: tuple, initial_move: tuple):
        super().__init__(name, color, img, pos)
        self.initial_move = initial_move
        self.moved = False

    def check_moved(self):
        if self.pos != self.initial_move:
            self.moved = True

    def get_possible_moves(self):
        x, y = self.pos
        move_list = [(x, y + 1), (x + 1, y + 1), (x - 1, y + 1)]
        if not self.moved:
            move_list.append((x, y + 2))
        return move_list


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
                if type(move) is str:
                    if selected_piece.moved is False:
                        if move == 'K':
                            if self.pos == (6, 0):
                                for square in square_list:  # Has_piece set to False for the square where the piece was
                                    if square.pos == selected_piece.pos:
                                        square.has_piece = False
                                    elif square.pos == main_dict.get((7, 0)).pos:
                                        square.has_piece = False

                                selected_piece.pos = self.pos
                                selected_piece.int_coords = self.int_coords
                                selected_piece.top_rect = pygame.Rect(self.int_coords, (75, 75))

                                main_dict.get((7, 0)).pos = (5, 0)
                                main_dict.get((7, 0)).int_coords = main_dict.get((7, 0)).get_gui_pos()
                                main_dict.get((7, 0)).top_rect = pygame.Rect(main_dict.get((7, 0)).int_coords, (75, 75))
                                self.has_piece = True
                                halfmove()
                                fen_translate()


                        if move == 'Q':
                            if self.pos == (2, 0):
                                for square in square_list:  # Has_piece set to False for the square where the piece was
                                    if square.pos == selected_piece.pos:
                                        square.has_piece = False
                                    elif square.pos == main_dict.get((0, 0)).pos:
                                        square.has_piece = False

                                selected_piece.pos = self.pos
                                selected_piece.int_coords = self.int_coords
                                selected_piece.top_rect = pygame.Rect(self.int_coords, (75, 75))

                                main_dict.get((0, 0)).pos = (3, 0)
                                main_dict.get((0, 0)).int_coords = main_dict.get((0, 0)).get_gui_pos()
                                main_dict.get((0, 0)).top_rect = pygame.Rect(main_dict.get((0, 0)).int_coords, (75, 75))
                                self.has_piece = True
                                halfmove()
                                fen_translate()

                    # TODO
                    #   FINISH 'k' 'q' CASTLING

                    # if move == 'k':
                    # if move == 'q':
                elif move == self.pos:
                    for square in square_list:  # Has_piece set to False for the square where the piece was
                        if square.pos == selected_piece.pos:
                            square.has_piece = False

                    # Changes the item in main_dict from 'PIECE' to None and vice versa
                    piece_old_pos = selected_piece.pos
                    main_dict[move] = selected_piece
                    main_dict[piece_old_pos] = None

                    # Changes the coords of the selected piece with the empty square's coords and updates Rect
                    selected_piece.pos = self.pos
                    selected_piece.int_coords = self.int_coords
                    selected_piece.top_rect = pygame.Rect(self.int_coords, (75, 75))
                    self.has_piece = True
                    halfmove()
                    fen_translate()


# blacks WHITES
def fen_translate():
    global turn, move, main_dict, halfmove_clock
    main_string = ''
    n1 = 0
    n2 = 8
    for i in range(8):
        string = ''
        var = 0
        counter = 0
        for i in list(main_dict.values())[n1:n2]:
            counter = counter + 1
            if i is None:
                var = var + 1
            # Rook
            elif i.name == 'Rook':
                if i.color == 'white':
                    if var == 0:
                        string = string + 'R'
                    elif var != 0:
                        string = string + str(var) + 'R'
                    var = 0
                elif i.color == 'black':
                    if var == 0:
                        string = string + 'r'
                    elif var != 0:
                        string = string + str(var) + 'r'
                    var = 0
            # PAWN
            elif i.name == 'Pawn':
                if i.color == 'white':
                    if var == 0:
                        string = string + 'P'
                    elif var != 0:
                        string = string + str(var) + 'P'
                    var = 0
                elif i.color == 'black':
                    if var == 0:
                        string = string + 'p'
                    elif var != 0:
                        string = string + str(var) + 'p'
                    var = 0
            # Bishop
            elif i.name == 'Bishop':
                if i.color == 'white':
                    if var == 0:
                        string = string + 'B'
                    elif var != 0:
                        string = string + str(var) + 'B'
                    var = 0
                elif i.color == 'black':
                    if var == 0:
                        string = string + 'b'
                    elif var != 0:
                        string = string + str(var) + 'b'
                    var = 0
            # King
            elif i.name == 'King':
                if i.color == 'white':
                    if var == 0:
                        string = string + 'K'
                    elif var != 0:
                        string = string + str(var) + 'K'
                    var = 0
                elif i.color == 'black':
                    if var == 0:
                        string = string + 'k'
                    elif var != 0:
                        string = string + str(var) + 'k'
                    var = 0
            # Knight
            elif i.name == 'Knight':
                if i.color == 'white':
                    if var == 0:
                        string = string + 'N'
                    elif var != 0:
                        string = string + str(var) + 'N'
                    var = 0
                elif i.color == 'black':
                    if var == 0:
                        string = string + 'n'
                    elif var != 0:
                        string = string + str(var) + 'n'
                    var = 0
            # Queen
            elif i.name == 'Queen':
                if i.color == 'white':
                    if var == 0:
                        string = string + 'Q'
                    elif var != 0:
                        string = string + str(var) + 'Q'
                    var = 0
                elif i.color == 'black':
                    if var == 0:
                        string = string + 'q'
                    elif var != 0:
                        string = string + str(var) + 'q'
                    var = 0
            if counter == 8:
                if var != 0:
                    string = string + str(var)
        main_string = main_string + string + "/"

        n1 = n1 + 8
        n2 = n2 + 8

    main_string = main_string[:-1]
    string2 = ''

    if turn == 'w':
        string2 = 'w'
    elif turn == 'b':
        string2 = 'b'

    string3 = ''
    for king in kings:
        if not king.moved:
            if king.name == 'King':
                if king.color == 'white':
                    if not king.rooks[0].moved:
                        string3 = string3 + 'Q'
                    if not king.rooks[1].moved:
                        string3 = string3 + 'K'
                elif king.color == 'black':
                    if not king.rooks[0].moved:
                        string3 = string3 + 'q'
                    if not king.rooks[1].moved:
                        string3 = string3 + 'k'

    string4 = ''
    if selected_piece.name == 'Pawn':
        if selected_piece.color == 'white':
            if selected_piece.pos[1] == 3:
                if selected_piece.pos[0] == 0:
                    string4 = 'a3'
                elif selected_piece.pos[0] == 1:
                    string4 = 'b3'
                elif selected_piece.pos[0] == 2:
                    string4 = 'c3'
                elif selected_piece.pos[0] == 3:
                    string4 = 'd3'
                elif selected_piece.pos[0] == 4:
                    string4 = 'e3'
                elif selected_piece.pos[0] == 5:
                    string4 = 'f3'
                elif selected_piece.pos[0] == 6:
                    string4 = 'g3'
                elif selected_piece.pos[0] == 7:
                    string4 = 'h3'
            else:
                string4 = '-'
        elif selected_piece.color == 'black':
            if selected_piece.pos[1] == 4:
                if selected_piece.pos[0] == 0:
                    string4 = 'a6'
                elif selected_piece.pos[0] == 1:
                    string4 = 'b6'
                elif selected_piece.pos[0] == 2:
                    string4 = 'c6'
                elif selected_piece.pos[0] == 3:
                    string4 = 'd6'
                elif selected_piece.pos[0] == 4:
                    string4 = 'e6'
                elif selected_piece.pos[0] == 5:
                    string4 = 'f6'
                elif selected_piece.pos[0] == 6:
                    string4 = 'g6'
                elif selected_piece.pos[0] == 7:
                    string4 = 'h6'
            else:
                string4 = '-'
    else:
        string4 = '-'

    if turn == 'black':
        move = move + 1
    main_string = main_string + " " + string2 + " " + string3 + " " + string4 + " " + str(halfmove_clock) + " " + str(move)
    print(main_string)


def halfmove():
    global halfmove_clock
    if selected_piece.name == 'Pawn':
        halfmove_clock = 0
    else:
        halfmove_clock = halfmove_clock + 1


gameDisplay.fill(black)
gameDisplay.blit(bg, (300, 100))

pawn_b_1 = Pawn('Pawn', 'black', b_pawn, (0, 6), (0, 6))
pawn_b_2 = Pawn('Pawn', 'black', b_pawn, (1, 6), (1, 6))
pawn_b_3 = Pawn('Pawn', 'black', b_pawn, (2, 6), (2, 6))
pawn_b_4 = Pawn('Pawn', 'black', b_pawn, (3, 6), (3, 6))
pawn_b_5 = Pawn('Pawn', 'black', b_pawn, (4, 6), (4, 6))
pawn_b_6 = Pawn('Pawn', 'black', b_pawn, (5, 6), (5, 6))
pawn_b_7 = Pawn('Pawn', 'black', b_pawn, (6, 6), (6, 6))
pawn_b_8 = Pawn('Pawn', 'black', b_pawn, (7, 6), (7, 6))

rook_b_1 = Rook('Rook', 'black', b_rook, (0, 7), (0, 7))
knight_b_1 = Knight('Knight', 'black', b_knight, (1, 7))
bishop_b_1 = Bishop('Bishop', 'black', b_bishop, (2, 7))
queen_b = Queen('Queen', 'black', b_queen, (3, 7))
bishop_b_2 = Bishop('Bishop', 'black', b_bishop, (5, 7))
knight_b_2 = Knight('Knight', 'black', b_knight, (6, 7))
rook_b_2 = Rook('Rook', 'black', b_rook, (7, 7), (7, 7))
king_b = King('King', 'black', b_king, (4, 7), (4, 7), (rook_b_1, rook_b_2))

pawn_w_1 = Pawn('Pawn', 'white', w_pawn, (0, 1), (0, 1))
pawn_w_2 = Pawn('Pawn', 'white', w_pawn, (1, 1), (1, 1))
pawn_w_3 = Pawn('Pawn', 'white', w_pawn, (2, 1), (2, 1))
pawn_w_4 = Pawn('Pawn', 'white', w_pawn, (3, 1), (3, 1))
pawn_w_5 = Pawn('Pawn', 'white', w_pawn, (4, 1), (4, 1))
pawn_w_6 = Pawn('Pawn', 'white', w_pawn, (5, 1), (5, 1))
pawn_w_7 = Pawn('Pawn', 'white', w_pawn, (6, 1), (6, 1))
pawn_w_8 = Pawn('Pawn', 'white', w_pawn, (7, 1), (7, 1))

rook_w_1 = Rook('Rook', 'white', w_rook, (0, 0), (0, 0))
knight_w_1 = Knight('Knight', 'white', w_knight, (1, 0))
bishop_w_1 = Bishop('Bishop', 'white', w_bishop, (2, 0))
queen_w = Queen('Queen', 'white', w_queen, (3, 0))
bishop_w_2 = Bishop('Bishop', 'white', w_bishop, (5, 0))
knight_w_2 = Knight('Knight', 'white', w_knight, (6, 0))
rook_w_2 = Rook('Rook', 'white', w_rook, (7, 0), (7, 0))
king_w = King('King', 'white', w_king, (4, 0), (4, 0), (rook_w_1, rook_w_2))

square1 = Square((0, 0), 'light', True)
square2 = Square((0, 1), 'brown', True)
square3 = Square((0, 2), 'light', False)
square4 = Square((0, 3), 'brown', False)
square5 = Square((0, 4), 'light', False)
square6 = Square((0, 5), 'brown', False)
square7 = Square((0, 6), 'light', True)
square8 = Square((0, 7), 'brown', True)

square9 = Square((1, 0), 'brown', True)
square10 = Square((1, 1), 'light', True)
square11 = Square((1, 2), 'brown', False)
square12 = Square((1, 3), 'light', False)
square13 = Square((1, 4), 'brown', False)
square14 = Square((1, 5), 'light', False)
square15 = Square((1, 6), 'brown', True)
square16 = Square((1, 7), 'light', True)

square17 = Square((2, 0), 'light', True)
square18 = Square((2, 1), 'brown', True)
square19 = Square((2, 2), 'light', False)
square20 = Square((2, 3), 'brown', False)
square21 = Square((2, 4), 'light', False)
square22 = Square((2, 5), 'brown', False)
square23 = Square((2, 6), 'light', True)
square24 = Square((2, 7), 'brown', True)

square25 = Square((3, 0), 'brown', True)
square26 = Square((3, 1), 'light', True)
square27 = Square((3, 2), 'brown', False)
square28 = Square((3, 3), 'light', False)
square29 = Square((3, 4), 'brown', False)
square30 = Square((3, 5), 'light', False)
square31 = Square((3, 6), 'brown', True)
square32 = Square((3, 7), 'light', True)

square33 = Square((4, 0), 'light', True)
square34 = Square((4, 1), 'brown', True)
square35 = Square((4, 2), 'light', False)
square36 = Square((4, 3), 'brown', False)
square37 = Square((4, 4), 'light', False)
square38 = Square((4, 5), 'brown', False)
square39 = Square((4, 6), 'light', True)
square40 = Square((4, 7), 'brown', True)

square41 = Square((5, 0), 'brown', True)
square42 = Square((5, 1), 'light', True)
square43 = Square((5, 2), 'brown', False)
square44 = Square((5, 3), 'light', False)
square45 = Square((5, 4), 'brown', False)
square46 = Square((5, 5), 'light', False)
square47 = Square((5, 6), 'brown', True)
square48 = Square((5, 7), 'light', True)

square49 = Square((6, 0), 'light', True)
square50 = Square((6, 1), 'brown', True)
square51 = Square((6, 2), 'light', False)
square52 = Square((6, 3), 'brown', False)
square53 = Square((6, 4), 'light', False)
square54 = Square((6, 5), 'brown', False)
square55 = Square((6, 6), 'light', True)
square56 = Square((6, 7), 'brown', True)

square57 = Square((7, 0), 'brown', True)
square58 = Square((7, 1), 'light', True)
square59 = Square((7, 2), 'brown', False)
square60 = Square((7, 3), 'light', False)
square61 = Square((7, 4), 'brown', False)
square62 = Square((7, 5), 'light', False)
square63 = Square((7, 6), 'brown', True)
square64 = Square((7, 7), 'light', True)

square_list = [square1, square2, square3, square4, square5, square6, square7, square8, square9,
               square10, square11, square12, square13, square14, square15, square16, square17,
               square18, square19, square20, square21, square22, square23, square24, square25,
               square26, square27, square28, square29, square30, square31, square32, square33,
               square34, square35, square36, square37, square38, square39, square40, square41,
               square42, square43, square44, square45, square46, square47, square48, square49,
               square50, square51, square52, square53, square54, square55, square56, square57,
               square58, square59, square60, square61, square62, square63, square64]

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

w_passant_row = [main_dict.get((0, 4)), main_dict.get((1, 4)), main_dict.get((2, 4)), main_dict.get((3, 4)),
                 main_dict.get((4, 4)), main_dict.get((5, 4)), main_dict.get((6, 4)), main_dict.get((7, 4))]

b_passant_row = [main_dict.get((0, 5)), main_dict.get((1, 5)), main_dict.get((2, 5)), main_dict.get((3, 5)),
                 main_dict.get((4, 5)), main_dict.get((5, 5)), main_dict.get((6, 5)), main_dict.get((7, 5))]

kings = [king_w, king_b]

pawns = [pawn_w_1, pawn_w_2, pawn_w_3, pawn_w_4, pawn_w_5, pawn_w_6, pawn_w_7, pawn_w_8, pawn_b_1, pawn_b_2, pawn_b_3,
         pawn_b_4, pawn_b_5, pawn_b_6, pawn_b_7, pawn_b_8]

whites = [pawn_w_1, pawn_w_2, pawn_w_3, pawn_w_4, pawn_w_5, pawn_w_6, pawn_w_7, pawn_w_8,
          rook_w_1, rook_w_2, knight_w_1, knight_w_2, bishop_w_1, bishop_w_2, queen_w, king_w]
blacks = [pawn_b_1, pawn_b_2, pawn_b_3, pawn_b_4, pawn_b_5, pawn_b_6, pawn_b_7, pawn_b_8,
          rook_b_1, rook_b_2, knight_b_1, knight_b_2, bishop_b_1, bishop_b_2, queen_b, king_b]


def castling_check():
    global kings
    for pawn in pawns:
        pawn.check_moved()
    for king in kings:
        king.check_moved()
        for rook in king.rooks:
            rook.check_moved()


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
            castling_check()
            for piece in whites:
                if piece.name == 'King':
                    piece.check_castling()
    refresh_screen()

# TODO
#   ADD:
#       AFTER MOVING A PIECE, RETURN TO NON-SELECTED SQUARES
#       INVERTED BOARD FOR BLACK
#       NOT BEING ABLE TO MOVE WHEN PIECE IS INFRONT
#       SOUND
#

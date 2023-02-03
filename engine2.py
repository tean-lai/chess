import pygame


class Game:

    class Piece:  # empty piece

        sprite_name = "-"

        checking = False

        def __init__(self, game, color, coord, total_moves):

            self.game = game
            self.board = self.game.board
            self.screen = self.game.screen

            self.color = color
            if self.color == "w":
                self.opposite = "b"
            elif self.color == "b":
                self.opposite = "w"
            else:
                self.opposite = "-"

            self.sprite_name = self.color + self.sprite_name

            self.r, self.c = coord

            self.moves = []
            self.total_moves = total_moves

            self.sprite = pygame.transform.scale(
                pygame.image.load("Sprites/" + self.sprite_name + ".png"),
                (self.game.SQ_SIZE, self.game.SQ_SIZE)
            )

        def draw(self):

            rect = pygame.Rect(self.c * self.game.SQ_SIZE, self.r * self.game.SQ_SIZE, self.game.SQ_SIZE, self.game.SQ_SIZE)

            self.screen.blit(self.sprite, rect)

        def move(self, r, c):

            self.game.record_board()

            self.board[self.r][self.c] = self.game.Piece(self.game, "-", (self.r, self.c), 0)

            self.r = r
            self.c = c

            self.board[self.r][self.c] = self

            self.total_moves += 1

            # for line in self.board:
                # print(", ".join(list(map(lambda x: self.game.get_piece_info(x)[2:4], line))))
            # print()

        def gen_moves(self):

            pass

        def cut1(self, move_list):  # cuts all out of bounds
            # new_list = []
            #
            # for coord in move_list:
            #     if 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7:
            #         new_list.append((coord[0], coord[1]))
            #
            # return new_list

            return list(filter(
                lambda coord: 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7,
                move_list
            ))

        def cut2(self, move_list):  # for rooks, bishops, and queens
            for i in range(len(move_list)):
                observed = self.board[move_list[i][0]][move_list[i][1]]
                if observed.color == self.color:
                    return move_list[:i]
                elif observed.color == self.opposite:
                    return move_list[:i + 1]

            return move_list

        def cut3(self, move_list):  # only keeps capture moves

            return list(filter(
                lambda coord: self.board[coord[0]][coord[1]].color == self.opposite,
                move_list
            ))

        def cut4(self, move_list):  # cuts moves that land on same color

            return list(filter(
                lambda coord: self.board[coord[0]][coord[1]].color != self.color,
                move_list
            ))

        def cut5(self, move_list):  # cuts moves that would leave the king in check

            if self.sprite_name[1] == "K":
                return list(filter(
                    lambda coord: self.check(coord),
                    move_list
                ))

            # output = []
            #
            # for r in self.board:
            #     for p in r:
            #         if p.sprite_name == self.color + "K":
            #             king = p
            #
            # for coord in move_list:
            #     r, c = coord
            #
            #     place_holder = self.board[r][c]
            #     self.board[self.r][self.c] = self.game.Piece(self.game, "-", (self.r, self.c), 0)
            #     self.board[r][c] = self
            #
            #     if king.check((king.r, king.c)):
            #
            #         output.append((r, c))
            #
            #     self.board[self.r][self.c] = self
            #     self.board[r][c] = place_holder
            #
            # return output


        def cut6(self, move_list):  # only keeps empty tiles

            return list(filter(
                lambda coord: self.board[coord[0]][coord[1]].color == "-",
                move_list
            ))

        def check(self, coord):  # checks if the piece will be in danger, returns True if not in danger

            lis = []

            for r in self.board:
                for piece in r:
                    piece.checking = True

                    if piece.color == self.opposite:
                        lis.append(piece)
                        # print(piece.color)

            r, c = coord

            place_holder = self.board[r][c]
            self.board[self.r][self.c] = self.game.Piece(self.game, "-", (self.r, self.c), 0)
            self.board[r][c] = self

            in_check = False

            for piece in lis:
                piece.gen_moves()

                if (r, c) in piece.moves:
                    in_check = True
                    break

            self.board[self.r][self.c] = self
            self.board[r][c] = place_holder

            for r in self.board:
                for piece in r:
                    piece.checking = False

            return not in_check

    class Pawn(Piece):

        sprite_name = "P"

        def gen_moves(self):

            self.moves = []

            if self.color == "w":
                var = 1
            elif self.color == "b":
                var = -1

            self.moves.append((self.r - 1 * var, self.c - 1))
            self.moves.append((self.r - 1 * var, self.c + 1))

            self.moves = self.cut1(self.moves)

            # only keep the moves where there is a piece to capture
            self.moves = self.cut3(self.moves)

            sub = []
            sub.append((self.r - 1 * var, self.c))
            if not self.total_moves:
                sub.append((self.r - 2 * var, self.c))
            sub = self.cut6(sub)

            self.moves += sub

    class Rook(Piece):

        sprite_name = "R"

        def gen_moves(self):
            # will be combined later to be self.moves
            sub1 = []
            sub2 = []
            sub3 = []
            sub4 = []

            for i in range(1, 8):
                sub1.append((self.r - i, self.c))
                sub2.append((self.r + i, self.c))
                sub3.append((self.r, self.c - i))
                sub4.append((self.r, self.c + i))

            sub1 = self.cut1(sub1)
            sub2 = self.cut1(sub2)
            sub3 = self.cut1(sub3)
            sub4 = self.cut1(sub4)

            sub1 = self.cut2(sub1)
            sub2 = self.cut2(sub2)
            sub3 = self.cut2(sub3)
            sub4 = self.cut2(sub4)

            self.moves = sub1 + sub2 + sub3 + sub4

    class Knight(Piece):

        sprite_name = "N"

        def gen_moves(self):
            self.moves = [
                (self.r - 1, self.c - 2),
                (self.r - 1, self.c + 2),
                (self.r + 1, self.c - 2),
                (self.r + 1, self.c + 2),
                (self.r - 2, self.c - 1),
                (self.r - 2, self.c + 1),
                (self.r + 2, self.c - 1),
                (self.r + 2, self.c + 1)
            ]

            self.moves = self.cut1(self.moves)

            self.moves = self.cut4(self.moves)

    class Bishop(Piece):

        sprite_name = "B"

        def gen_moves(self):
            # will be combined later to be self.moves
            sub1 = []
            sub2 = []
            sub3 = []
            sub4 = []

            for i in range(1, 8):
                sub1.append((self.r - i, self.c - i))
                sub2.append((self.r - i, self.c + i))
                sub3.append((self.r + i, self.c - i))
                sub4.append((self.r + i, self.c + i))

            sub1 = self.cut1(sub1)
            sub2 = self.cut1(sub2)
            sub3 = self.cut1(sub3)
            sub4 = self.cut1(sub4)

            sub1 = self.cut2(sub1)
            sub2 = self.cut2(sub2)
            sub3 = self.cut2(sub3)
            sub4 = self.cut2(sub4)

            self.moves = sub1 + sub2 + sub3 + sub4

    class Queen(Piece):

        sprite_name = "Q"

        def gen_moves(self):
            # will be combined later to be self.moves
            sub1 = []
            sub2 = []
            sub3 = []
            sub4 = []
            sub5 = []
            sub6 = []
            sub7 = []
            sub8 = []

            for i in range(1, 8):
                sub1.append((self.r - i, self.c))
                sub2.append((self.r + i, self.c))
                sub3.append((self.r, self.c - i))
                sub4.append((self.r, self.c + i))
                sub5.append((self.r - i, self.c - i))
                sub6.append((self.r - i, self.c + i))
                sub7.append((self.r + i, self.c - i))
                sub8.append((self.r + i, self.c + i))

            sub1 = self.cut1(sub1)
            sub2 = self.cut1(sub2)
            sub3 = self.cut1(sub3)
            sub4 = self.cut1(sub4)
            sub5 = self.cut1(sub5)
            sub6 = self.cut1(sub6)
            sub7 = self.cut1(sub7)
            sub8 = self.cut1(sub8)

            sub1 = self.cut2(sub1)
            sub2 = self.cut2(sub2)
            sub3 = self.cut2(sub3)
            sub4 = self.cut2(sub4)
            sub5 = self.cut2(sub5)
            sub6 = self.cut2(sub6)
            sub7 = self.cut2(sub7)
            sub8 = self.cut2(sub8)

            self.moves = sub1 + sub2 + sub3 + sub4 + sub5 + sub6 + sub7 + sub8

    class King(Piece):

        sprite_name = "K"

        def gen_moves(self):
            self.moves = [
                (self.r - 1, self.c),
                (self.r + 1, self.c),
                (self.r, self.c - 1),
                (self.r, self.c + 1),
                (self.r - 1, self.c - 1),
                (self.r - 1, self.c + 1),
                (self.r + 1, self.c - 1),
                (self.r + 1, self.c + 1)
            ]

            self.moves = self.cut1(self.moves)

            self.moves = self.cut4(self.moves)

            if not self.checking:
                self.moves = self.cut5(self.moves)

                # BONUS: castling
                # if not self.total_moves:
                #     if self.check((self.r, self.c)) and self.check((self.r, self.c - 1)) and self.check((self.r, self.c - 2)):
                #         pass

    class TurnState:

        def __init__(self, game):

            self.game = game

            self.color = "w"

            self.piece = None
            self.reset_piece()

        def update_color(self):

            self.color = "w" if self.color == "b" else "b"

        def reset_piece(self):

            self.piece = self.game.Piece(self.game, "-", (-1, -1), 0)

    SQ_SIZE = 50
    NUM_R = NUM_C = 8
    WIDTH = HEIGHT = NUM_R * 50

    board_history = []

    def __init__(self, screen):

        self.screen = screen

        self.board = [
            ["00bR0", "01bN0", "02bB0", "03bQ0", "04bK0", "05bB0", "06bN0", "07bR0"],
            ["10bP0", "11bP0", "12bP0", "13bP0", "14bP0", "15bP0", "16bP0", "17bP0"],
            ["20--0", "21--0", "22--0", "23--0", "24--0", "25--0", "26--0", "27--0"],
            ["30--0", "31--0", "32--0", "33--0", "34--0", "35--0", "36--0", "37--0"],
            ["40--0", "41--0", "42--0", "43--0", "44--0", "45--0", "46--0", "47--0"],
            ["50--0", "51--0", "52--0", "53--0", "54--0", "55--0", "56--0", "57--0"],
            ["60wP0", "61wP0", "62wP0", "63wP0", "64wP0", "65wP0", "66wP0", "67wP0"],
            ["70wR0", "71wN0", "72wB0", "73wQ0", "74wK0", "75wB0", "76wN0", "77wR0"]
        ]
        # self.board = [
        #     ["00bR0", "01bN0", "02bB0", "03bQ0", "04--0", "05bB0", "06bN0", "07bR0"],
        #     ["10bP0", "11bP0", "12bP0", "13bP0", "14--0", "15bP0", "16bP0", "17bP0"],
        #     ["20--0", "21--0", "22--0", "23bK2", "24--0", "25--0", "26--0", "27--0"],
        #     ["30--0", "31--0", "32--0", "33--0", "34bP1", "35--0", "36--0", "37--0"],
        #     ["40--0", "41--0", "42--0", "43--0", "44--0", "45--0", "46--0", "47--0"],
        #     ["50--0", "51--0", "52--0", "53wK2", "54wP1", "55--0", "56--0", "57--0"],
        #     ["60wP0", "61wP0", "62wP0", "63wP0", "64--0", "65wP0", "66wP0", "67wP0"],
        #     ["70wR0", "71wN0", "72wB0", "73wQ0", "74--0", "75wB0", "76wN0", "77wR0"]
        # ]

        # convert all elements from ^^^^ into Piece objects
        for r in range(8):
            for c in range(8):
                string = self.board[r][c]

                self.board[r][c] = self.create_piece(string)

        # self.turn_state = ["w", self.Piece(self, "-", (-1, -1), False)]  # color turn it is and piece selected
        self.turn_state = self.TurnState(self)

    def update(self, pos=False):  # pos is True when there is a mouse input

        if pos:
            x, y = pos

            r = y // self.SQ_SIZE
            c = x // self.SQ_SIZE

            piece = self.board[r][c]

            if piece.color == self.turn_state.color and piece != self.turn_state.piece:
                self.turn_state.piece = piece
                piece.gen_moves()
            else:
                if (r, c) in self.turn_state.piece.moves:
                    self.turn_state.piece.move(r, c)
                    self.turn_state.update_color()
                    self.turn_state.reset_piece()

        self.draw()

    def draw(self):

        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                selected_piece = self.turn_state.piece

                color = [255 - 127 * ((r + c) % 2)] * 3
                if piece == selected_piece:
                    color = [0, 127, 0]

                rect1 = pygame.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)

                pygame.draw.rect(
                    self.screen,
                    color,
                    rect1
                )

                piece.draw()

                # highlights the selected piece
                if (r, c) in selected_piece.moves:
                    color = [255, 255, 0]

                    rect2 = pygame.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE / 4, self.SQ_SIZE / 4)
                    rect2.center = (rect2[0] + self.SQ_SIZE / 2, rect2[1] + self.SQ_SIZE / 2)

                    pygame.draw.rect(
                        self.screen,
                        color,
                        rect2
                    )

        # label ranks and files
        pygame.font.init()

        my_font = pygame.font.SysFont('Comic Sans MS', 25)

        for key, val in enumerate("abcdefgh"):
            rect = pygame.Rect(8 * self.SQ_SIZE, key * self.SQ_SIZE, self.SQ_SIZE / 4, self.SQ_SIZE / 4)
            rect.centerx = rect[0] + self.SQ_SIZE / 2

            text_surface = my_font.render(val, False, (0, 0, 0))
            self.screen.blit(text_surface, rect)

            rect = pygame.Rect((key) * self.SQ_SIZE, 8 * self.SQ_SIZE, self.SQ_SIZE / 4, self.SQ_SIZE / 4)
            rect.centerx = rect[0] + self.SQ_SIZE / 2

            text_surface = my_font.render(str(key + 1), False, (0, 0, 0))
            self.screen.blit(text_surface, rect)

    def record_board(self):

        lis = [[None for __ in range(8)] for __ in range(8)]

        for r in range(8):
            for c in range(8):
                lis[r][c] = self.get_piece_info(self.board[r][c])

        self.board_history.append(lis)

    def undo_move(self):

        if self.board_history:

            board = self.board_history.pop()

            for r in range(8):
                for c in range(8):
                    self.board[r][c] = self.create_piece(board[r][c])

            self.turn_state.update_color()
            self.turn_state.reset_piece()

    def create_piece(self, info):

        r = info[0]
        c = info[1]
        r, c = int(r), int(c)

        color = info[2]

        name = info[3]

        total_moves = int(info[4:])

        if name == "P":
            temp = self.Pawn
        elif name == "R":
            temp = self.Rook
        elif name == "N":
            temp = self.Knight
        elif name == "B":
            temp = self.Bishop
        elif name == "Q":
            temp = self.Queen
        elif name == "K":
            temp = self.King
        else:
            temp = self.Piece

        return temp(self, color, (r, c), total_moves)

    def get_piece_info(self, piece):
        """
        returns info
        info is a string of r + c + color + name + total_moves
        """

        info = str(piece.r) + str(piece.c)
        info += piece.sprite_name
        info += str(piece.total_moves)

        return info

    def reset_turn(self, color):
        """
        color = color turn it'll be
        """

        pass

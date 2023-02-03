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
                self.game.white_pieces.append(self)
            elif self.color == "b":
                self.opposite = "w"
                self.game.black_pieces.append(self)
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

        def draw(self, rect):

            self.screen.blit(self.sprite, rect)

        def move(self, r, c):

            if self.board[r][c].color == self.opposite:
                self.game.dead_pieces.append(self.board[r][c])

            self.board[self.r][self.c] = self.game.Piece(self.game, "-", (self.r, self.c), False)

            self.r = r
            self.c = c

            self.board[r][c] = self

            self.total_moves += 1

        def gen_moves(self):

            pass

        def cut1(self, move_list):  # cuts all out of bounds
            new_list = []

            for coord in move_list:
                if 0 <= coord[0] <= self.game.NUM_R - 1 and 0 <= coord[1] <= self.game.NUM_C - 1:
                    new_list.append((coord[0], coord[1]))

            return new_list

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

        def cut5(self, move_list):  # cuts moves that would leave the piece in danger

            return list(filter(
                lambda coord: self.check(coord),
                move_list
            ))

        def cut6(self, move_list):  # only keeps empty tiles

            return list(filter(
                lambda coord: self.board[coord[0]][coord[1]].color == "-",
                move_list
            ))

        def check(self, coord):  # checks if the piece will be in danger

            r, c = coord

            for piece in self.game.white_pieces + self.game.black_pieces:
                piece.checking = True

            place_holder = self.board[r][c]

            self.board[r][c] = self  # moves piece there temporarily
            self.board[self.r][self.c] = self.game.Piece(self.game, "-", (self.r, self.c))


            # r, c = coord
            #
            # for piece in self.game.white_pieces + self.game.black_pieces:
            #     piece.checking = True
            #
            # # must have a place holder for this algorithm
            # place_holder = self.board[r][c]
            # place_holder2 = (self.r, self.c)
            #
            # self.board[r][c] = self
            #
            # self.board[self.r][self.c] = self.game.Piece(self.game, "-", (self.r, self.c), 0)
            # self.r, self.c = r, c
            #
            # output = True
            #
            # if self.color == "w":
            #     temp = self.game.black_pieces
            # elif self.color == "b":
            #     temp = self.game.white_pieces
            #
            # for piece in temp:
            #     piece.gen_moves()
            #
            #     if (self.r, self.c) in piece.moves:
            #         output = False
            #         break
            #
            # for piece in self.game.white_pieces + self.game.black_pieces:
            #     piece.checking = False
            #
            # self.board[r][c] = place_holder
            #
            # self.r, self.c = place_holder2
            # self.board[self.r][self.c] = self
            #
            # return output

    class Pawn(Piece):

        sprite_name = "P"

        def gen_moves(self):

            var = 1 if self.color == "w" else -1

            self.moves.append((self.r - 1 * var, self.c - 1))
            self.moves.append((self.r - 1 * var, self.c + 1))

            self.moves = self.cut1(self.moves)

            # only keep the moves where there is a piece to capture
            self.moves = self.cut3(self.moves)

            if self.board[self.r - 1 * var][self.c].color == "-":  # can't move forward if there is a piece there
                self.moves.append((self.r - 1 * var, self.c))
                if self.board[self.r - 2 * var][self.c].color == "-" and self.total_moves == 0:
                    self.moves.append((self.r - 2 * var, self.c))

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

    class Button:

        def __init__(self, game, x, y, w, h, color):

            self.game = game
            self.screen = self.game.screen

            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.rect = pygame.Rect(x, y, w, h)

            self.color = color

        def action(self):

            self.game.undo_move()

        def draw(self):

            pygame.draw.rect(self.screen, self.color, self.rect)

    SQ_SIZE = 50
    NUM_R = NUM_C = 8
    WIDTH = HEIGHT = NUM_R * 50

    white_pieces = []
    black_pieces = []
    dead_pieces = []

    board_history = []

    def __init__(self, screen):

        self.screen = screen

        self.board = [
            ["bR0", "bN0", "bB0", "bQ0", "bK0", "bB0", "bN0", "bR0"],
            ["bP0", "bP0", "bP0", "bP0", "bP0", "bP0", "bP0", "bP0"],
            ["--0", "--0", "--0", "--0", "--0", "--0", "--0", "--0"],
            ["--0", "--0", "--0", "--0", "--0", "--0", "--0", "--0"],
            ["--0", "--0", "--0", "--0", "--0", "--0", "--0", "--0"],
            ["--0", "--0", "--0", "--0", "--0", "--0", "--0", "--0"],
            ["wP0", "wP0", "wP0", "wP0", "wP0", "wP0", "wP0", "wP0"],
            ["wR0", "wN0", "wB0", "wQ0", "wK0", "wB0", "wN0", "wR0"]
        ]
        # self.board = [
        #     ["bR", "--", "--", "--", "bK", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        #     ["wR", "--", "--", "--", "wK", "--", "--", "wR"]
        # ]

        # convert all elements from ^^^^ into Piece objects
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                string = self.board[r][c]

                self.board[r][c] = self.create_piece((r, c), string)

        self.turn_state = ["w", self.Piece(self, "-", (-1, -1), False)]  # color turn it is and piece selected

        self.board_old = self.board[:]

        self.buttons = [self.Button(self, self.WIDTH, 0, 100, 50, (0, 0, 255))]

        self.record_board()

    def update(self, pos=False):  # pos is True when there is a mouse input

        if pos:
            x, y = pos

            if x >= self.WIDTH or y >= self.HEIGHT:

                for button in self.buttons:
                    if button.x < x < button.x + button.w and button.y < y < button.y + button.h:
                        button.action()

                return

            r = y // self.SQ_SIZE
            c = x // self.SQ_SIZE

            piece = self.board[r][c]

            if piece.color == self.turn_state[0] and piece != self.turn_state[1]:
                self.turn_state[1] = piece
                piece.gen_moves()
            else:
                if (r, c) in self.turn_state[1].moves:
                    self.record_board()

                    self.turn_state[1].move(r, c)
                    self.turn_state[0] = self.turn_state[1].opposite
                    self.turn_state[1] = self.Piece(self, "-", (-1, -1), False)

        self.draw()

    def draw(self):

        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                selected_piece = self.turn_state[1]

                color = [255 - 127 * ((r + c) % 2)] * 3
                if piece == selected_piece:
                    color = [0, 127, 0]

                rect1 = pygame.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)

                pygame.draw.rect(
                    self.screen,
                    color,
                    rect1
                    )

                piece.draw(rect1)

                if (r, c) in selected_piece.moves:
                    color = [255, 255, 0]

                    rect2 = pygame.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE / 4, self.SQ_SIZE / 4)
                    rect2.center = (rect2[0] + self.SQ_SIZE / 2, rect2[1] + self.SQ_SIZE / 2)

                    pygame.draw.rect(
                        self.screen,
                        color,
                        rect2
                    )

                for button in self.buttons:
                    button.draw()

    def record_board(self):

        lis = [[None for __ in range(8)] for __ in range(8)]

        self.board_history.append([])

    def undo_move(self):

        pass

    def create_piece(self, coord, string):

        r, c = coord

        color = string[0]
        name = string[1]
        total_moves = int(string[2:])

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

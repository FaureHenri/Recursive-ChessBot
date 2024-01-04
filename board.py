from piece import ChessPiece


class Board:
    def __init__(self):
        self.board = {(x, y): None for x in range(8) for y in range(8)}
        self.history = []  # [(piece identifier, [(row, column), special], 1/0, True/False),] (1 alive, 0 dead),
        # True if there is a moves chain (for example if an opponent piece is eaten or for castle
        self.counter = 0  # number of moves
        self.alive = {1: [], -1: []}
        self.dead = {1: [], -1: []}

    def print(self, colour):
        """
        Method which prints the current state of the board
        :param colour: to set the orientation of the board
        """
        red = "\033[31m"
        green = "\033[32m"
        player_color = [0, green, red]
        reset = "\033[0m"
        if colour == 1:
            range_row = list(reversed(range(8)))
            range_col = range(8)
            col_names = " |A|B|C|D|E|F|G|H| "
        else:
            range_row = range(8)
            range_col = list(reversed(range(8)))
            col_names = " |H|G|F|E|D|C|B|A| "

        print()
        print(col_names)
        for r in range_row:
            print_row = str(r + 1) + "|"
            for c in range_col:
                if self.board[r, c]:
                    print_row += reset + player_color[self.board[r, c].colour] + self.board[r, c].name + reset + "|"
                else:
                    print_row += " |"
            print(print_row + str(r + 1))
        print(col_names)

    def pose_piece(self, piece, row, col, special=False, chain=False):
        """
        Method which places a piece on the target cell, firstly removing the opponent piece if there is one
        :param piece: piece to place
        :param row: row target
        :param col: column target
        :param special: True if castle or if pawn eat diagonally without an opponent pawn on the target cell
        :param chain: True or False
        """

        self.counter += 1

        # Remove the piece from its initial pose
        if piece.row is not None:
            self.board[piece.row, piece.col] = None

        # En passant
        if special and piece.name == "P":
            dead = self.board[piece.row, col]
            self.board[piece.row, col] = None
        # Castle
        elif special and piece.name == "K":
            chain = True
            dead = None
            self.castle(piece, col)
        else:
            dead = self.board[row, col]

        if dead:
            chain = True
            dead.alive = 0

            self.alive[dead.colour].remove(dead)
            self.dead[dead.colour].append(dead)

            if dead.name == "P" and (dead.row == 0 or dead.row == 7):
                self.history.append((dead, [(dead.row, dead.col), False], 0, True))
            else:
                self.history.append((dead, [(dead.row, dead.col), False], 0, False))

        # Place the piece on the target cell
        self.board[row, col] = piece
        piece.row, piece.col = row, col
        piece.history.append([(row, col), special])
        self.history.append((piece, [(row, col), special], 1, chain))

        # Pawn promotion
        if piece.name == "P" and (row == 0 or row == 7):
            self.promote(piece, pawn_to="Q")

    def move_back(self):
        """
        Method which moves back last move
        """

        self.counter -= 1

        last_moves = list(reversed(self.history))

        for k, (last_piece, last_pose, last_living, is_chain) in enumerate(last_moves):
            del self.history[-1]

            if last_living:
                del last_piece.history[-1]
                (replace_row, replace_col), _ = last_piece.history[-1]
            else:
                replace_row, replace_col = last_pose[0]
                self.dead[last_piece.colour].remove(last_piece)
                last_piece.alive = 1
                self.alive[last_piece.colour].append(last_piece)

            self.board[last_piece.row, last_piece.col] = None

            if replace_row is not None:
                self.board[replace_row, replace_col] = last_piece
            # pawn promotion case
            else:
                self.alive[last_piece.colour].remove(last_piece)
                last_piece.alive = 0

            last_piece.row, last_piece.col = replace_row, replace_col

            if not is_chain:
                break

    def promote(self, pawn, pawn_to="Q"):
        """
        Method which transforms a pawn to a queen, bishop, knight or rook
        :param pawn: pawn to promote
        :param pawn_to: Q, B, N or R
        """

        new_piece = ChessPiece(pawn.colour, pawn_to)
        new_piece.starting_pos(self.board)
        self.pose_piece(new_piece, pawn.row, pawn.col, special=False, chain=True)
        self.alive[pawn.colour].append(new_piece)
        self.counter -= 1

    def castle_rule(self, king, rook):
        """
        Method which checks if king can castle
        :param king: king
        :param rook: rook
        :return: boolean value
        """

        if len(rook.history) == 2:
            if rook.col < king.col:
                king_range = [3, 4]
                rook_range = [1, 2, 3]
            else:
                king_range = [4, 5]
                rook_range = [5, 6]

            # check that king is not in check, neither the next cell
            for ck in king_range:
                if self.is_check(king.row, ck, king.colour):
                    return False

            # check that no piece is in between the king and the rook
            for cr in rook_range:
                if self.board[king.row, cr]:
                    return False

            return True
        else:
            return False

    def castle(self, king, king_target):
        """
        Method which moves the rook for castling
        :param king: king of interest
        :param king_target: king castle pose
        """
        if king.col > king_target:
            rook = self.board[king.row, 0]
            rook_pose = 3
        else:
            rook = self.board[king.row, 7]
            rook_pose = 5

        self.pose_piece(rook, rook.row, rook_pose, special=True, chain=False)
        self.counter -= 1  # because castle is 1 move and not 2 moves

    def set_board(self):
        """
        Method which sets the board with starting positions
        """
        piece_list = ["K"] + ["N"] * 2 + ["P"] * 8 + ["R"] * 2 + ["B"] * 2 + ["Q"]
        colour_list = [1, -1]
        for color in colour_list:
            for p in piece_list:
                p_obj = ChessPiece(color, p)
                p_row, p_col = p_obj.starting_pos(self.board)
                self.pose_piece(p_obj, p_row, p_col)
                self.alive[color].append(p_obj)
                self.counter -= 1

    def is_check(self, check_r, check_c, colour, print_check=False):
        """
        Method to check if a cell is in check by the opponent
        :param check_r: row index
        :param check_c: column index
        :param colour: player colour
        :param print_check: print detail why king is in check
        :return: True or False
        """
        focus = self.board[check_r, check_c]

        # Knight Check
        knight_opp = [n for n in self.alive[-colour] if n.name == "N"]
        dist = [abs(kn.row - check_r) ** 2 + abs(kn.col - check_c) ** 2 for kn in knight_opp]
        if 5 in dist:
            if print_check:
                if focus and focus.name == "K":
                    colour_names = [0, "White", "Black"]
                    print("{} King is in check by N".format(colour_names[focus.colour]))
            return True

        # iterate through the 8 directions
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        distances = [7 - check_r, 7 - check_c, check_r, check_c, min([7 - check_r, 7 - check_c]),
                     min([check_r, 7 - check_c]), min(check_r, check_c), min([7 - check_r, check_c])]

        for [vd, hd], ds in zip(directions, distances):
            for step in range(1, ds + 1):
                cell = self.board[check_r + step * vd, check_c + step * hd]
                if not cell:
                    continue

                # if next piece in that direction is same color, no check, break
                elif cell.colour == colour:
                    break

                # if there is an opponent piece
                else:

                    # Check on the vertical or horizontal line
                    if cell.name in "RQ" and (hd == 0 or vd == 0):
                        if print_check:
                            if focus and focus.name == "K":
                                colour_names = [0, "White", "Black"]
                                print("{} King is in check by {}".format(colour_names[focus.colour], cell.name))
                        return True

                    # Check on the diagonal
                    elif cell.name in "BQ" and abs(vd) == 1 and abs(hd) == 1:
                        if print_check:
                            if focus and focus.name == "K":
                                colour_names = [0, "White", "Black"]
                                print("{} King is in check by {}".format(colour_names[focus.colour], cell.name))
                        return True

                    # Pawn Check
                    elif step == 1 and cell.name == "P" and abs(hd) == 1 and cell.row == check_r + colour:
                        if print_check:
                            if focus and focus.name == "K":
                                colour_names = [0, "White", "Black"]
                                print("{} King is in check by {}".format(colour_names[focus.colour], cell.name))
                        return True

                    # King Check
                    elif step == 1 and cell.name == "K":
                        if print_check:
                            if focus and focus.name == "K":
                                colour_names = [0, "White", "Black"]
                                print("{} King is in check by {}".format(colour_names[focus.colour], cell.name))
                        return True
                    else:
                        break
        return False

    def is_checkmate(self, colour, print_check=False):
        """
        Method which checks if a team is checkmate
        :param colour: team to check
        :param print_check: to print why king is in check position
        :return: boolean value
        """

        king = next(k for k in self.alive[colour] if k.name == "K")
        if self.is_check(king.row, king.col, colour, print_check=print_check):
            if any(self.legal_moves(colour)):
                return False
            else:
                return True
        # elif not any(self.next_moves(colour)):
        #     return True, "DRAW"
        else:
            return False

    def is_draw(self):
        """
        Method which return True if Game is Draw by repetition
        :return: boolean value
        """
        if self.history[-2:-1] == self.history[-4:-3] == self.history[-6:-5]:
            return True
        else:
            return False

    def chess_rules(self, piece, pos_options, print_opt=False):
        """
        Method which check if a move follows chess rules
        :param piece: piece to move
        :param pos_options: future piece positions
        :param print_opt: print why a move is not possible
        :return: list of lists of boolean values, the first is move is allowed, the second if it is a special move,
        "en passant" or "castle"
        """
        king = next(k for k in self.alive[piece.colour] if k.name == "K")
        ipx, ipy = piece.row, piece.col
        is_feasible = [[True, False] for _ in range(len(pos_options))]
        for k, (px, py) in enumerate(pos_options):
            # check move is still on the board
            if px not in range(8) or py not in range(8):
                if print_opt:
                    print("Move out of the board")
                is_feasible[k][0] = False
                continue

            future = self.board[px, py]
            dx, dy = px - ipx, py - ipy
            abs_dx, abs_dy = abs(dx), abs(dy)

            # King cannot be taken
            if future and future.name == "K":
                if print_opt:
                    print("King can't be taken")
                is_feasible[k][0] = False
                continue

            # Check there is no piece from the same colour and for pawns, that there is no piece for vertical moves
            elif future and (future.colour == piece.colour or (piece.name == "P" and abs_dy == 0)):
                if print_opt:
                    print("This cell is not free")
                is_feasible[k][0] = False
                continue

            # check that pawns can only move diagonally while eating a piece from the opponent
            elif piece.name == "P" and abs_dy == 1:
                pawn_opp = self.board[ipx, ipy + dy]  # different from future var ("en passant")

                # Pawns can move diagonally to eat an opponent piece or "en passant"
                if not future and not (
                        pawn_opp and pawn_opp.name == "P" and pawn_opp.colour != piece.colour and self.history[-1][1] ==
                        pawn_opp.history[-1] and len(pawn_opp.history) == 3 and (
                                pawn_opp.row == 3 or pawn_opp.row == 4)):
                    if print_opt:
                        print("Pawns cannot move diagonally")
                    is_feasible[k][0] = False
                    continue
                elif future:
                    pass
                else:
                    is_feasible[k][1] = True
                    if print_opt:
                        print("En passant")

            # check that no piece is on the way for pawns, rooks, queen vertical moves
            elif piece.name in "PRQ" and abs_dx >= 2 and abs_dy == 0 and any(
                    i for i in [self.board[r, ipy] for r in range(min(ipx + 1, px + 1), max(ipx, px))]):
                if print_opt:
                    print("The way is not free (vertical)")
                is_feasible[k][0] = False
                continue

            # check that no piece is on the way for pawns, rooks, queen horizontal moves
            elif piece.name in "RQ" and abs_dy >= 2 and abs_dx == 0 and any(
                    i for i in [self.board[ipx, c] for c in range(min(ipy + 1, py + 1), max(ipy, py))]):
                if print_opt:
                    print("The way is not free (horizontal)")
                is_feasible[k][0] = False
                continue

            # check that no piece is on the way for bishops, queen diagonal moves
            elif piece.name in "BQ" and abs_dx >= 2 and abs_dy >= 2:
                if dx * dy < 0:
                    row_range, col_range = reversed(range(min(ipx + 1, px + 1), max(ipx, px))), range(
                        min(ipy + 1, py + 1), max(ipy, py))
                else:
                    row_range, col_range = range(min(ipx + 1, px + 1), max(ipx, px)), range(min(ipy + 1, py + 1),
                                                                                            max(ipy, py))

                if any(i for i in [self.board[i, j] for i, j in zip(row_range, col_range)]):
                    if print_opt:
                        print("The way is not free (diagonal)")
                    is_feasible[k][0] = False
                    continue

            # Castle rule
            elif piece.name == "K" and len(piece.history) == 2 and abs_dy == 2:
                if dy == 2:
                    castle_rook = self.board[piece.row, 7]
                    if castle_rook:
                        can_castle = self.castle_rule(piece, castle_rook)
                        if not can_castle:
                            if print_opt:
                                print("Castle not possible")
                            is_feasible[k][0] = False
                            continue
                        else:
                            if print_opt:
                                print("King Castle")
                            is_feasible[k][1] = True
                    else:
                        is_feasible[k][0] = False
                        continue
                elif dy == -2:
                    castle_rook = self.board[piece.row, 0]
                    if castle_rook:
                        can_castle = self.castle_rule(piece, castle_rook)
                        if not can_castle:
                            if print_opt:
                                print("Castle not possible")
                            is_feasible[k][0] = False
                            continue
                        else:
                            if print_opt:
                                print("King Castle")
                            is_feasible[k][1] = True
                    else:
                        is_feasible[k][0] = False
                        continue

            # Never let your own king in check
            self.pose_piece(piece, px, py, special=is_feasible[k][1])

            if piece.name == "K":
                king_x, king_y = px, py
            else:
                king_x, king_y = king.row, king.col

            if self.is_check(king_x, king_y, king.colour, print_check=print_opt):
                if print_opt:
                    print("This move put the King in check")
                is_feasible[k][0] = False

            self.move_back()
        return is_feasible

    def potential_pos(self, piece, print_opt=False):
        """
        Method which identifies allowed moves
        :param piece: piece
        :param print_opt: print details why a move is not allowed
        :return: list of tuple of allowed moves for a specific piece
        """
        dirs, dist = piece.possible_moves()

        future_moves = []
        for [vd, hd], ds in zip(dirs, dist):
            for step in range(1, ds + 1):
                future_moves.append((piece.row + step * vd, piece.col + step * hd))

        # Pawn can move two cells ahead if did not move yet
        if piece.name == "P" and len(piece.history) == 2:
            future_moves.append((piece.row + 2 * piece.colour, piece.col))
        # King can castle if did not move yet (1st condition but not last)
        elif piece.name == "K" and len(piece.history) == 2:
            future_moves.append((piece.row, piece.col + 2))
            future_moves.append((piece.row, piece.col - 2))

        allowed = self.chess_rules(piece, future_moves, print_opt=print_opt)
        allowed_moves = [[m, b[1]] for m, b in zip(future_moves, allowed) if b[0]]

        return allowed_moves

    def legal_moves(self, colour):
        """
        Method which determines all possible moves for a player
        :param colour: -1 or 1
        :return: list of tuples of possible moves for a colour [(piece, [(row, column), special]),]
        """

        legal_moves = []
        for piece in self.alive[colour]:
            legals = self.potential_pos(piece, print_opt=False)
            legal_moves += [(piece, leg) for leg in legals]

        return legal_moves

    def evaluate(self, colour):
        """
        Method which evaluate state of the board
        :param colour: team side
        :return: team score
        """
        team = self.alive[colour]
        opponent = self.alive[-colour]

        team_value = sum([v.value + v.heatmap[v.row][v.col] for v in team])
        opponent_value = sum([v.value + v.heatmap[v.row][v.col] for v in opponent])

        team_value -= opponent_value

        if self.is_checkmate(-colour, print_check=False):
            team_value = float("inf")
        elif self.is_draw():
            team_value -= 5

        return team_value


class BoardCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.colour = 1 if (row + col) % 2 == 0 else -1


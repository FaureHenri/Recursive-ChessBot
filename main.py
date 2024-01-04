import random
import time
from utils import *
from board import Board
from bot import robot


def main(chess_board, against_bot=True, bot_against_bot=False, bot_iter=4):
    """
    Main method to run the chess game
    :param chess_board: Board of interest
    :param against_bot: Human against bot.
    :param bot_against_bot: Bot against bot
    :param bot_iter: Depth of prediction
    """
    player_color = random.choice([1, -1])
    color_list = [0, "White", "Black"]  # 1 for White, -1 for Black
    player_team = color_list[player_color]
    print("You play {}".format(player_team))
    active_color = 1  # White starts

    if against_bot:
        chess_board.print(player_color)
    else:
        chess_board.print(active_color)

    for i in range(500):
        print("counter:", int(chess_board.counter / 2))
        player = color_list[active_color]
        is_valid = True
        human = True
        piece, f_pos, is_special = None, None, False

        lives = chess_board.alive[-1] + chess_board.alive[1]
        if len(lives) <= 6:
            bot_iter = 5
        elif len(lives) <= 10:
            bot_iter = 4
        elif len(lives) <= 16:
            bot_iter = 4

        if (player == player_team or not against_bot) and not bot_against_bot:
            i_move = input("\033[0m" + "\n" + player + " Player: from: ")
            try:
                i_pos = pos_converter(i_move, direction=1)
            except (Exception,):
                print("\033[31m" + "Wrong input")
                continue

            if not 0 <= i_pos[0] < 8 or not 0 <= i_pos[1] < 8:
                is_valid = False
                print("\033[31m" + "Input out of range" + "\033[0m")
            else:
                piece = chess_board.board[i_pos[0], i_pos[1]]

                if not piece or piece.colour != active_color:
                    print("\033[31m" + "Move impossible, you don't have a piece here" + "\033[0m")
                    is_valid = False
                else:
                    f_move = input("to: ")
                    try:
                        f_pos = pos_converter(f_move)
                    except (Exception,):
                        print("\033[31m" + "Wrong input" + "\033[0m")
                        continue

                    possibles = chess_board.potential_pos(piece, print_opt=False)
                    poss_move = [p for p, _ in possibles]
                    if tuple(f_pos) in poss_move:
                        is_valid = True
                        is_special = [s for p, s in possibles if p == tuple(f_pos)][0]

                    else:
                        chess_board.chess_rules(piece, [(f_pos[0], f_pos[1])], print_opt=True)
                        is_valid = False
                        print("\033[31m" + "The move is not valid" + "\033[0m")

        elif (against_bot and player != player_team) or (bot_against_bot and player == player_team):
            human = False
            tic = time.time()
            _, [piece, [f_pos, is_special]] = robot(chess_board, active_color, iteration=bot_iter)
            # new_board = mcts(chess_board, active_color, 1000)
            tac = time.time()
            dt = tac - tic
            print("\033[32m" + "\n" + "Bot moved {} to {} [{}]".format(piece.name, pos_converter(f_pos, -1), dt)
                  + "\033[0m")
        else:
            human = False
            tic = time.time()
            _, [piece, [f_pos, is_special]] = robot(chess_board, active_color, iteration=bot_iter)
            tac = time.time()
            dt = tac - tic
            print("\033[32m" + "\n" + "Bot moved {} to {} [{}]".format(piece.name, pos_converter(f_pos, -1), dt)
                  + "\033[0m")

        if is_valid:
            chess_board.pose_piece(piece, f_pos[0], f_pos[1], special=is_special)
            chess_board.print(1)
            print("\nDead white pieces:", [p.name for p in chess_board.dead[1]])
            print("Dead black pieces:", [p.name for p in chess_board.dead[-1]])

            if human:
                cancel = input("\nCancel last move? [yes/no]")

                if cancel == "yes":
                    chess_board.move_back()
                    chess_board.print(1)
                    continue

            is_mate = chess_board.is_checkmate(-active_color, print_check=True)

            if is_mate:
                print("{} Wins".format(player))
                break

            # switch player
            active_color = -active_color


if __name__ == '__main__':
    my_board = Board()
    my_board.set_board()

    main(my_board, against_bot=True, bot_against_bot=False, bot_iter=3)
    print(" ------- Game finished ------- ")

 
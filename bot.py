def robot(board, colour, iteration=3):
    """
    Recursive method to predict next best move
    :param board: board of interest
    :param colour: team to play
    :param iteration: depth of exploring
    :return: best score float, best move [piece, [(row, column), special]]
    """

    if iteration == 0:
        board_state = board.evaluate(colour=colour)

        return board_state, None

    best_score = float("-inf")
    best_move = None
    best_iter = 0

    legal = board.legal_moves(colour)

    # Draw case
    if not legal and not board.is_checkmate(colour):
        best_score = 0

    for leg, pos in legal:
        (leg_r, leg_c), spe = pos
        board.pose_piece(leg, leg_r, leg_c, spe)
        score, _ = robot(board, -colour, iteration=iteration - 1)
        score = -score

        board.move_back()

        if score > best_score or (score == best_score and iteration >= best_iter):
            best_score = score
            best_move = [leg, pos]
            best_iter = iteration
            if best_score == float("inf"):
                break

    return best_score, best_move

 
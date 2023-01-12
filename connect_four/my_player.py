import math

infinity = math.inf

def h_alphabeta_search(player, board):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""

    print("On est entré dans la loop : ",player)

    def max_value(board, alpha, beta, depth):

        if board.check_game_over(player)[0]:
            final_score = board.check_game_over(player)[1]
            # print("FINAL : ", final_score)
            return final_score, None
        if depth > 5:
            score =  board.score_heuristic(current_player=player,size=2) / 100
            # print("Max_value : ", score)
            return score, None

        v, move = -infinity, None
        actions = filter_valid_moves(board.get_valid_moves(player))
        for a in actions:
            # if a[0] == 1:
                next_board = board.clone()
                next_board.play_action(a)
                v2, _ = min_value(next_board, alpha, beta, depth + 1)
                if v2 > v:
                    v, move = v2, a
                    alpha = max(alpha, v)
                if v >= beta:
                    return v, move
        return v, move

    def min_value(board, alpha, beta, depth):

        if board.check_game_over(player)[0]:
            final_score = board.check_game_over(player)[1]
            # print("FINAL : ", final_score)
            return final_score, None
        if depth > 5:
            score = board.score_heuristic(current_player=player,size=2) / 100
            # print("Min_value : ", score)
            return score, None

        v, move = +infinity, None
        actions = filter_valid_moves(board.get_valid_moves(player))
        for a in actions:
            # if a[0] == 1:
                next_board = board.clone()
                next_board.play_action(a)
                v2, _ = max_value(next_board, alpha, beta, depth + 1)
                if v2 < v:
                    v, move = v2, a
                    beta = min(beta, v)
                if v <= alpha:
                    return v, move
        return v, move
    end = max_value(board, -infinity, +infinity, 0)
    print("END : ", end)
    return end


def filter_valid_moves(valid_moves):
        """Filters the valid_moves array and returns a list of tuples with only the moves whose first element is 1.

        Args:
            valid_moves: A numpy array of moves in the form of (validity, row, column) tuples.

        Returns:
            A list of valid moves in the form of (row, column) tuples.
        """
        filtered_moves = []
        for move in valid_moves:
            if move[0] == 1:
                filtered_moves.append((move[1], move[2]))
        return filtered_moves
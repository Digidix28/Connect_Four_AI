import math
import statistics
infinity = math.inf


def h_alphabeta_search3(player, board,transposition_table,uses_tt):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""
    
    if uses_tt:
        best_move =  transposition_table.get_best_move(board.state)
        if(best_move != None):
            print("WE ARE IN")
            return (0,best_move,transposition_table.hash_map)

    print("On est entré dans la loop : ",player)

    def max_value(board, alpha, beta, depth):

        if board.check_game_over(player)[0]:
            final_score = board.check_game_over(player)[1]
            # print("FINAL : ", final_score)
            return final_score, None
        if depth > 8:
            score = score_heuristic(board,current_player=player,size=2) / 100000
            # print("Max_value : ", score)
            return score, None

        # I also want to check in the table when exploring the tree, but I first need to modify the table so that it takes the move plus the score associated to it
        # best_move =  transposition_table.get_best_move(board.state)
        # if(best_move != None):
        #     print("WE ARE IN")
        #     return (0,best_move,transposition_table.hash_map)

        v, move = -infinity, None
        actions = filter_valid_moves(board.get_valid_moves(player))

        def middle_first(x):
            second_values = [t[1] for t in actions]
            median = statistics.median(second_values)
            return abs(x[1] - median)

        actions = sorted(actions, key=middle_first)
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

        if depth > 8:
            score = score_heuristic(board,current_player=player,size=2) / 100000
            # print("Min_value : ", score)
            return score, None

        v, move = +infinity, None
        actions = filter_valid_moves(board.get_valid_moves(player))

        def middle_first(x):
            second_values = [t[1] for t in actions]
            median = statistics.median(second_values)
            return abs(x[1] - median)
            
        actions = sorted(actions, key=middle_first)
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

    v,move = max_value(board, -infinity, +infinity, 0)
    print("END : ", (v,move))

    if uses_tt:
        transposition_table.store_best_move(board.state,move)
    
    return v,move,transposition_table.hash_map



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


def score_heuristic(board,current_player,size):
        """Counts the number of winning possibilities"""

        # Define player A and player B
        player_a = current_player

        # Define the number of possibilities for each player
        player_a_possibilities_count = 0

        # Loop through every position on the board
        for x in range(board.row):
            for y in range(board.column):
                # Initialize player A and player B count
                player_a_count = 0

                # If the current position is occupied by player A,
                # search in all 8 directions for similar pieces
                if board.state[x][y] == player_a:
                    player_a_count += 1

                    for i in range(len(board.directions)):
                        # Get direction tuple
                        d = board.directions[i]

                        # Calculate next position
                        r = x + d[0]
                        c = y + d[1]

                        # Check if next position is within board boundaries
                        if r < board.row and c < board.column:
                            count = 1

                            # Keep searching for a connect in this direction
                            while True:
                                r = x + d[0] * count
                                c = y + d[1] * count
                                count += 1

                                # Check if next position is within board boundaries
                                if 0 <= r < board.row and 0 <= c < board.column:
                                    # If the next position is occupied by player A,
                                    # increment the count
                    
                                    if board.state[r][c] == player_a:
                                        player_a_count += 1
                                    # Otherwise, stop searching in this direction
                                    else:
                                        break
                                # If next position is not within board boundaries,
                                # stop searching in this direction
                                else:
                                    break

                        # If player A has enough pieces in a row,
                        # the game is over and player A wins
                        LOOKUP_TABLE = {
                            2: 50,
                            3: 1000
                        }

                        if player_a_count in LOOKUP_TABLE:
                            if x + player_a_count*d[0] < board.row and y + player_a_count*d[1] < board.column:
                                if board.state[x + player_a_count*d[0]][y + player_a_count*d[1]] == 0:
                                    player_a_possibilities_count += LOOKUP_TABLE[player_a_count]

                        # Reset player A count for next direction
                        player_a_count = 1

                

        return player_a_possibilities_count 

def count_open_threes(game, player):
    count = 0
    # Loop through every position on the board
    for x in range(game.row):
        for y in range(game.column):
            # If the current position is occupied by the given player,
            # search in all 8 directions for similar pieces
            if game.state[x][y] == player:
                for i in range(len(game.directions)):
                    # Get direction tuple
                    d = game.directions[i]
                    # Calculate next position
                    r = x + d[0]
                    c = y + d[1]
                    # Check if next position is within board boundaries
                    if r >= 0 and r < game.row and c >= 0 and c < game.column:
                        # If the next position is empty, check if there are three similar pieces in a row
                        if game.state[r][c] == 0:
                            three_in_a_row = True
                            for j in range(1, 4):
                                r2 = x + d[0] * j
                                c2 = y + d[1] * j
                                if not (0 <= r2 < game.row and 0 <= c2 < game.column and game.state[r2][c2] == player):
                                    three_in_a_row = False
                                    break
                            if three_in_a_row:
                                count += 1
    return count

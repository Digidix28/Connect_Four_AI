import random

def random_player_(player, board,transposition_table):
    actions = filter_valid_moves(board.get_valid_moves(player))
    move = random.choice(actions)
    clone = board.clone()
    clone.play_action(move)
    i=0
    while transposition_table.get_hash(clone.state) in transposition_table.hash_map and i < 10:
        move = random.choice(actions)
        clone = board.clone()
        clone.play_action(move)
        i +=1
    return move

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
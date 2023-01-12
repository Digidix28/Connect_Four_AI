"""Class for Board State and Logic."""
from copy import deepcopy

import numpy as np

from game import Game


class ConnectFourGame(Game):
    """Represents the game board and its logic.

    Attributes:
        row: An integer indicating the length of the board row.
        column: An integer indicating the length of the board column.
        connect: An integer indicating the number of pieces to connect.
        current_player: An integer to keep track of the current player.
        state: A list which stores the game state in matrix form.
        action_size: An integer indicating the total number of board squares.
        directions: A dictionary containing tuples to check for valid moves.
    """

    def __init__(self):
        """Initializes ConnectFourGame with the initial board state."""
        super().__init__()
        self.row = 6
        self.column = 7
        self.connect = 4
        self.current_player = 1
        self.state = []
        self.action_size = self.row * self.column

        # Create a n x n matrix to represent the board
        for i in range(self.row):
            self.state.append([0 * j for j in range(self.column)])

        self.state = np.array(self.state)

        self.directions = {
            # 0: (-1, -1),
            # 1: (-1, 0),
            # 2: (-1, 1),
            # 3: (0, -1),
            0: (0, 1),
            1: (1, -1),
            2: (1, 0),
            3: (1, 1)
        }

    def clone(self):
        """Creates a deep clone of the game object.

        Returns:
            the cloned game object.
        """
        game_clone = ConnectFourGame()
        game_clone.state = deepcopy(self.state)
        game_clone.current_player = self.current_player
        return game_clone

    def play_action(self, action):
        """Plays an action on the game board.

        Args:
            action: A tuple in the form of (row, column).
        """
        x = action[0]
        y = action[1]

        self.state[x][y] = self.current_player
        self.current_player = -self.current_player

    def get_valid_moves(self, current_player):
        """Returns a list of moves along with their validity.

        Searches the board for zeros(0). 0 represents an empty square.

        Returns:
            A list containing moves in the form of (validity, row, column).
        """
        valid_moves = []

        for x in range(self.row):
            for y in range(self.column):
                if self.state[x][y] == 0:
                    if x + 1 == self.row:
                        valid_moves.append((1, x, y))
                    elif x + 1 < self.row:
                        if self.state[x + 1][y] != 0:
                            valid_moves.append((1, x, y))
                        else:
                            valid_moves.append((0, None, None))
                else:
                    valid_moves.append((0, None, None))

        return np.array(valid_moves)


    def get_next_open_row(self, column):
        """Returns the row index of the next open position in the given column.

        Args:
            column: An integer representing the column index.

        Returns:
            An integer representing the row index of the next open position in the given column.
            If the column is full, returns None.
        """
        for row in range(self.row - 1, -1, -1):
            if self.state[row][column] == 0:
                return row
        return None

    def score_heuristic(self,current_player,size):
        """Counts the number of winning possibilities"""

        # Define player A and player B
        player_a = current_player
        player_b = -current_player

        # Define the number of possibilities for each player
        player_a_possibilities_count = 0
        player_b_possibilities_count = 0

        # Loop through every position on the board
        for x in range(self.row):
            for y in range(self.column):
                # Initialize player A and player B count
                player_a_count = 0
                player_b_count = 0

                # If the current position is occupied by player A,
                # search in all 8 directions for similar pieces
                if self.state[x][y] == player_a:
                    player_a_count += 1

                    for i in range(len(self.directions)):
                        # Get direction tuple
                        d = self.directions[i]

                        # Calculate next position
                        r = x + d[0]
                        c = y + d[1]

                        # Check if next position is within board boundaries
                        if r < self.row and c < self.column:
                            count = 1

                            # Keep searching for a connect in this direction
                            while True:
                                r = x + d[0] * count
                                c = y + d[1] * count
                                count += 1

                                # Check if next position is within board boundaries
                                if 0 <= r < self.row and 0 <= c < self.column:
                                    # If the next position is occupied by player A,
                                    # increment the count

                                    if self.state[r][c] == player_a:
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
                        if player_a_count >= size:
                            player_a_possibilities_count += 1

                        # Reset player A count for next direction
                        player_a_count = 1

                # If the current position is occupied by player B,
                # search in all 8 directions for similar pieces
                if self.state[x][y] == player_b:
                    player_b_count += 1

                    for i in range(len(self.directions)):
                        # Get direction tuple
                        d = self.directions[i]

                        # Calculate next position
                        r = x + d[0]
                        c = y + d[1]

                        # Check if next position is within board boundaries
                        if r < self.row and c < self.column:
                            count = 1

                            # Keep searching for a connect in this direction
                            while True:
                                r = x + d[0] * count
                                c = y + d[1] * count
                                count += 1

                                # Check if next position is within board boundaries
                                if 0 <= r < self.row and 0 <= c < self.column:
                                    # If the next position is occupied by player B,
                                    # increment the count
                                    if self.state[r][c] == player_b:
                                        player_b_count += 1
                                    # Otherwise, stop searching in this direction
                                    else:
                                        break
                                # If next position is not within board boundaries,
                                # stop searching in this direction
                                else:
                                    break

                        # If player B has enough pieces in a row,
                        # the game is over and player B wins
                        if player_b_count >= size:
                            player_b_possibilities_count += 1

                        # Reset player B count for next direction
                        player_b_count = 1

        return player_a_possibilities_count

    def check_game_over(self, current_player):
        """Checks if the game is over and return a possible winner.

        There are 3 possible scenarios.
            a) The game is over and we have a winner.
            b) The game is over but it is a draw.
            c) The game is not over.

        Args:
            current_player: An integer representing the current player.

        Returns:
            A bool representing the game over state.
            An integer action value. (win: 1, loss: -1, draw: 0
        """

        # Define player A and player B
        player_a = current_player
        player_b = -current_player

        # Loop through every position on the board
        for x in range(self.row):
            for y in range(self.column):
                # Initialize player A and player B count
                player_a_count = 0
                player_b_count = 0

                # If the current position is occupied by player A,
                # search in all 8 directions for similar pieces
                if self.state[x][y] == player_a:
                    player_a_count += 1

                    for i in range(len(self.directions)):
                        # Get direction tuple
                        d = self.directions[i]

                        # Calculate next position
                        r = x + d[0]
                        c = y + d[1]

                        # Check if next position is within board boundaries
                        if r < self.row and c < self.column:
                            count = 1

                            # Keep searching for a connect in this direction
                            while True:
                                r = x + d[0] * count
                                c = y + d[1] * count
                                count += 1

                                # Check if next position is within board boundaries
                                if 0 <= r < self.row and 0 <= c < self.column:
                                    # If the next position is occupied by player A,
                                    # increment the count

                                    if self.state[r][c] == player_a:
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
                        if player_a_count >= self.connect:
                            return True, 1

                        # Reset player A count for next direction
                        player_a_count = 1

                # If the current position is occupied by player B,
                # search in all 8 directions for similar pieces
                if self.state[x][y] == player_b:
                    player_b_count += 1

                    for i in range(len(self.directions)):
                        # Get direction tuple
                        d = self.directions[i]

                        # Calculate next position
                        r = x + d[0]
                        c = y + d[1]

                        # Check if next position is within board boundaries
                        if r < self.row and c < self.column:
                            count = 1

                            # Keep searching for a connect in this direction
                            while True:
                                r = x + d[0] * count
                                c = y + d[1] * count
                                count += 1

                                # Check if next position is within board boundaries
                                if 0 <= r < self.row and 0 <= c < self.column:
                                    # If the next position is occupied by player B,
                                    # increment the count
                                    if self.state[r][c] == player_b:
                                        player_b_count += 1
                                    # Otherwise, stop searching in this direction
                                    else:
                                        break
                                # If next position is not within board boundaries,
                                # stop searching in this direction
                                else:
                                    break

                        # If player B has enough pieces in a row,
                        # the game is over and player B wins
                        if player_b_count >= self.connect:
                            return True, -1

                        # Reset player B count for next direction
                        player_b_count = 1

        # Get list of valid moves
        valid_moves = self.get_valid_moves(current_player)

        # Check if there are any valid moves left
        for move in valid_moves:
            if move[0] is 1:
                return False, 0

        # If there are no moves left the game is over without a winner
        return True, 0

    def print_board(self):
        """Prints the board state."""
        print("   0    1    2    3    4    5    6")
        for x in range(self.row):
            print(x, end='')
            for y in range(self.column):
                if self.state[x][y] == 0:
                    print('  -  ', end='')
                elif self.state[x][y] == 1:
                    print('  X  ', end='')
                elif self.state[x][y] == -1:
                    print('  O  ', end='')
            print('\n')
        print('\n')

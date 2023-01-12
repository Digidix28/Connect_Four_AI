import pickle

class TranspositionTable:

    def __init__(self) :
        self.hash_map = {}

    # Save the transposition table to a file
    def save_transposition_table(self):

        with open('transposition_table.pkl', 'wb') as f:
            pickle.dump(self.hash_map, f)

    # Load the transposition table from a file
    def load_transposition_table(self):

        try:
            with open("transposition_table.pkl", "rb") as f:
                self.hash_map = pickle.load(f)
        except EOFError:
            self.hash_map = {}
            self.save_transposition_table()
     


    def get_hash(self,board_state):

        return tuple(board_state.flatten())

    def store_best_move(self,board_state,best_move) :

        key = self.get_hash(board_state=board_state)
        if key not in self.hash_map:
            self.hash_map[key] = best_move
        return self.hash_map

    def get_best_move(self,board_state):

        key = self.get_hash(board_state=board_state)
        if key in self.hash_map:
            return self.hash_map[key]
        else :
            return None

    



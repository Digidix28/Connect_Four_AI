import argparse

from connect_four_game import ConnectFourGame
from my_player import *
from my_player2 import *
from my_player3 import *
from my_player4 import *
from transposition_table import TranspositionTable 
import time 
from random_player import random_player_


def play_game(player1, player2,algo1,algo2):
    # for i in range(100):
    #     print("c'est la game : ", i)
        game = ConnectFourGame()
        transposition_table = TranspositionTable()
        transposition_table.load_transposition_table()
        while True:
            # Display the current board state
            print(game.print_board())
            start_time = time.time()

            # Get the list of valid moves
            valid_moves = filter_valid_moves(game.get_valid_moves(game.current_player))
            print("Valid moves:", valid_moves)

            # Check if the game is over
            game_over, result = game.check_game_over(game.current_player)
            if game_over:
                transposition_table.save_transposition_table()
                if result == 1:
                    print("Player 1 wins!")
                elif result == -1:
                    print("Player 2 wins!")
                else:
                    print("It's a draw!")
                break

            # Player 1's turn
            if game.current_player == 1:
                # If player1 is human
                if player1 == "human":
                    # Get player 1's move
                    while True:
                        try:
                            move = int(input("Enter your move (column number): "))
                            if move < 0 or move >= game.column:
                                print("Invalid move. Enter a valid column number.")
                                continue
                            row = game.get_next_open_row(move)
                            if row is None:
                                print("Column is full. Enter a different column.")
                                continue
                            break
                        except ValueError:
                            print("Invalid input. Enter a valid column number.")
                # If player1 is AI
                elif player1 == "AI":
                    print("AI's turn...")
                    _, ai_move,transposition_table.hash_map = algo1(game.current_player, game,transposition_table,False)
                    transposition_table.save_transposition_table()
                    print("AI's move:", ai_move)
                    row, move = ai_move
                    end_time = time.time()
                    print("temps d'éxecution : ", end_time - start_time,"\n")

                else:
                    print("random's player turn... ")
                    row,move = random_player_(game.current_player, game,transposition_table)
                
                game.play_action((row, move))
                
            # Player 2's turn
            else:
                # If player2 is human
                if player2 == "human":
                    # Get player 2's move
                    while True:
                        try:
                            move = int(input("Enter your move (column number): "))
                            if move < 0 or move >= game.column:
                                print("Invalid move. Enter a valid column number.")
                                continue
                            row = game.get_next_open_row(move)
                            if row is None:
                                print("Column is full. Enter a different column.")
                                continue
                            break
                        except ValueError:
                            print("Invalid input. Enter a valid column number.")
                # If player2 is AI
                elif player2 == "AI":
                    print("AI's turn...")
                    print(transposition_table)
                    _, ai_move,transposition_table.hash_map = algo2(game.current_player, game,transposition_table,False)
                    transposition_table.save_transposition_table()
                    print("AI's move:", ai_move)
                    row, move = ai_move
                    end_time = time.time()
                    print("temps d'éxecution : ", end_time - start_time,"\n")

                else:
                    print("random's player turn... ")
                    row,move = random_player_(game.current_player, game,transposition_table)
                
                game.play_action((row, move))




if __name__ == "__main__":
    play_game("AI","AI",algo1=h_alphabeta_search3,algo2=h_alphabeta_search4)

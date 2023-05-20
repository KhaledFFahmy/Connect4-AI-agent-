from board import Board
import time
#import random

# GAME LINK
# http://kevinshannon.com/connect4/


def main():
    board = Board()

    time.sleep(5)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()
        # FOR DEBUG PURPOSES
        board.print_grid(game_board)
        print("*******************************************************************")
        column_to_select = board.minimax(game_board,1,float("-inf"),float("inf"),True)
        board.select_column(column_to_select)  # Random selection replaced
        time.sleep(5)


if __name__ == "__main__":
    main()

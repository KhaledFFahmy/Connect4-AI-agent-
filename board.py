from PIL import ImageGrab
import pyautogui
import random

# YOU MAY NEED TO CHANGE THESE VALUES BASED ON YOUR SCREEN SIZE
LEFT = 611
TOP = 250
RIGHT = 1320
BOTTOM = 870

EMPTY = 0
RED = 1
BLUE = 2


class Board:
    def __init__(self):
        self.board = [[EMPTY for i in range(7)] for j in range(6)]
    
    # The function print_grid takes in one parameter:
    # grid, which is a two-dimensional list representing the color values of the cells in the game board.
    def print_grid(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY:
                    print("*", end=" \t")
                elif grid[i][j] == RED:
                    print("R", end=" \t")
                elif grid[i][j] == BLUE:
                    print("B", end=" \t")
            print("\n")
    
    # The function _convert_grid_to_color takes in one parameter:
    # grid, which is a two-dimensional list representing the color values of the cells in the game board in the form of RGB tuples.
    def _convert_grid_to_color(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == (255, 255, 255):
                    grid[i][j] = EMPTY
                elif grid[i][j][0] > 200:
                    grid[i][j] = RED
                elif grid[i][j][0] > 50:
                    grid[i][j] = BLUE
        return grid
    
    # The function _get_grid_cordinates has no parameters and returns a list of tuples representing 
    # the screen coordinates of the top-left corner of each cell in the game board.
    def _get_grid_cordinates(self):
        startCord = (55, 55)
        cordArr = []
        for i in range(0, 7):
            for j in range(0, 6):
                x = startCord[0] + i * 100
                y = startCord[1] + j * 100
                cordArr.append((x, y))
        return cordArr

    # The function _transpose_grid takes in one parameter: grid, 
    # which is a two-dimensional list of integers representing the color values of the cells in the game board.
    def _transpose_grid(self, grid):
        return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    # The function _capture_image has no parameters and returns a cropped image of the game board, 
    # which is obtained by taking a screenshot of the entire screen and cropping it to include only the region where the game board is located.
    def _capture_image(self):
        image = ImageGrab.grab()
        cropedImage = image.crop((LEFT, TOP, RIGHT, BOTTOM))
        return cropedImage

    # The function _convert_image_to_grid takes one parameter:
    # image, which is a PIL Image object representing a screenshot of the game board.
    def _convert_image_to_grid(self, image):
        pixels = [[] for i in range(7)]
        i = 0
        for index, cord in enumerate(self._get_grid_cordinates()):
            pixel = image.getpixel(cord)
            if index % 6 == 0 and index != 0:
                i += 1
            pixels[i].append(pixel)
        return pixels

    # The function _get_grid has no parameters and returns a two-dimensional list representing the color values of the cells in the game board,
    # which is obtained by capturing a screenshot of the game board, 
    # converting it to a grid of color values, 
    # transposing the grid, and returning the resulting grid.
    def _get_grid(self):
        cropedImage = self._capture_image()
        pixels = self._convert_image_to_grid(cropedImage)
        # cropedImage.show()
        grid = self._transpose_grid(pixels)
        return grid

    # The function _check_if_game_end takes in one parameter: grid, 
    # which is a two-dimensional list representing the current state of the game board.
    def _check_if_game_end(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY and self.board[i][j] != EMPTY:
                    return True
        return False

    # The function get_game_grid has no parameters and returns a tuple containing two elements:
    # The first element is a two-dimensional list representing the color values of the cells in the game board.
    # The second element is a boolean value indicating whether the game has ended.
    def get_game_grid(self):
        game_grid = self._get_grid()
        new_grid = self._convert_grid_to_color(game_grid)
        is_game_end = self._check_if_game_end(new_grid)
        self.board = new_grid
        return (self.board, is_game_end)

    # The function available_moves takes in one parameter: grid, 
    # which is a two-dimensional list representing the current state of the game board.
    def available_moves(self, grid):
        moves = []
        for i in range(7):
            if grid[0][i] == EMPTY:
                moves.append(i)
        return moves

    # The function make_move takes in three parameters: grid, move, and player. 
    # grid is a two-dimensional list representing the current state of the game board, 
    # move is an integer representing the column index where the player wants to drop their token, 
    # and player is an integer or a character representing the player's token color.
    def make_move(self, grid, move, player):
        for i in range(5, -1, -1):
            if grid[i][move] == EMPTY:
                grid[i][move] = player
                break

    # The function undo_move takes in two parameters: grid and move. 
    # grid is a two-dimensional list representing the current state of the game board, 
    # and move is an integer representing the column index where the last token was dropped.
    def undo_move(self, grid, move):
        for i in range(6):
            if grid[i][move] != EMPTY:
                grid[i][move] = EMPTY
                break

    # The function evaluate_window takes two parameters:
    # window, which is a list of four tokens representing a window of cells in the game board.
    # player, which is a string representing the color of the token of the current player.
    def evaluate_window(self, window, player):
        score = 0
        opponent = RED if player == BLUE else BLUE
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(EMPTY) == 2:
            score += 2
        if window.count(opponent) == 3 and window.count(EMPTY) == 1:
            score -= 4
        return score

    def score_position(self, grid, player):
        score = 0

        # Score center column
        center_array = [grid[i][3] for i in range(6)]
        center_count = center_array.count(player)
        score += center_count * 3

        # Score horizontal
        for row in range(6):
            for col in range(4):
                window = grid[row][col:col + 4]
                score += self.evaluate_window(window, player)

        # Score vertical
        for col in range(7):
            for row in range(3):
                window = [grid[row + i][col] for i in range(4)]
                score += self.evaluate_window(window, player)

        # Score positive diagonal
        for row in range(3):
            for col in range(4):
                window = [grid[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # Score negative diagonal
        for row in range(3):
            for col in range(4):
                window = [grid[row + 3 - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score

    # MinMax Algorithm 
        def minimax(self, grid, depth, alpha, beta, maximizing_player):
            valid_moves = self.available_moves(grid)
            game_end = self._check_if_game_end(grid)

            if depth == 0 or game_end:
                if game_end:
                    if self.score_position(grid, BLUE) == 0:
                        return 0, None
                    elif maximizing_player:
                        return -10000, None
                    else:
                        return 10000, None
                else:
                    return self.score_position(grid, BLUE), None

            if maximizing_player:
                max_eval = float('-inf')
                best_move = None
                for move in valid_moves:
                    self.make_move(grid, move, BLUE)
                    eval, _ = self.minimax(grid, depth - 1, alpha, beta, False)
                    self.undo_move(grid, move)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return best_move
            else:
                min_eval = float('inf')
                best_move = None
                for move in valid_moves:
                    self.make_move(grid, move, RED)
                    eval, _ = self.minimax(grid, depth - 1, alpha, beta, True)
                    self.undo_move(grid, move)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return best_move
			
	# The function select_column takes in one parameter:
    # column, which is an integer representing the index of the column where the player wants to drop their token.		
    def select_column(self, column):
        pyautogui.click(
            self._get_grid_cordinates()[column][0] + LEFT,
            self._get_grid_cordinates()[column][1] + TOP,
        )

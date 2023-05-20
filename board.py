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

    def _get_grid_cordinates(self):
        startCord = (55, 55)
        cordArr = []
        for i in range(0, 7):
            for j in range(0, 6):
                x = startCord[0] + i * 100
                y = startCord[1] + j * 100
                cordArr.append((x, y))
        return cordArr

    def _transpose_grid(self, grid):
        return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    def _capture_image(self):
        image = ImageGrab.grab()
        cropedImage = image.crop((LEFT, TOP, RIGHT, BOTTOM))
        return cropedImage

    def _convert_image_to_grid(self, image):
        pixels = [[] for i in range(7)]
        i = 0
        for index, cord in enumerate(self._get_grid_cordinates()):
            pixel = image.getpixel(cord)
            if index % 6 == 0 and index != 0:
                i += 1
            pixels[i].append(pixel)
        return pixels

    def _get_grid(self):
        cropedImage = self._capture_image()
        pixels = self._convert_image_to_grid(cropedImage)
        # cropedImage.show()
        grid = self._transpose_grid(pixels)
        return grid

    def _check_if_game_end(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY and self.board[i][j] != EMPTY:
                    return True
        return False

    def get_game_grid(self):
        game_grid = self._get_grid()
        new_grid = self._convert_grid_to_color(game_grid)
        is_game_end = self._check_if_game_end(new_grid)
        self.board = new_grid
        return (self.board, is_game_end)

    def available_moves(self, grid):
        moves = []
        for i in range(7):
            if grid[0][i] == EMPTY:
                moves.append(i)
        return moves

    def make_move(self, grid, move, player):
        for i in range(5, -1, -1):
            if grid[i][move] == EMPTY:
                grid[i][move] = player
                break

    def undo_move(self, grid, move):
        for i in range(6):
            if grid[i][move] != EMPTY:
                grid[i][move] = EMPTY
                break

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
            return  best_move
			
			
    def select_column(self, column):
        pyautogui.click(
            self._get_grid_cordinates()[column][0] + LEFT,
            self._get_grid_cordinates()[column][1] + TOP,
        )

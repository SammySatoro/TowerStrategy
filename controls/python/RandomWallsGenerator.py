import random

class RandomWallsGenerator:
    def __init__(self):
        self._all_wall_coordinates = []
        self._wall_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self._board = []

    def generate(self):
        self._all_wall_coordinates = []
        self._board = self._create_empty_board()
        for wall_size in self._wall_sizes:
            wall_coords = self._generate_random_wall_coords(wall_size)
            self._all_wall_coordinates.append(wall_coords)
    def get_all_wall_coordinates(self):
        return self._all_wall_coordinates
    def _create_empty_board(self):
        return [['O' for _ in range(10)] for _ in range(10)]

    def _is_valid_location(self, wall_coords):
        rows, cols = len(self._board), len(self._board[0])

        for row, col in wall_coords:
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    r, c = row + dr, col + dc
                    if 0 <= r < rows and 0 <= c < cols and self._board[r][c] == 'S':
                        return False
        return True


    def _generate_random_wall_coords(self, wall_size):
        rows, cols = len(self._board), len(self._board[0])
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, rows - 1)
                col = random.randint(0, cols - wall_size)
                wall_coords = [(row, col + i) for i in range(wall_size)]
            else:
                row = random.randint(0, rows - wall_size)
                col = random.randint(0, cols - 1)
                wall_coords = [(row + i, col) for i in range(wall_size)]

            if self._is_valid_location(wall_coords):
                self._place_ship(wall_coords)
                return wall_coords

    def _place_ship(self, coords):
        for row, col in coords:
            self._board[row][col] = 'S'


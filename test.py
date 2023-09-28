import random


def create_empty_board():
    return [['O' for _ in range(10)] for _ in range(10)]


def is_valid_location(board, ship_coords):
    # Check if the ship can be placed at the given coordinates
    rows, cols = len(board), len(board[0])

    for row, col in ship_coords:
        # Check if the ship goes out of bounds
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return False

        # Check if any ship is already present in the neighboring cells
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = row + dr, col + dc
                if 0 <= r < rows and 0 <= c < cols and board[r][c] == 'S':
                    return False

    return True


def generate_random_ship_coords(board, ship_size):
    rows, cols = len(board), len(board[0])
    while True:
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - ship_size)
            ship_coords = [(row, col + i) for i in range(ship_size)]
        else:
            row = random.randint(0, rows - ship_size)
            col = random.randint(0, cols - 1)
            ship_coords = [(row + i, col) for i in range(ship_size)]

        if is_valid_location(board, ship_coords):
            return ship_coords


def place_ship(board, ship_coords):
    for row, col in ship_coords:
        board[row][col] = 'S'

all_ship_coordinates = []

def main():
    board = create_empty_board()
    ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


    for ship_size in ship_sizes:
        ship_coords = generate_random_ship_coords(board, ship_size)
        place_ship(board, ship_coords)
        all_ship_coordinates.append(ship_coords)

    # Print the coordinates of each ship
    # for i, ship_coords in enumerate(all_ship_coordinates):
    #     print(ship_coords)


if __name__ == "__main__":
    main()

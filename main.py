import sys

from pyswip import Prolog
from PyQt6.QtWidgets import QApplication

from controls.python.MainController import MainController


def main():
    app = QApplication(sys.argv)
    menu_window = MainController()
    menu_window.show()
    sys.exit(app.exec())


def test():
    prolog = Prolog()
    prolog.consult("file.pl")

    matrix1 = [[0, 1, 0, 1, 2, 1, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[1, 3, 0, 0, 0, 0, 0, 1, 1, 0],[1, 3, 0, 2, 0, 0, 0, 0, 0, 0],[0, 0, 0, 1, 1, 0, 0, 0, 0, 0],[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 1, 0, 1, 0, 0, 0, 0],[0, 0, 0, 1, 0, 1, 0, 0, 0, 0],[0, 1, 0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    matrix2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    cells = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [0, 1], [1, 1], [2, 1],
        [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2],
        [7, 2], [8, 2], [9, 2], [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3], [0, 4],
        [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5],
        [5, 5], [6, 5], [7, 5], [8, 5], [9, 5], [0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6], [8, 6],
        [9, 6], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7], [8, 7], [9, 7], [0, 8], [1, 8], [2, 8],
        [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8], [0, 9], [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9],
        [7, 9], [8, 9], [9, 9]]

    prolog.assertz(f"cells({cells})")
    prolog.assertz(f"matrix({matrix1})")

    # solution = list(prolog.query("random_cell(Cell)"))
    # print(solution)
    # solution_for_prolog = [solution[0]['Cell'][0], solution[0]['Cell'][1]]
    # list(prolog.query(f"remove_value_from_cells({solution[0]['Cell']})"))
    # cells.remove(solution[0]['Cell'])
    #
    # # new_matrix = list(prolog.query(f"update_matrix_item({matrix1}, {solution_for_prolog}, 1, NewMatrix)"))[0]["NewMatrix"]
    # value = list(prolog.query(f"get_matrix_value({matrix1}, {solution_for_prolog}, Value)"))[0]["Value"]
    # print(value)
    for row in matrix1:
        for item in row:
            print(item, end=" ")
        print()

    lm = list(prolog.query(f"test([3,0], Data)"))
    # lm2 = list(prolog.query(f"test([1,2], Data)"))
    # lm3 = list(prolog.query(f"test([0,3], Data)"))
    # lm4 = list(prolog.query(f"test([0,2], Data)"))

    print(lm)
    # print(lm2)
    # print(lm3)
    # print(lm4)
    print(list(prolog.query("current_wall_cells(X)")))



if __name__ == '__main__':
    test()

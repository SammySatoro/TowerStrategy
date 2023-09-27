import sys

from pyswip import Prolog
from PyQt6.QtWidgets import QApplication

from controls.python.MainController import MainController


def main():
    app = QApplication(sys.argv)
    menu_window = MainController()
    menu_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()







def test():
    # Create a Prolog instance
    prolog = Prolog()

    # Load the Prolog file
    prolog.consult("file.pl")

    # Pass the matrix and K as arguments to the Prolog program and get the shifted matrix
    query = "sum_of_digits(123454321, Sum)"
    result = list(prolog.query(query))

    for i in result:
        print(i["Sum"])
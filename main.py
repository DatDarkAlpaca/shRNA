import sys

from PySide6.QtWidgets import QApplication
from ui.implemented.shrna_window import ShRNAWindow


def main():
    app = QApplication()

    window = ShRNAWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()

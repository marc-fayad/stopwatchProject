from controller import *


def main():
    app = QApplication([])
    window = Controller()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()

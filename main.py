import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
import tanks


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Tank\'s menu')
        self.show_background()

        self.btn_start = QPushButton('Играть', self)
        self.btn_start.resize(100, 100)
        self.btn_start.move(100, 100)
        self.btn_start.clicked.connect(self.start)

        self.btn_exit = QPushButton('Выйти', self)
        self.btn_exit.resize(100, 100)
        self.btn_exit.move(100, 200)
        self.btn_exit.clicked.connect(self.exit)

        self.show()

    def start(self):
        self.level_menu = LevelMenu()
        self.level_menu.show()

    def exit(self):
        self.close()
        sys.exit(app.exec())

    def show_background(self):
        self.label = QLabel(self)
        self.label.setText('')
        self.label.resize(500, 500)
        self.label.move(0, 0)
        self.label.setStyleSheet(
            "background-image: url(data/back.jpg); background-attachment: fixed; background-color: red; background-position: center")


class LevelMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Tank\'s menu')
        self.show_background()

        self.btn_level_1 = QPushButton('Уровень 1', self)
        self.btn_level_1.resize(100, 100)
        self.btn_level_1.move(100, 100)
        self.btn_level_1.clicked.connect(self.run_level_1)

        self.btn_exit = QPushButton('Выйти', self)
        self.btn_exit.resize(100, 100)
        self.btn_exit.move(100, 200)
        self.btn_exit.clicked.connect(self.exit)

    def exit(self):
        self.close()

    def run_level_1(self):
        res = tanks.start_level_1(self)
        msgBox = QMessageBox()
        msgBox.setText("Вы пебедили" if res else 'Вы проиграли')
        msgBox.exec()

    def end(self):
        t = LevelMenu()
        t.show()

    def show_background(self):
        self.label = QLabel(self)
        self.label.setText('')
        self.label.resize(500, 500)
        self.label.move(0, 0)
        self.label.setStyleSheet(
            "background-image: url(data/back.jpg); background-attachment: fixed; background-color: red; background-position: center")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    sys.exit(app.exec())

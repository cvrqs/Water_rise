import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton

class Wplace(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Выбор места')

        self.leftTopButton= QPushButton(self)
        self.leftTopButton.setText("lt")
        self.leftTopButton.resize(100, 90)
        self.leftTopButton.move(0, 0)

        self.middleTopButton = QPushButton(self)
        self.middleTopButton.setText("mt")
        self.middleTopButton.resize(100, 90)
        self.middleTopButton.move(100, 0)

        self.rightTopButton = QPushButton(self)
        self.rightTopButton.setText("rt")
        self.rightTopButton.resize(100, 90)
        self.rightTopButton.move(200, 0)

        self.leftMiddleButton = QPushButton(self)
        self.leftMiddleButton.setText("lm")
        self.leftMiddleButton.resize(100, 90)
        self.leftMiddleButton.move(0, 100)

        self.midMiddleButton = QPushButton(self)
        self.midMiddleButton.setText("lt")
        self.midMiddleButton.resize(100, 90)
        self.midMiddleButton.move(100, 100)

        self.rightMiddleButton = QPushButton(self)
        self.rightMiddleButton.setText("rm")
        self.rightMiddleButton.resize(100, 90)
        self.rightMiddleButton.move(200, 100)

        self.leftDownButton = QPushButton(self)
        self.leftDownButton.setText("ld")
        self.leftDownButton.resize(100, 90)
        self.leftDownButton.move(0, 200)

        self.midDownButton = QPushButton(self)
        self.midDownButton.setText("rd")
        self.midDownButton.resize(100, 90)
        self.midDownButton.move(100, 200)

        self.rightDownButton = QPushButton(self)
        self.rightDownButton.setText("rd")
        self.rightDownButton.resize(100, 90)
        self.rightDownButton.move(200, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Wplace()
    ex.show()
    sys.exit(app.exec())

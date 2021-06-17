import sys
import os

from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class NewWorkoutWindow(QMainWindow):
    def __init__(self):
        super(NewWorkoutWindow, self).__init__()
        loadUi("new_design/new_workout.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewWorkoutWindow()
    window.show()
    sys.exit(app.exec_())
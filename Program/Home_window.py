import sys
import os

from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from My_profile import Profile
from Trainings_Manager import TrainingsManager


class HomeWindow(QMainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("new_design/new_interface.ui", self)
        self.my_profile = Profile()
        self.training_manager = TrainingsManager()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.my_profile.save_changes()
        self.training_manager.load_database()
        data = self.my_profile.load_data()
        self.curent_page = 0
        self.default_filling_values()
        self.filling_values(data)
        self.all_connection()


    def all_connection(self):
        # иконка скрыть
        self.wrap.clicked.connect(lambda: self.showMinimized())
        # иконка расширить или уменьшить
        self.maximize.clicked.connect(self.restore_or_maximize_window)
        # иконка закрыть
        self.close.clicked.connect(lambda: self.close())
        self.exit_btn.clicked.connect(lambda: self.close())
        # передвижение окна
        self.header_frame.mouseMoveEvent = self.moveWindow

        # Движение слайдера: общее движение и отдельное для каждой иконки
        self.open_left.clicked.connect(lambda: self.move_slider())
        self.my_profile_btn.clicked.connect(lambda: self.move_slider(0))
        self.workouts_btn.clicked.connect(lambda: self.move_slider(1))
        self.my_records_btn.clicked.connect(lambda: self.move_slider(2))
        self.connect_developers_btn.clicked.connect(lambda: self.move_slider(3))
        self.settings_btn.clicked.connect(lambda: self.move_slider(4))
        self.give_mark_btn.clicked.connect(lambda: self.move_slider(5))
        self.exit_2_btn.clicked.connect(lambda: self.move_slider())

        # Оценивание
        self.star1.clicked.connect(lambda: self.set_mark(1))
        self.star2.clicked.connect(lambda: self.set_mark(2))
        self.star3.clicked.connect(lambda: self.set_mark(3))
        self.star4.clicked.connect(lambda: self.set_mark(4))
        self.star5.clicked.connect(lambda: self.set_mark(5))

        # Кнопки для переключения страниц тренировок
        self.swipe_left.clicked.connect(self.move_left_page)
        self.swipe_right.clicked.connect(self.move_right_page)

    def move_left_page(self):
        if self.training_manager.is_page_exist(self.curent_page+1):
            self.swipe_left.setEnabled(False)
        else:
            self.swipe_left.setEnabled(True)
    def move_right_page(self):
        if self.training_manager.is_page_exist(self.curent_page - 1):
            self.swipe_right.setEnabled(False)
        else:
            self.swipe_right.setEnabled(True)

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize.setIcon(QtGui.QIcon('new_design/icons/maximize-2.svg'))
        else:
            self.showMaximized()
            self.maximize.setIcon(QtGui.QIcon('new_design/icons/minimize-2.svg'))

    def moveWindow(self, e):
        if not self.isMaximized():
            if e.buttons() == Qt.LeftButton:
                self.move(self.pos() + e.globalPos() - self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def default_filling_values(self):
        # изображжение по умолчанию
        pixmap = QtGui.QPixmap('source/default_photo.jpg')
        self.user_photo.setPixmap(pixmap)
        # основная информация (нет информации)
        self.user_name.setText("Нет имени")
        self.user_goal.setText("Нет цели")
        self.day_shot.setText("0 дней без пропусков")
        # оценка (0 звезд)
        self.set_mark(0)
        # кнопки свапа страниц (заблокированы)
        self.swipe_left.setEnabled(False)
        self.swipe_right.setEnabled(False)

    def filling_values(self, data):
        if os.path.exists('source/my_photo.jpg'):
            pixmap = QtGui.QPixmap('source/my_photo.jpg')
            self.user_photo.setPixmap(pixmap)
        if data['name'] is not None:
            self.user_name.setText(data['name'])
        if data['goal']['title'] is not None:
            self.user_goal.setText(data['goal']['title'])
        if data['nice_days'] is not None:
            self.day_shot.setText(data['nice_days'] + " дней без пропусков")
        if data['raiting_app'] != 0:
            self.set_mark(int(data['raiting_app']))

        self.update_trainings()

    def update_trainings(self):
        trainings_places = [[self.date1, self.time1, self.distance1],
                            [self.date2, self.time2, self.distance2],
                            [self.date3, self.time3, self.distance3],
                            [self.date4, self.time4, self.distance4]]
        training_values = self.training_manager.get_4_trainings()
        for training_place, training_value in zip(trainings_places, training_values):
            training_place[0].setText(training_value[0])
            training_place[1].setText(training_value[1])
            training_place[2].setText(training_value[2])
        if self.training_manager.get_n_page() > 1:
            self.swipe_left.setEnabled(True)
            self.swipe_right.setEnabled(True)

    def move_slider(self, number=5):
        self.toolBox.setCurrentIndex(number)
        width = self.slider_menu_container.width()
        if width == 0:
            newWidth = 200
            self.open_left.setIcon(QtGui.QIcon('new_design/icons/chevrons-left.svg'))
        else:
            newWidth = 0
            self.open_left.setIcon(QtGui.QIcon('new_design/icons/chevrons-right.svg'))
        self.animation1 = QPropertyAnimation(self.slider_menu_container, b"maximumWidth")
        self.animation1.setDuration(250)
        self.animation1.setStartValue(width)
        self.animation1.setEndValue(newWidth)
        self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation1.start()
        self.animation2 = QPropertyAnimation(self.icons, b"maximumWidth")
        self.animation2.setDuration(250)
        self.animation2.setStartValue(newWidth//5)
        self.animation2.setEndValue(width//5)
        self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation2.start()

    def set_mark(self, n_stars):
        stars = [self.star1, self.star2, self.star3, self.star4, self.star5]
        messages = [
            "Пожалуйста оцените наше приложение",
            "Спасибо за Вашу оценку! Мы будем работать над нашими ошибками",
            "Спасибо за Вашу оценку! Мы будем работать над нашими ошибками",
            "Спасибо за Вашу оценку! Мы рады, что вам нравится наше приложение",
            "Спасибо за Вашу оценку! Мы стараемся для Вас!",
            "Спасибо за Вашу оценку! Мы рады, что вы с нами!"
        ]
        for i in range(5, 0, -1):
            if n_stars >= i:
                stars[i-1].setIcon(QtGui.QIcon('new_design/icons/star-fill.svg'))
            else:
                stars[i - 1].setIcon(QtGui.QIcon('new_design/icons/star.svg'))
                self.thanks_for_raiting.setText(messages[i-1])
        if n_stars == 5:
            self.thanks_for_raiting.setText(messages[5])








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec_())

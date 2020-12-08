# -*- coding: utf-8 -*-

from PyQt5.QtCore import QRect, Qt, QCoreApplication, QMetaObject
from PyQt5.QtGui import QFont, QPixmap  # Импортируем специальные библиотеки
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QApplication  # ->
# Импортируем специальные библиотеки
from Code.Auth import AuthWindow  # Импортируем окно с авторизацией
from Code.Registration import RegistrationWindow  # Импортируем окно с регистрацией
from Code.ButtonsForWindow import MyBar  # Импортируем титульные кнопки
from Code.config import backgroundMain as bM  #
from Code.config import buttonAuth as bA
from Code.config import buttonRegistration as bR
# Импортируем настройки стилей
import sys
#  Импорт всех нужных библиотек, стилей


class Main_Auth(QWidget):  # Главное окно с которого начинается работа приложения,
    def __init__(self):  # Инициализация
        super(Main_Auth, self).__init__()  # Наследование от окна и его инициализация
        self.layout = QVBoxLayout()  # Создание лэйаута
        self.layout.addWidget(MyBar(self))  # Добавление специального класса в лэйаут
        self.setLayout(self.layout)  # Изменение лэйаута в основном окне
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setMinimumSize(800, 400)  # Изменение минимального размера окна
        self.resize(1080, 720)  # Изменение размера окна
        self.setWindowFlags(Qt.FramelessWindowHint)  # изменение конфига титульных кнопок
        self.pressing = False
        self.setupUi()  # вызов метода с основной работой

    def setupUi(self):  # Основной метод
        #  Все кнопки создаются по мере работы, а не в инициализации т.к. после инициализации кнопки не хотят работать
        self.font = QFont()  # Создаем объект шрифта
        self.font.setFamily("Roboto Light")  # Изменяем семейство шрифта
        self.font.setPointSize(22)  # Изменяем размер шрифта
        self.label = QLabel(self)  # Создаем лейбл(для фона)
        self.label.setGeometry(QRect(0, 0, 801, 571))  # ->
        # Изменяем его геометрию(отступ по x, отступ по y, размер по x, размер по y)
        self.label.setText("")  # Изменяем текст на пустою строчку
        self.label.setPixmap(QPixmap(bM))  # Загружаем фотографию
        self.label.setScaledContents(True)  # Изменяем(разрешаем) динамичное подстраивание фотографии под размер окна
        self.label.setObjectName("label")
        self.Auth = QPushButton(self)  # Создаем кнопку
        self.Auth.setText('Авторизация')  # Изменяем текст кнопки
        self.Auth.clicked.connect(self.showWindowAuth)  # Коннектим функцию с нажатием кнопки
        self.Auth.setFont(self.font)  # Изменяем шрифт текста в кнопке на объект который создавали ранее
        self.Auth.adjustSize()  # Позволяем кнопке подстроить свой размер по размеру объекта в нем(текст, фото)
        self.Auth.setStyleSheet(bA)  # Изменяем стили на написанные и импортированные заранее
        self.Auth.move(self.width() // 2 - self.Auth.width() // 2, self.height() // 2 - self.Auth.height() // 2)  # ->
        # Перемещаем кнопку в середину экрана
        self.Registration = QPushButton(self)  # Создаем кнопку
        self.Registration.clicked.connect(self.showWindowRegistration)  # Коннектим функцию с нажатием кнопки
        self.Registration.setText('Регистрация')  # Изменяем текст кнопки
        self.Registration.setFont(self.font)  # Изменяем шрифт текста в кнопке на объект который создавали ранее
        self.Registration.adjustSize()  # Позволяем кнопке подстроить свой размер по размеру объекта в нем(текст, фото)
        self.Registration.move(self.width() // 2 - self.Auth.width() // 2,
                               self.height() // 2 - self.Auth.height() // 2 + 80)  # ->
        # Перемещаем кнопку в середину экрана и смещаем не много ниже
        self.Registration.setStyleSheet(bR)  # Изменяем стили на написанные и импортированные заранее
        self.retranslateUi()  # Вызов специальной функции от qt  для переменовывания названий объектов
        QMetaObject.connectSlotsByName(self)  # Коннект сигналов к слотам по названиям ???WTF ----------------

    def retranslateUi(self):  # Специальная функция от qt для переименовывания названий объектов
        _translate = QCoreApplication.translate  # Экземпляр для работы с переименовыванием объектов
        self.setWindowTitle(_translate("", "Окно"))  # Изменение названия титульного окна

    def showWindowAuth(self):  # функция для показа окна авторизации
        self.Auth = AuthWindow(self)  # создаем объект для работы с окном из другого файла и инициализируем его
        self.Auth.show()  # отображаем окно

    def showWindowRegistration(self):  # функция для показа окна регистрации
        self.Registr = RegistrationWindow(self)  # ->
        # создаем объект для работы с окном из другого файла и инициализируем его
        self.Registr.show()  # отображаем окно


if __name__ == '__main__':  # Запускаем приложение
    app = QApplication(sys.argv)
    main = Main_Auth()
    main.show()
    sys.exit(app.exec_())

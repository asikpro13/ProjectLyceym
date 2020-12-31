# -*- coding: utf-8 -*-
from PyQt5.QtCore import QRect, Qt, QCoreApplication, QMetaObject
from PyQt5.QtGui import QFont, QPixmap  # Импортируем специальные библиотеки
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QApplication  # ->
# Импортируем специальные библиотеки
from Code.auth import AuthWindow  # Импортируем окно с авторизацией
from Code.registration import RegistrationWindow  # Импортируем окно с регистрацией
from Code.buttonsForWindow import MyBar  # Импортируем титульные кнопки
from Code.config import backgroundMain as bM  #
from Code.config import buttonAuth as bA
from Code.config import buttonRegistration as bR
# Импортируем настройки стилей
import sys
from DataBase.workFromDB import DB
#  Импорт всех нужных библиотек, стилей


class Main_Auth(QWidget):  # Главное окно с которого начинается работа приложения,
    def __init__(self):  # Инициализация
        self.AuthWind = 0
        self.RegistrWind = 0
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

        self.label = QLabel(self)  # Создаем лейбл(для фона)
        self.Auth = QPushButton(self)  # Создаем кнопку для авторизации
        self.Registration = QPushButton(self)  # Создаем кнопку для регистрации

        self.font = QFont()  # Создаем объект шрифта
        self.font.setFamily("Roboto Light")  # Изменяем семейство шрифта
        self.font.setPointSize(22)  # Изменяем размер шрифта

        self.db = DB()

        self.setupUi()  # вызов метода с основной работой

        self.Auth.clicked.connect(self.showWindowAuth)
        self.Registration.clicked.connect(self.showWindowRegistration)
        self.Registration.setStyleSheet(bR)  # Изменяем стили на написанные и импортированные заранее
        self.setWindowTitle("Окно")  # Изменение названия титульного окна

    def setupUi(self):  # Основной метод
        self.label.setGeometry(QRect(0, 0, 801, 571))
        self.label.setPixmap(QPixmap(bM))  # Загружаем фотографию
        self.label.setScaledContents(True)  # Изменяем(разрешаем) динамичное подстраивание фотографии под размер окна
        self.Auth.setText('Авторизация')  # Изменяем текст кнопки
        self.Auth.setFont(self.font)  # Изменяем шрифт текста в кнопке на объект который создавали ранее
        self.Auth.adjustSize()  # Позволяем кнопке подстроить свой размер по размеру объекта в нем(текст, фото)
        self.Auth.setStyleSheet(bA)  # Изменяем стили на написанные и импортированные заранее
        self.Auth.move(self.width() // 2 - self.Auth.width() // 2, self.height() // 2 - self.Auth.height() // 2)  # ->
        # Перемещаем кнопку в середину экрана
        self.Registration.setText('Регистрация')  # Изменяем текст кнопки
        self.Registration.setFont(self.font)  # Изменяем шрифт текста в кнопке на объект который создавали ранее
        self.Registration.adjustSize()  # Позволяем кнопке подстроить свой размер по размеру объекта в нем(текст, фото)
        self.Registration.move(self.width() // 2 - self.Auth.width() // 2,
                               self.height() // 2 - self.Auth.height() // 2 + 80)

    def showWindowAuth(self):  # функция для показа окна авторизации
        self.AuthWind = AuthWindow(self)
        self.AuthWind.show()

    def showWindowRegistration(self):  # функция для показа окна регистрации
        self.RegistrWind = RegistrationWindow(self)  # ->
        self.RegistrWind.show()
    # Объявляем функции для показа окон


if __name__ == '__main__':  # Запускаем приложение
    app = QApplication(sys.argv)
    main = Main_Auth()
    main.show()
    sys.exit(app.exec_())

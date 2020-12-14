# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFrame, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from Code.Shop import shopWindow
# Импортируем специальные библиотеки
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import DB
# Импортируем настройки стилей


class RegistrationWindow(QDialog):  # Окно для регистрации
    def __init__(self, root):  # Инициализация
        self.root = root  # Создаем экземпляр родительского окна
        self.font = root.font
        self.root.setEnabled(False)
        self.db = DB()
        super(RegistrationWindow, self).__init__()
        #  Наследуем все необходимые объекты
        self.setWindowTitle("Регистрация")  # Изменяем название титульного окна

        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        # Создание стиля титульных кнопок
        self.id = QLabel(self)
        self.labelLogin = QLabel(self)  # Создаем надпись логина
        self.labelRegistr = QLabel(self)  # Создаем надпись регистрации
        self.labelPassword = QLabel(self)  # Создаем надпись пароля
        self.labelWarRegistr = QLabel(self)  # Создаем надпись с предупреждением
        self.lineEditForLogin = QLineEdit(self)  # Создаем поле ввода для логина
        self.lineEditForPassword = QLineEdit(self)  # Создаем поле ввода для пароля
        self.buttonForRegistr = QPushButton(self)  # Создаем кнопку для регистрации
        self.setupUi()  # Вызываем метод с основной работой

        self.buttonForRegistr.clicked.connect(self.reg)  # Коннектим функцию с нажатием кнопки

    def setupUi(self):
        self.setFixedSize(400, 439)  # Изменяем размер окна при появлении

        self.id.setText('0')
        self.id.hide()
        #  id - Специальный объект который передается между окнами(1 - админ, 0 - пользователь)
        self.labelRegistr.setGeometry(QRect(self.width() // 2 - self.labelRegistr.width(), 10, 231, 151))
        self.labelRegistr.setFont(self.font)  # Изменяем шрифт текста
        self.labelRegistr.setFrameShadow(QFrame.Plain)  # Изменяем значение тени рамки
        self.labelRegistr.setText("Регистрация")  # Изменяем надпись регистрации

        self.labelLogin.setFont(self.font)  # Изменяем шрифт текста
        self.labelLogin.setGeometry(QRect(self.width() // 2 - self.labelLogin.width() // 2, 130, 151, 61))
        self.labelLogin.setText("Логин")

        self.labelPassword.setFont(self.font)  # Изменяем шрифт текста
        self.labelPassword.setGeometry(QRect(self.width() // 2 - self.labelPassword.width() // 2 - 5, 250, 151, 61))
        self.labelPassword.setText("Пароль")

        self.lineEditForLogin.setGeometry(QRect(60, 210, 270, 30))
        self.lineEditForLogin.returnPressed.connect(self.reg)

        self.lineEditForPassword.setGeometry(QRect(60, 320, 271, 30))
        self.lineEditForPassword.setEchoMode(QLineEdit.Password)  # Делаем так чтобы наш пароль был не виден
        self.lineEditForPassword.returnPressed.connect(self.reg)

        self.buttonForRegistr.resize(130, 30)  # Меняем размер кнопки
        self.buttonForRegistr.move(self.width() // 2 - self.buttonForRegistr.width() // 2, 370)  # Двигаем кнопку
        self.buttonForRegistr.setText("Зарегистрироваться")  # Изменяем надпись кнопки регистрации

    def reg(self):  # Функция регистрации пользователя
        result = self.db.checkUser(self.lineEditForLogin.text(), self.lineEditForPassword.text())
        if len(result) == 1:
            self.labelWarRegistr.setText('Такой пользователь уже существует')
        elif len(self.lineEditForPassword.text()) <= 6:
            self.labelWarRegistr.setText('Пароль слишком короткий')
        elif len(self.lineEditForLogin.text()) < 3:
            self.labelWarRegistr.setText('Логин слишком короткий')
        else:
            self.db.registrationUser(self.lineEditForLogin.text(), self.lineEditForPassword.text())
            self.close()
            self.root.close()
            # Закрываем рабочее и родительское окно
            self.shopWind()
            # Открываем магазин
        #  Проводим запрос на добавление юзера в бд только если проходят условия
        self.labelWarRegistr.adjustSize()
        self.labelWarRegistr.move(self.width() // 2 - self.labelWarRegistr.width() // 2, 20)
        #  Подгоняем и двигаем надпись на середину окна

    def closeEvent(self, event):  # Продолжение работы родительского окна при закрытии рабочего
        self.root.setEnabled(True)

    def shopWind(self):  # Показа окна с магазином
        self.Wind = shopWindow(self)
        self.Wind.show()

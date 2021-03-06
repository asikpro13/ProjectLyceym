# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Code.shop import shopWindow
from Code.buttonsForWindow import MyBar
from DataBase.workFromDB import DB
from PyQt5.QtGui import QFont


class AuthWindow(QDialog):  # Окно авторизации
    def __init__(self, root):  # Инициализация
        self.root = root
        self.root.setEnabled(False)
        self.db = self.root.db
        self.Wind = 0
        self.font = self.root.font
        #  Наследуем все необходимые объекты
        super(AuthWindow, self).__init__()

        self.setFixedSize(400, 439)
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        # Создание стиля титульных кнопок
        self.labelLogin = QLabel(self)  # Создаем надпись логина
        self.labelAuth = QLabel(self)  # Создаем надпись авторизации
        self.labelWarAuth = QLabel(self)  # Создаем надпись с предупреждением
        self.labelPassword = QLabel(self)  # Создаем надпись пароля
        self.lineEditForLoginAuth = QLineEdit(self)  # Создаем поле ввода для логина
        self.lineEditForPasswordAuth = QLineEdit(self)  # Создаем поле ввода для пароля
        self.buttonForAuth = QPushButton(self)  # Создаем кнопку для авторизации

        self.id = QLabel(self)
        self.login = QLabel(self)
        self.Auth()

        self.setWindowTitle("Авторизация")
        self.labelAuth.setText("Авторизация")
        self.labelLogin.setText("Логин")
        self.labelPassword.setText("Пароль")

    def Auth(self):  # Основной метод
        self.setWindowTitle('Авторизация')
        self.labelAuth.setGeometry(QRect(self.width() // 2 - self.labelAuth.width(), 10, 231, 151))
        # Изменяем размер надписи

        self.labelAuth.setFont(self.font)
        self.labelAuth.setFrameShadow(QFrame.Plain)
        self.labelLogin.setGeometry(QRect(self.width() // 2 - self.labelLogin.width() // 2, 130, 151, 61))
        self.labelPassword.setFont(self.font)
        self.labelPassword.setGeometry(QRect(self.width() // 2 - self.labelPassword.width() // 2 - 5, 250, 151, 61))
        self.labelLogin.setFont(self.font)
        self.lineEditForLoginAuth.setGeometry(QRect(60, 210, 270, 30))
        self.lineEditForLoginAuth.returnPressed.connect(self.check)
        self.buttonForAuth.clicked.connect(self.check)
        self.buttonForAuth.setText('Авторизироваться')
        self.lineEditForPasswordAuth.setGeometry(QRect(60, 320, 271, 30))
        self.lineEditForPasswordAuth.returnPressed.connect(self.check)
        self.lineEditForPasswordAuth.setEchoMode(QLineEdit.Password)
        self.buttonForAuth.resize(130, 30)
        self.buttonForAuth.move(self.width() // 2 - self.buttonForAuth.width() // 2, 370)
        # В основном методе изменемяем название окна, создаем надписи, меняем шрифт

    def check(self):  # Функция проверки
        result = self.db.auth(self.lineEditForLoginAuth.text(), self.lineEditForPasswordAuth.text())
        if len(result) > 0:
            self.root.close()
            self.id.setText(str(result[0][3]))
            self.login.setText(str(self.lineEditForLoginAuth.text()))
            self.shopWind()
            self.close()
            # Пропускаем
        else:
            self.labelWarAuth.setText('Такого пользователя или пароля не существует')
            self.font.setPointSize(8)
            self.labelWarAuth.setFont(self.font)
            self.labelWarAuth.adjustSize()
            self.labelWarAuth.setStyleSheet('color: red')
            self.labelWarAuth.move(self.width() // 2 - self.labelWarAuth.width() // 2, 190)
            self.labelWarAuth.show()
            # Выводим ошибку

    def shopWind(self):  # Функция дла показа окна с магазином
        self.Wind = shopWindow(self)
        self.Wind.show()

    def closeEvent(self, event):  # Макрос от pyqt срабатывающий при закрытии окна
        self.root.setEnabled(True)  # Говорим окну продолжить работу

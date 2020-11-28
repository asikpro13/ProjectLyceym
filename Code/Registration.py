# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFrame, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
# Импортируем специальные библиотеки
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import db
# Импортируем настройки стилей


class RegistrationWindow(QDialog):  # Окно для регистрации(можно сказать дочернее окно Main.py)
    def __init__(self, root):  # Инициализация
        self.root = root  # Создаем экземпляр родительского окна
        self.root.setEnabled(False)  # Делаем окно не активным
        super(RegistrationWindow, self).__init__()  # Инициализация
        self.layout = QVBoxLayout()  # Создание лэйаута
        self.layout.addWidget(MyBar(self))  # Добавление специального класса в лэйаут
        self.setLayout(self.layout)  # Изменение лэйаута в основном окне
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setWindowFlags(Qt.FramelessWindowHint)  # изменение конфига титульных кнопок
        self.pressing = False
        self.labelRegistr = QLabel(self)  # Создаем надпись регистрации
        self.labelWarRegistr = QLabel(self)  # Создаем надпись с предупреждением
        self.labelLogin = QLabel(self)  # Создаем надпись логина
        self.labelPassword = QLabel(self)  # Создаем надпись пароля
        self.lineEditForLogin = QLineEdit(self)  # Создаем поле ввода для логина
        self.lineEditForPassword = QLineEdit(self)  # Создаем поле ввода для пароля
        self.buttonForRegistr = QPushButton(self)  # Создаем кнопку для регистрации
        self.setupUi()  # Вызываем метод с основной работой
        # В данном случае проблем с созданием кнопок до работы с основной функцией не наблюдается

    def setupUi(self):
        self.setFixedSize(400, 439)  # Изменяем размер окна при появлении
        self.labelRegistr.setGeometry(QRect(self.width() // 2 - self.labelRegistr.width(), 10, 231, 151))  # ->
        # Изменяем геометрию(отступ по x, отступ по y, размер по x, размер по y) надписи регистрации
        self.font = QFont()  # Создаем объект шрифта
        self.font.setFamily("Roboto Light")  # Изменяем семейство шрифта
        self.font.setPointSize(22)  # Изменяем размер шрифта
        self.labelRegistr.setFont(self.font)  # Изменяем шрифт текста на объект шрифта который создавали ранее
        self.labelRegistr.setFrameShadow(QFrame.Plain)  # Изменяем значение тени рамки
        self.labelRegistr.setObjectName("label")
        self.labelLogin.setGeometry(QRect(self.width() // 2 - self.labelLogin.width() // 2, 130, 151, 61))  # ->
        # Изменяем геометрию(отступ по x, отступ по y, размер по x, размер по y) надписи логина
        self.labelPassword.setFont(self.font)
        self.labelPassword.setObjectName("label_2")
        self.labelPassword.setGeometry(QRect(self.width() // 2 - self.labelPassword.width() // 2 - 5, 250, 151, 61))
        # Изменяем геометрию(отступ по x, отступ по y, размер по x, размер по y) надписи пароля
        self.labelLogin.setFont(self.font)  # Изменяем шрифт текста на объект шрифта который создавали ранее
        self.labelLogin.setObjectName("label_3")
        self.lineEditForLogin.setGeometry(QRect(60, 210, 270, 30))  # ->
        # Изменяем геометрию(отступ по x, отступ по y, размер по x, размер по y) поля ввода логина
        self.lineEditForLogin.setObjectName("lineEdit")
        self.lineEditForPassword.setGeometry(QRect(60, 320, 271, 30))  # ->
        # Изменяем геометрию(отступ по x, отступ по y, размер по x, размер по y) поля ввода пароля
        self.lineEditForPassword.setObjectName("lineEdit_2")
        self.lineEditForPassword.setEchoMode(QLineEdit.Password)  # Делаем так чтобы наш пароль был не виден
        self.buttonForRegistr.resize(130, 30)  # Меняем размер кнопки
        self.buttonForRegistr.move(self.width() // 2 - self.buttonForRegistr.width() // 2, 370)  # Двигаем кнопку
        self.buttonForRegistr.clicked.connect(self.reg)  # Коннектим функцию с нажатием кнопки
        self.retranslateUi()  # Вызов специальной функции от qt  для переменовывания названий объектов
        QMetaObject.connectSlotsByName(self)  # Коннект сигналов к слотам по названиям ???WTF ----------------

    def reg(self):  # функция регистрации(работа с бд)
        result = db("select * from Auth where login = ? and password = ?", (self.lineEditForLogin.text(), self.lineEditForPassword.text(),))
        if len(result) == 1:
            self.labelWarRegistr.setText('Такой пользователь уже существует')
        elif len(self.lineEditForPassword.text()) <= 6:
            self.labelWarRegistr.setText('Длина пароля слишком маленькая')
        elif len(self.lineEditForLogin.text()) < 3:
            self.labelWarRegistr.setText('Логин не доступен')
        else:
            db('INSERT INTO Auth (login, password) VALUES (?, ?)', (self.lineEditForLogin.text(), self.lineEditForPassword.text(),))
            self.close()  # закрываем окно
        #  Проводим запрос на добавление юзера в бд только если проходят условия
        self.labelWarRegistr.adjustSize()  # ->
        # Позволяем кнопке подстроить свой размер по размеру объекта в нем(текст, фото)
        self.labelWarRegistr.move(self.width() // 2 - self.labelWarRegistr.width() // 2, 20)  # ->
        # Двигаем надпись предупреждения

    def closeEvent(self, Event):  # Внутренний макрос pyqt на закрытие окна
        self.root.setEnabled(True)  # Заставляем окно продолжить работу

    def retranslateUi(self):  # Специальная функция от qt для переименовывания названий объектов
        _translate = QCoreApplication.translate  # Экземпляр для работы с переименовыванием объектов
        self.setWindowTitle(_translate("Form", "Регистрация"))  # Изменяем название титульного окна
        self.labelRegistr.setText(_translate("", "Регистрация"))  # Изменяем надпись регистрации
        self.labelLogin.setText(_translate("", "Логин"))  # Изменяем надпись логина
        self.labelPassword.setText(_translate("", "Пароль"))  # Изменяем надпись пароля
        self.buttonForRegistr.setText(_translate("Form", "Зарегистрироваться"))  # Изменяем надпись кнопки регистрации

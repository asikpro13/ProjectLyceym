# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFrame, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
# Импортируем специальные библиотеки
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import db
# Импортируем настройки стилей


class RegistrationWindow(QDialog):
    def __init__(self, root):
        self.root = root
        self.root.setEnabled(False)
        super(RegistrationWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.labelRegistr = QLabel(self)
        self.labelWarRegistr = QLabel(self)
        self.labelLogin = QLabel(self)
        self.labelPassword = QLabel(self)
        self.lineEditForLogin = QLineEdit(self)
        self.lineEditForPassword = QLineEdit(self)
        self.buttonForRegistr = QPushButton(self)
        self.setupUi()

    def setupUi(self):
        self.setFixedSize(400, 439)
        self.labelRegistr.setGeometry(QRect(self.width() // 2 - self.labelRegistr.width(), 10, 231, 151))
        self.font = QFont()
        self.font.setFamily("Roboto Light")
        self.font.setPointSize(22)
        self.labelRegistr.setFont(self.font)
        self.labelRegistr.setFrameShadow(QFrame.Plain)
        self.labelRegistr.setObjectName("label")
        self.labelLogin.setGeometry(QRect(self.width() // 2 - self.labelLogin.width() // 2, 130, 151, 61))
        self.labelPassword.setFont(self.font)
        self.labelPassword.setObjectName("label_2")
        self.labelPassword.setGeometry(QRect(self.width() // 2 - self.labelPassword.width() // 2 - 5, 250, 151, 61))
        self.labelLogin.setFont(self.font)
        self.labelLogin.setObjectName("label_3")
        self.lineEditForLogin.setGeometry(QRect(60, 210, 270, 30))
        self.lineEditForLogin.setObjectName("lineEdit")
        self.lineEditForPassword.setGeometry(QRect(60, 320, 271, 30))
        self.lineEditForPassword.setObjectName("lineEdit_2")
        self.lineEditForPassword.setEchoMode(QLineEdit.Password)
        self.buttonForRegistr.resize(130, 30)
        self.buttonForRegistr.move(self.width() // 2 - self.buttonForRegistr.width() // 2, 370)
        self.buttonForRegistr.clicked.connect(self.reg)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def reg(self):
        result = db("select * from Auth where login = ? and password = ?", (self.lineEditForLogin.text(), self.lineEditForPassword.text(),))
        if len(result) == 1:
            self.labelWarRegistr.setText('Такой пользователь уже существует')
        elif len(self.lineEditForPassword.text()) <= 6:
            self.labelWarRegistr.setText('Длина пароля слишком маленькая')
        elif len(self.lineEditForLogin.text()) < 3:
            self.labelWarRegistr.setText('Логин не доступен')
        else:
            db('INSERT INTO Auth (login, password) VALUES (?, ?)', (self.lineEditForLogin.text(), self.lineEditForPassword.text(),))
            self.close()
        self.labelWarRegistr.adjustSize()
        self.labelWarRegistr.move(self.width() // 2 - self.labelWarRegistr.width() // 2, 20)

    def closeEvent(self, Event):
        self.root.setEnabled(True)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Регистрация"))
        self.labelRegistr.setText(_translate("", "Регистрация"))
        self.labelLogin.setText(_translate("", "Логин"))
        self.labelPassword.setText(_translate("", "Пароль"))
        self.buttonForRegistr.setText(_translate("Form", "Зарегистрироваться"))

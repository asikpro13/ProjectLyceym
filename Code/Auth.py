from PyQt5.QtWidgets import QDialog, QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Code.Shop import shopWindow
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import DB
from PyQt5.QtGui import QFont


class AuthWindow(QDialog):  # Окно авторизации
    def __init__(self, root):  # Инициализация
        self.root = root
        self.db = DB()
        self.root.setEnabled(False)
        super(AuthWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setMinimumSize(800, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.labelAuth = QLabel(self)
        self.labelWarAuth = QLabel(self)
        self.labelLogin = QLabel(self)
        self.labelPassword = QLabel(self)
        self.lineEditForLogin = QLineEdit(self)
        self.lineEditForPassword = QLineEdit(self)
        self.buttonForAuth = QPushButton(self)
        self.id = QLabel(self)
        self.setFixedSize(400, 439)
        self.Auth()
        #  Создаем объект дочернего окна, создаем кастомные титульные кнопки, создаем надписи, поля для ввода
        #  Изменяем размер окна и вызываем основной метод

    def Auth(self):  # Основной метод
        self.setWindowTitle('Авторизация')
        self.setObjectName("")
        self.labelAuth.setGeometry(QRect(self.width() // 2 - self.labelAuth.width(), 10, 231, 151))
        # Изменяем размер надписи
        self.font = QFont()
        self.font.setFamily("Roboto Light")
        self.font.setPointSize(22)
        self.labelAuth.setFont(self.font)
        self.labelAuth.setFrameShadow(QFrame.Plain)
        self.labelAuth.setObjectName("label")
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
        self.lineEditForPassword.returnPressed.connect(self.check)
        self.buttonForAuth.clicked.connect(self.check)
        self.buttonForAuth.setText('Авторизироваться')
        self.buttonForAuth.resize(130, 30)
        self.buttonForAuth.move(self.width() // 2 - self.buttonForAuth.width() // 2, 370)
        self.retranslateUi()
        # В основном методе изменемяем название окна, создаем надписи, меняем шрифт

    def check(self):  # Функция проверки
        result = self.db.auth(self.lineEditForLogin.text(), self.lineEditForPassword.text())
        if len(result) > 0:
            self.root.close()
            self.id.setText(str(result[0][-1]))
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

    def closeEvent(self, Event):  # Макрос от pyqt срабатывающий при закрытии окна
        self.root.setEnabled(True)  # Говорим окну продолжить работу

    def retranslateUi(self):  # Специальная функция от qt для переименовывания названий объектов
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("", "Авторизация"))
        self.labelAuth.setText(_translate("", "Авторизация"))
        self.labelLogin.setText(_translate("", "Логин"))
        self.labelPassword.setText(_translate("", "Пароль"))
    #  Изменяем текст в объетках по смыслу

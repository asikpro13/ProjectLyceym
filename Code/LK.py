from PyQt5 import QtCore, QtGui, QtWidgets
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import DB


class LK_window(QtWidgets.QDialog):
    def __init__(self, root):
        self.root = root
        self.db = DB()
        super(LK_window, self).__init__()
        self.login = root.login
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setMinimumSize(456, 456)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.pressing = False
        self.setupUi()
        self.updateStats()

    def setupUi(self):
        self.setObjectName("Form")
        stats = self.db.getStats(self.login)
        self.setEnabled(True)
        if self.root.id == "0":
            self.pix = QtGui.QPixmap('../Image/account_group_team_user_icon_127141 (1).png').scaled(150, 150)
        else:
            self.pix = QtGui.QPixmap('../Image/date.png').scaled(150, 150)
        self.userPhoto = QtWidgets.QLabel(self)
        self.userPhoto.move(int(self.width() * 0.05), 111 + 40)
        self.userPhoto.setPixmap(self.pix)
        self.userPhoto.resize(150, 150)
        self.userLogin = QtWidgets.QLabel(self)
        self.userLogin.setGeometry(QtCore.QRect(280, 50, 61, 21))
        self.userLogin.setText("Ваш логин:")
        self.purchases = QtWidgets.QLabel(self)
        self.purchases.setText("Совершено покупок:")
        self.purchases.adjustSize()
        self.purchases.move(self.userLogin.x() + self.userLogin.width() // 2 - self.purchases.width() // 2, 100)
        self.money = QtWidgets.QLabel(self)
        self.money.setText("Сумма которая была потрачена на покупки:")
        self.money.adjustSize()
        self.money.move(self.userLogin.x() + self.userLogin.width() // 2 - self.money.width() // 2, 155)
        self.counterProducts = QtWidgets.QLabel(self)
        self.counterProducts.setText("Количество купленного товара:")
        self.counterProducts.adjustSize()
        self.counterProducts.move(self.userLogin.x() + self.userLogin.width() // 2 - self.counterProducts.width() // 2, 200)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setText(str(stats[1]))
        self.label_6.adjustSize()
        self.label_6.move(self.userLogin.x() + self.userLogin.width() // 2 - self.label_6.width() // 2, 170)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setText(str(stats[0]))
        self.label_7.adjustSize()
        self.label_7.setGeometry(QtCore.QRect(280, 120, 51, 30))
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.adjustSize()
        self.label_8.move(self.userLogin.x() + self.userLogin.width() // 2 - self.label_8.width() // 2, 70)
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setText(self.login)
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setText(str(stats[2]))
        self.label_9.adjustSize()
        self.label_9.setGeometry(QtCore.QRect(280, 220, 51, 30))
        self.label_9.setFont(font)
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(270, 410, 160, 28))
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(20, 410, 140, 28))
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Статистика пользователя"))
        self.pushButton.setText(_translate("Form", "Назначить администратора"))

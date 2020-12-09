from PyQt5 import QtCore, QtGui, QtWidgets
from Code.ButtonsForWindow import MyBar


class LK_window(QtWidgets.QDialog):
    def __init__(self, root):
        self.root = root
        super(LK_window, self).__init__()
        self.setupUi()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setMinimumSize(456, 456)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.pressing = False

    def setupUi(self):
        self.setObjectName("Form")
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
        self.purchases = QtWidgets.QLabel(self)
        self.purchases.setGeometry(QtCore.QRect(250, 100, 120, 16))
        self.money = QtWidgets.QLabel(self)
        self.money.setGeometry(QtCore.QRect(200, 155, 230, 13))
        self.counterProducts = QtWidgets.QLabel(self)
        self.counterProducts.setGeometry(QtCore.QRect(230, 200, 171, 16))
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(280, 170, 51, 30))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(280, 120, 51, 30))
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(270, 70, 81, 30))
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(280, 220, 51, 30))
        self.label_9.setFont(font)
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setObjectName("label_9")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(270, 410, 160, 28))
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(20, 410, 140, 28))
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.userLogin.setText(_translate("Form", "Ваш логин:"))
        self.purchases.setText(_translate("Form", "Совершено покупок:"))
        self.money.setText(_translate("Form", "Сумма которая была потрачена на покупки:"))
        self.counterProducts.setText(_translate("Form", "Количество купленного товара:"))
        self.label_8.setText(_translate("Form", "asikpro13"))
        self.pushButton.setText(_translate("Form", "Назначить администратора"))

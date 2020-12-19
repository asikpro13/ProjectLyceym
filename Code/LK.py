from PyQt5 import QtCore, QtGui, QtWidgets
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import DB


class LK_window(QtWidgets.QDialog):
    def __init__(self, root):
        self.root = root
        self.id = root.id  # Получаем параметр админ/не админ от родительского окна
        self.db = self.root.db
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

        if self.id == '0':
            self.comboBox.hide()
            self.pushButton.hide()

        self.pushButton.clicked.connect(self.setAdmin)

    def setupUi(self):
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
        self.purchases.setText("Проведено транзакций:")
        self.purchases.adjustSize()
        self.purchases.move(self.userLogin.x() + self.userLogin.width() // 2 - self.purchases.width() // 2, 100)
        self.money = QtWidgets.QLabel(self)
        self.money.setText("Доход:")
        self.money.adjustSize()
        self.money.move(self.userLogin.x() + self.userLogin.width() // 2 - self.money.width() // 2, 155)
        self.counterProducts = QtWidgets.QLabel(self)
        self.counterProducts.setText("Количество купленного товара:")
        self.counterProducts.adjustSize()
        self.counterProducts.move(self.userLogin.x() + self.userLogin.width() // 2 - self.counterProducts.width() // 2,
                                  200)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.moneyValue = QtWidgets.QLabel(self)
        self.moneyValue.setText(str(stats[1]))
        self.moneyValue.adjustSize()
        self.moneyValue.resize(self.moneyValue.width() + 10, self.moneyValue.height())
        self.moneyValue.move(self.userLogin.x() + self.userLogin.width() // 2 - self.moneyValue.width() // 2, 170)
        self.moneyValue.setFont(font)
        self.moneyValue.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.purchasesValue = QtWidgets.QLabel(self)
        self.purchasesValue.setText(str(stats[0]))
        self.purchasesValue.adjustSize()
        self.purchasesValue.resize(self.purchasesValue.width() + 10, self.purchasesValue.height())
        self.purchasesValue.move(self.userLogin.x() + self.userLogin.width() // 2 - self.purchasesValue.width() // 2,
                                 120)
        self.purchasesValue.setFont(font)
        self.purchasesValue.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setText(self.login)
        self.label_8.setFont(font)
        self.label_8.adjustSize()
        self.label_8.move(self.userLogin.x() + self.userLogin.width() // 2 - self.label_8.width() // 2, 70)
        self.label_8.adjustSize()
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.counterProductsValue = QtWidgets.QLabel(self)
        self.counterProductsValue.setText(str(stats[2]))
        self.counterProductsValue.adjustSize()
        self.counterProductsValue.resize(self.counterProductsValue.width() + 10, self.counterProductsValue.height())

        self.counterProductsValue.move(self.userLogin.x() + self.userLogin.width() // 2 -
                                       self.counterProductsValue.width() // 2, 220)
        self.counterProductsValue.setFont(font)
        self.counterProductsValue.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox = QtWidgets.QComboBox(self)
        users = self.db.getUsers()
        for i in range(len(users)):
            self.comboBox.addItem(users[i][0])
        self.comboBox.setGeometry(QtCore.QRect(20, 410, 140, 28))
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(270, 410, 160, 28))
        self.retranslateUi()

    def setAdmin(self):
        self.db.setAdmin(self.comboBox.currentText())

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Статистика пользователя"))
        self.pushButton.setText(_translate("Form", "Назначить администратора"))

from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import DB


class DelWindow(QDialog):  # Окно авторизации
    def __init__(self, root):  # Инициализация
        self.root = root
        self.root.setEnabled(False)
        self.db = self.root.db
        super(DelWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setMinimumSize(288, 258)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False

        self.delProduct = QLabel(self)
        self.ok = QPushButton(self)
        self.cancel = QPushButton(self)

        self.delUI()

        self.ok.clicked.connect(self.delProduct)
        self.cancel.clicked.connect(self.close)
        #  Создаем объект дочернего окна, создаем кастомные титульные кнопки, создаем надписи, поля для ввода
        #  Изменяем размер окна и вызываем основной метод

    def delUI(self):  # Основной метод

        self.delProduct.setGeometry(QRect(60, 70, 181, 16))
        self.delProduct.setText("Вы точно хотите удалить товар?")

        self.ok.setGeometry(QRect(50, 160, 75, 23))
        self.ok.setText('Да')

        self.cancel.setGeometry(QRect(160, 160, 75, 23))
        self.cancel.setText('Нет')

    def delProduct(self):
        self.db.delProduct(self.root.tableWidget.item(self.root.r, 0).text())
        self.close()

    def closeEvent(self, event):  # Макрос от pyqt срабатывающий при закрытии окна
        self.root.setEnabled(True)  # Говорим окну продолжить работу
        self.root.updateTable()

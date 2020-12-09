from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import DB


class DelWindow(QDialog):  # Окно авторизации
    def __init__(self, root):  # Инициализация
        self.root = root
        self.root.setEnabled(False)
        self.db = DB()
        super(DelWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setMinimumSize(288, 258)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.delUI()
        #  Создаем объект дочернего окна, создаем кастомные титульные кнопки, создаем надписи, поля для ввода
        #  Изменяем размер окна и вызываем основной метод

    def delUI(self):  # Основной метод
        self.label = QLabel(self)
        self.label.setGeometry(QRect(60, 70, 181, 16))
        self.label.setObjectName("label")
        self.ok = QPushButton(self)
        self.ok.setGeometry(QRect(50, 160, 75, 23))
        self.ok.setObjectName("pushButton")
        self.ok.clicked.connect(self.delProduct)
        self.cancel = QPushButton(self)
        self.cancel.setGeometry(QRect(160, 160, 75, 23))
        self.cancel.setObjectName("pushButton_2")
        self.cancel.clicked.connect(self.close)
        self.retranslateUi()

    def delProduct(self):
        self.db.delProduct(self.root.tableWidget.item(self.root.r, 0).text())
        self.close()

    def closeEvent(self, Event):  # Макрос от pyqt срабатывающий при закрытии окна
        self.root.setEnabled(True)  # Говорим окну продолжить работу
        self.root.updateTable()

    def retranslateUi(self):  # Специальная функция от qt для переименовывания названий объектов
        _translate = QCoreApplication.translate
        self.label.setText(_translate("Form", "Вы точно хотите удалить товар?"))
        self.ok.setText('Да')
        self.cancel.setText('Нет')
    #  Изменяем текст в объетках по смыслу

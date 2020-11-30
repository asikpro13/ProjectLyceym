from PyQt5.QtWidgets import QDialog, QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Code.ButtonsForWindow import MyBar
from DataBase.workFromDB import db
from PyQt5.QtGui import QFont


class DelWindow(QDialog):  # Окно авторизации
    def __init__(self, root):  # Инициализация
        self.root = root
        self.root.setEnabled(False)
        super(DelWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.setMinimumSize(800, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.labelDel = QLabel(self)
        self.buttonForDeleteProduct = QPushButton(self)
        self.labelid = QLabel(self)
        self.lineForDeleteProduct = QLineEdit(self)
        self.labelWarAuth = QLabel(self)

        self.setFixedSize(400, 439)
        self.Del()
        #  Создаем объект дочернего окна, создаем кастомные титульные кнопки, создаем надписи, поля для ввода
        #  Изменяем размер окна и вызываем основной метод

    def Del(self):  # Основной метод
        self.setWindowTitle('Удаление товара')
        self.setObjectName("")
        self.font = QFont()
        self.font.setFamily("Roboto Light")
        self.font.setPointSize(22)
        self.labelDel.setFont(self.font)
        self.labelDel.setFrameShadow(QFrame.Plain)
        self.labelDel.setObjectName("label")
        self.buttonForDeleteProduct.clicked.connect(self.check)
        self.retranslateUi()
        self.labelid.setText('id товара')
        self.labelid.move(self.width() // 2 - self.lineForDeleteProduct.width() // 2 - 80, self.height() // 2)
        self.labelDel.move(self.width() // 2 - self.labelDel.width() // 2, 5)
        self.lineForDeleteProduct.move(self.width() // 2 - self.lineForDeleteProduct.width() // 2, self.height() // 2)
        self.buttonForDeleteProduct.move(self.width() // 2 - self.buttonForDeleteProduct.width() // 2, self.height() // 2 + 100)
        # В основном методе изменемяем название окна, создаем надписи, меняем шрифт

    def check(self):  # Функция проверки
        result = db("select * from product where product_id = ?",
                    (self.lineForDeleteProduct.text(),))
        if len(result) > 0:
            db('delete from product where product_id = ?', (self.lineForDeleteProduct.text(),))

            self.close()
            # Пропускаем
        else:
            self.labelWarAuth.setText('Такого товара не существует')
            self.font.setPointSize(8)
            self.labelWarAuth.setFont(self.font)
            self.labelWarAuth.adjustSize()
            self.labelWarAuth.setStyleSheet('color: red')
            self.labelWarAuth.move(self.width() // 2 - self.labelWarAuth.width() // 2, 190)
            self.labelWarAuth.show()
            # Выводим ошибку

    def closeEvent(self, Event):  # Макрос от pyqt срабатывающий при закрытии окна
        self.root.setEnabled(True)  # Говорим окну продолжить работу
        self.root.updateTable()

    def retranslateUi(self):  # Специальная функция от qt для переименовывания названий объектов
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("", "Удаление товара"))
        self.labelDel.setText(_translate("", "Удаление"))
        self.buttonForDeleteProduct.setText(_translate("", "Удалить"))
        self.labelDel.adjustSize()
    #  Изменяем текст в объетках по смыслу

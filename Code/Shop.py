# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from Code.DelProduct import DelWindow
from Code.AddProduct import addProductWindow
from DataBase.workFromDB import DB  # Импортируем работу с базой данных
#  Импорт всех нужных библиотек, стилей


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, root):
        self.root = root  # Создаем экземпляр родительского окна
        super(TableWidget, self).__init__(root)
        self.mouse_press = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            shopWindow.openDelProductWindow(self.root)
        super(TableWidget, self).mousePressEvent(event)


class shopWindow(QtWidgets.QWidget):
    def __init__(self, root):
        self.root = root  # Создаем экземпляр родительского окна
        self.id = root.id.text()  # Получаем параметр админ/не админ от родительского окна
        self.db = DB()
        super(shopWindow, self).__init__()
        self.resize(869, 746)  # Изменяем размер окна
        self.setMinimumWidth(self.width())  # Изменяем минимальную ширину окна
        self.setMinimumHeight(self.height())  # Изменяем минимальную высоту окна
        self.buttonForLK = QtWidgets.QPushButton(self)  # Создаем кнопку для личного кабинета
        self.buttonForAddProduct = QtWidgets.QPushButton(self)  # Создаем кнопку для добавления продукта(only admin)
        if self.id == '0':  # Если пользователь не админ то скрываем от него кнопки добавления и удаления продукта
            self.buttonForAddProduct.hide()
        self.buttonForCreateCheck = QtWidgets.QPushButton(self)  # Создаем кнопку для выписки чек
        self.lineEditForSearch = QtWidgets.QLineEdit(self)  # Создаем поле для поиска
        self.tableWidget = TableWidget(self)  # Создаем таблицу
        self.label = QtWidgets.QLabel(self)  # Создаем лейбл(для текста)
        self.warning = QtWidgets.QLabel(self)
        self.setupUi()  # Вызов метода с основной работой

    def setupUi(self):  # Основной метод
        #  Все кнопки создаются по мере работы, а не в инициализации т.к. после инициализации кнопки не хотят работать
        self.setObjectName("Form")
        self.buttonForLK.setGeometry(QtCore.QRect(730, 30, 120, 28))  # Изменяем геометрию кнопки для ЛК
        self.buttonForLK.setObjectName("pushButton")
        # self.buttonForLK.clicked.connect()  # Коннект функции к кнопке
        self.buttonForAddProduct.setGeometry(QtCore.QRect(20, 30, 131, 28))
        # Изменяем геометрию кнопки для создания продукта
        self.buttonForAddProduct.setObjectName("pushButton_2")
        self.buttonForAddProduct.clicked.connect(self.openAddProductWindow)
        # Изменяем геометрию кнопки для удаления продукта
        self.buttonForCreateCheck.setGeometry(QtCore.QRect(510, 30, 110, 28))
        # Изменяем геометрию кнопки для создания чека
        self.buttonForCreateCheck.setObjectName("pushButton_6")
        self.lineEditForSearch.setGeometry(QtCore.QRect(160, 80, 690, 22))
        #  Изменяем геометрию поля с поиском
        self.lineEditForSearch.setObjectName("lineEdit")
        self.lineEditForSearch.textChanged.connect(self.updateTable)
        self.tableWidget.setGeometry(QtCore.QRect(20, 110, 831, 621))
        #  Изменяем геометрию таблицы
        self.tableWidget.resize(831, 621)  # Изменяем размер таблицы
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)  # Очищаем все строки в таблице
        self.tableWidget.setColumnCount(7)  # Изменяем количество столбцов
        self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('ID'))
        self.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('ФОТО'))
        self.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('БРЕНД'))
        self.tableWidget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('НАЗВАНИЕ'))
        self.tableWidget.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('ЦЕНА'))
        self.tableWidget.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem('КОЛИЧЕСТВО'))
        self.tableWidget.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem('ТРЕБУЕТСЯ'))
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.cellPressed[int, int].connect(self.clickedRowColumn)

        self.warning.setText('Предупреждение')
        self.warning.move(self.width() // 2 - self.warning.width() // 2, 0)
        self.warning.hide()
        #  Изменяем названия столбцов
        self.font = QtGui.QFont()  # Создаем объект шрифта
        self.font.setFamily("Roboto Light")  # Изменяем семейство шрифта
        self.updateTable()  # Запускаем функцию обновления таблицы
        self.label.setGeometry(QtCore.QRect(30, 80, 120, 20))  # Изменяем геометрию надписи
        self.label.setObjectName("label")

        self.retranslateUi()  # Специальная функция от qt для переименовывания названий объектов
        self.buttonForCreateCheck.adjustSize()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):  # Специальная функция от qt для переименовывания названий объектов
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Касса"))
        self.buttonForLK.setText(_translate("Form", "Личный кабинет"))
        self.buttonForAddProduct.setText(_translate("Form", "Добавить продукт"))
        self.buttonForCreateCheck.setText(_translate("Form", "Совершить покупку"))
        self.label.setText(_translate("Form", "Поиск продукта:"))
    # Изменяем текст в объетках по смыслу

    def checkCount(self, row, column):
        if column >= 6:
            try:
                if int(self.tableWidget.item(row, column - 1).text()) < int(self.tableWidget.item(row, column).text()) \
                        or int(self.tableWidget.item(row, column).text()) < 0:
                    raise TypeError
                self.font.setBold(False)
                self.tableWidget.item(row, column).setFont(self.font)
                self.tableWidget.item(row, column).setForeground(QtGui.QColor(0, 0, 0))
                self.warning.hide()
                self.buttonForCreateCheck.setEnabled(True)
            except TypeError:
                self.font.setBold(True)  # Изменяем ширину шрифта
                self.warning.setText('Ошибка данных')
                self.tableWidget.item(row, column).setFont(self.font)
                self.tableWidget.item(row, column).setForeground(QtGui.QColor(255, 0, 0))
                self.buttonForCreateCheck.setEnabled(False)
                self.warning.show()
            except ValueError:
                self.font.setBold(True)  # Изменяем ширину шрифта
                self.warning.setText('Ошибка данных')
                self.tableWidget.item(row, column).setFont(self.font)
                self.tableWidget.item(row, column).setForeground(QtGui.QColor(255, 0, 0))
                self.buttonForCreateCheck.setEnabled(False)
                self.warning.show()
            except AttributeError:
                pass

    def openAddProductWindow(self):
        self.addWind = addProductWindow(self)
        self.addWind.show()

    def openDelProductWindow(self):
        self.delWind = DelWindow(self)  # создаем объект для работы с окном из другого файла и инициализируем его
        self.delWind.show()

    def clickedRowColumn(self, r, c):
        self.row = r
        self.column = c
        print("{}: row={}, column={}".format(self.tableWidget.mouse_press, r, c))

    def updateTable(self):
        self.tableWidget.setRowCount(0)
        request = self.lineEditForSearch.text()
        res = self.db.updateTableRequest(request)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                s = QTableWidgetItem(str(elem))
                if j == 1:
                    brush = QtGui.QBrush(QtGui.QPixmap(res[i][1]).scaled(200, 200))
                    self.tableWidget.setRowHeight(i, 200)
                    s.setText('')
                    s.setBackground(brush)
                if j == 0:
                    s.setFlags(QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(i, j, s)
            s = QTableWidgetItem('0')
            self.tableWidget.setItem(i, j + 1, s)

    def resizeEvent(self, Event):  # Макрос от pyqt срабатывающий при изменении ширины/длины окна
        self.tableWidget.resize(self.width() - (self.width() // 100 * 5), self.height() - (self.height() // 100 * 5) - self.tableWidget.y() + 20)
        self.tableWidget.move(self.width() // 2 - self.tableWidget.width() // 2, self.tableWidget.y())
        self.lineEditForSearch.resize(self.width() - (self.width() // 100 * 5) - 140, self.lineEditForSearch.height())
        self.lineEditForSearch.move(self.width() // 2 - self.lineEditForSearch.width() // 2 + 70, self.lineEditForSearch.y())
        self.warning.move(self.width() // 2 - self.warning.width() // 2, 0)
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from Code.DelProduct import DelWindow
from Code.AddProduct import addProductWindow
from Code.LK import LK_window
from DataBase.workFromDB import DB  # Импортируем работу с базой данных
#  Импорт всех нужных библиотек, стилей


class TableWidgetForTrans(QtWidgets.QTableWidget):
    def __init__(self, root):
        self.root = root
        super(TableWidgetForTrans, self).__init__(root)
        self.cellPressed[int, int].connect(self.root.clickedRow)

    def mouseDoubleClickEvent(self, event):
        super(TableWidgetForTrans, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            try:
                if self.root.c == 1:
                    self.root.tableWidgetForTrans.removeRow(self.root.r)
            except AttributeError:
                pass


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, root):
        self.root = root  # Создаем экземпляр родительского окна
        super(TableWidget, self).__init__(root)
        self.cellPressed[int, int].connect(self.root.clickedRow)

    def mousePressEvent(self, event):
        super(TableWidget, self).mousePressEvent(event)
        if self.root.id == '1':
            if event.button() == QtCore.Qt.RightButton:
                shopWindow.openDelProductWindow(self.root)
            elif event.button() == QtCore.Qt.LeftButton:
                try:
                    if self.root.c == 1:
                        self.fname, _ = QtWidgets.QFileDialog.\
                            getOpenFileName(self, 'Открыть изображение товара',
                                            filter='Файлы изображений (*.png *.jpg *.bmp)')
                        if self.fname != '':
                            product_id = self.root.tableWidget.item(self.root.r, 0).text()
                            self.root.db.updateProductPhoto(product_id, self.fname)
                            self.root.updateTable()
                    else:
                        self.edit(self.item(self.r, self.c).index)
                except AttributeError:
                    pass


class shopWindow(QtWidgets.QWidget):
    def __init__(self, root):
        self.root = root  # Создаем экземпляр родительского окна
        self.id = root.id.text()  # Получаем параметр админ/не админ от родительского окна
        self.login = root.login.text()
        self.column = 0
        self.r = 0
        self.listWarning = []
        self.db = self.root.db
        super(shopWindow, self).__init__()

        self.resize(1269, 746)  # Изменяем размер окна
        self.setMinimumWidth(self.width())  # Изменяем минимальную ширину окна
        self.setMinimumHeight(self.height())  # Изменяем минимальную высоту окна

        self.buttonForLK = QtWidgets.QPushButton(self)  # Создаем кнопку для личного кабинета
        self.buttonForAddProduct = QtWidgets.QPushButton(self)  # Создаем кнопку для добавления продукта(only admin)
        self.buttonForCreateTransaction = QtWidgets.QPushButton(self)  # Создаем кнопку для выписки чек
        self.buttonPurchases = QtWidgets.QPushButton(self)
        self.lineEditForSearch = QtWidgets.QLineEdit(self)  # Создаем поле для поиска
        self.tableWidget = TableWidget(self)  # Создаем таблицу
        self.tableWidgetForTrans = TableWidgetForTrans(self)
        self.label = QtWidgets.QLabel(self)  # Создаем лейбл(для текста)
        self.warning = QtWidgets.QLabel(self)
        self.font = QtGui.QFont()  # Создаем объект шрифта

        self.buttonForLK.clicked.connect(self.openLKWindow)
        self.buttonForCreateTransaction.clicked.connect(self.transaction)
        self.buttonForAddProduct.clicked.connect(self.openAddProductWindow)
        self.buttonPurchases.clicked.connect(self.buy)
        self.tableWidget.cellChanged.connect(self.updateProduct)
        self.lineEditForSearch.textChanged.connect(self.updateTable)

        self.setupUi()  # Вызов метода с основной работой

        if self.id == '0':  # Если пользователь не админ то скрываем от него кнопки добавления и удаления продукта
            self.buttonForAddProduct.hide()

        self.setWindowTitle("Касса")

    def setupUi(self):  # Основной метод
        self.buttonForLK.resize(120, 28)  # Изменяем геометрию кнопки для ЛК
        self.buttonForLK.setText("Личный кабинет")
        self.buttonForAddProduct.resize(131, 28)
        self.buttonForAddProduct.setText("Добавить продукт")
        # Изменяем геометрию кнопки для создания продукта
        self.buttonForCreateTransaction.resize(130, 28)
        self.buttonForCreateTransaction.setText("Провести транзакцию")
        self.buttonPurchases.setText('Купить')
        self.buttonPurchases.adjustSize()
        self.buttonPurchases.resize(self.buttonPurchases.width(), 30)
        self.lineEditForSearch.setGeometry(QtCore.QRect(160, 80, 690, 22))
        self.tableWidget.setGeometry(QtCore.QRect(20, 110, 831, 621))
        self.tableWidget.resize(self.width() - (self.width() // 100 * 5) - 400,
                                self.height() - (self.height() // 100 * 5) - self.tableWidget.y() + 20)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('ID'))
        self.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('ФОТО'))
        self.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('БРЕНД'))
        self.tableWidget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('НАЗВАНИЕ'))
        self.tableWidget.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('ЦЕНА'))
        self.tableWidget.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem('КОЛИЧЕСТВО'))
        self.tableWidget.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem('ТРЕБУЕТСЯ'))
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidgetForTrans.setColumnCount(2)
        self.tableWidgetForTrans.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('ТОВАР'))
        self.tableWidgetForTrans.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('УДАЛИТЬ'))
        self.tableWidgetForTrans.move(self.tableWidget.x(), self.tableWidget.y())
        self.tableWidgetForTrans.setColumnWidth(0, 200)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.buttonPurchases.move(self.tableWidgetForTrans.width() // 2 + self.tableWidgetForTrans.x(), 30)
        self.buttonForAddProduct.move(self.tableWidget.x(), 30)
        self.buttonForLK.move(self.tableWidget.x() + self.tableWidget.width() - self.buttonForLK.width(), 30)
        self.warning.setText('Предупреждение')
        self.warning.move(self.width() // 2 - self.warning.width() // 2, 0)
        self.warning.hide()
        self.label.setText("Поиск продукта:")
        self.font.setFamily("Roboto Light")  # Изменяем семейство шрифта
        self.updateTable()  # Запускаем функцию обновления таблицы
        self.checkError()

    def checkCount(self, row, column):
        if column >= 6:
            try:
                if int(self.tableWidget.item(row, column - 1).text()) < int(self.tableWidget.item(row, column).text()) \
                        or int(self.tableWidget.item(row, column).text()) < 0:
                    raise TypeError
            except TypeError:
                self.showError(row, column)
            except ValueError:
                self.showError(row, column)
            except AttributeError:
                pass

    def showError(self, row, column):
        try:
            if column == 6 or column == 5:
                count = 0
                self.tableWidget.blockSignals(True)
                self.checkError()
                for i in range(len(self.listWarning)):
                    if int(self.tableWidget.item(self.listWarning[i - count][0],
                                                 self.listWarning[i - count][1] - 1).text()) < int(
                            self.tableWidget.item(self.listWarning[i - count][0],
                                                  self.listWarning[i - count][1]).text()) \
                            or int(self.tableWidget.item(self.listWarning[i - count][0],
                                                         self.listWarning[i - count][1]).text()) < 0:
                        self.font.setBold(True)  # Изменяем ширину шрифта
                        self.warning.setText('Ошибка данных')
                        self.tableWidget.item(self.listWarning[i - count][0],
                                              self.listWarning[i - count][1]).setForeground(QtGui.QColor(255, 0, 0))
                        self.buttonForCreateTransaction.setEnabled(False)
                        self.warning.show()
                    else:
                        self.font.setBold(False)
                        self.tableWidget.item(self.listWarning[i - count][0],
                                              self.listWarning[i - count][1]).setForeground(QtGui.QColor(0, 0, 0))
                        if i + 1 <= len(self.listWarning):
                            self.listWarning.pop(i - count)
                            count += 1
                if len(self.listWarning) == 0:
                    self.buttonForCreateTransaction.setEnabled(True)
                    self.warning.hide()
                self.tableWidget.blockSignals(False)
        except ValueError:
            self.font.setBold(True)  # Изменяем ширину шрифта
            self.warning.setText('Ошибка данных')
            self.tableWidget.item(row, column).setFont(self.font)
            self.tableWidget.item(row, column).setForeground(
                QtGui.QColor(255, 0, 0))
            self.buttonForCreateTransaction.setEnabled(False)
            self.warning.show()
            self.tableWidget.blockSignals(False)

    def openLKWindow(self):
        self.LK = LK_window(self)
        self.LK.show()

    def openAddProductWindow(self):
        self.addWind = addProductWindow(self)
        self.addWind.show()

    def openDelProductWindow(self):
        self.delWind = DelWindow(self)  # создаем объект для работы с окном из другого файла и инициализируем его
        self.delWind.show()

    def clickedRow(self, r, c):
        self.r = r
        self.c = c

    def updateTable(self):
        self.tableWidget.blockSignals(True)
        self.tableWidget.setRowCount(0)
        res = self.db.findTableRequest(self.lineEditForSearch.text())
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            self.tableWidget.blockSignals(True)
            for j, elem in enumerate(row):
                s = QTableWidgetItem(str(elem))
                self.clickedRow(i, j)
                if j == 1:
                    brush = QtGui.QBrush(QtGui.QPixmap(res[i][1]).scaled(200, 200))
                    self.tableWidget.setRowHeight(i, 200)
                    s.setText('')
                    s.setBackground(brush)
                elif j == 6:
                    self.tableWidget.setItem(i, j, s)
                    self.checkCount(self.r, self.c)
                    continue
                if self.id != '1':
                    if str(j) in '012345':
                        s.setFlags(QtCore.Qt.ItemIsEditable)
                else:
                    if str(j) in '0':
                        s.setFlags(QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(i, j, s)
        self.tableWidget.blockSignals(False)
        self.checkError()

    def checkError(self):
        for i in range(self.tableWidget.rowCount()):
            if int(self.tableWidget.item(i, 5).text()) < int(self.tableWidget.item(i, 6).text()) \
                    and [i, 6] not in self.listWarning:
                self.listWarning.append([i, 6])

    def updateProduct(self, row, column):
        self.showError(row, column)
        id_product = self.tableWidget.item(row, 0).text()
        brand = self.tableWidget.item(row, 2).text()
        name = self.tableWidget.item(row, 3).text()
        price = self.tableWidget.item(row, 4).text()
        count = self.tableWidget.item(row, 5).text()
        required = self.tableWidget.item(row, 6).text()
        self.db.updateProduct(id_product, brand, name, price, count, required)

    def transaction(self):
        spisok = []
        self.tableWidgetForTrans.setRowCount(0)
        result = self.db.getTransactions()
        for k in range(len(result)):
            name = result[k][2] + ' ' + result[k][3] + ' в количестве ' + str(result[k][6]) + ' по цене ' \
                   + str(result[k][6] * result[k][4])
            spisok.append((name, ''))
        for i, row in enumerate(spisok):
            self.tableWidgetForTrans.setRowCount(
                self.tableWidgetForTrans.rowCount() + 1)
            for j, elem in enumerate(row):
                s = QTableWidgetItem(str(elem))
                if str(j) in '0':
                    s.setFlags(QtCore.Qt.ItemIsEditable)
                self.tableWidgetForTrans.setItem(i, j, s)

    def buy(self):
        for i in range(self.tableWidgetForTrans.rowCount()):
            transactions = self.tableWidgetForTrans.item(i, 0).text().split(' ')
            self.db.buyProduct(transactions, self.login)
        self.tableWidgetForTrans.setRowCount(0)
        self.updateTable()

    def resizeEvent(self, event):  # Макрос от pyqt срабатывающий при изменении ширины/длины окна
        self.tableWidget.resize(self.width() - (self.width() // 100 * 5) - 400,
                                self.height() - (self.height() // 100 * 5) - self.tableWidget.y() + 20)
        self.tableWidget.move(self.width() // 2 - self.tableWidget.width() // 2 + 200, self.tableWidget.y())
        self.lineEditForSearch.resize(self.width() - (self.width() // 100 * 5) - 140 - 400,
                                      self.lineEditForSearch.height())
        self.lineEditForSearch.move(self.tableWidget.x() + 140,
                                    self.lineEditForSearch.y())
        self.warning.move(self.width() // 2 - self.warning.width() // 2, 0)
        self.buttonForAddProduct.move(self.tableWidget.x(), 30)
        self.buttonForLK.move(self.tableWidget.x() + self.tableWidget.width() - self.buttonForLK.width(), 30)
        self.buttonForCreateTransaction.move(self.width() // 2 - self.buttonForCreateTransaction.width() // 2 + 200, 30)
        self.label.setGeometry(QtCore.QRect(self.tableWidget.x(), 80, 120, 20))
        self.tableWidgetForTrans.resize(self.tableWidget.x() - 40, self.height() - (self.height() // 100 * 5) -
                                        self.tableWidget.y() + 20)
        self.tableWidgetForTrans.move(20, self.tableWidget.y())
        self.buttonPurchases.move(self.tableWidgetForTrans.width() // 2 - self.tableWidgetForTrans.x(), 30)

    def closeEvent(self, event):
        self.db.closeConnection()
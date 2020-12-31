# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from DataBase.workFromDB import DB


class addProductWindow(QtWidgets.QDialog):
    def __init__(self, root):
        self.root = root
        self.root.setEnabled(False)
        self.db = self.root.db
        super(addProductWindow, self).__init__()

        self.warning = QtWidgets.QLabel(self)
        self.fname = 0
        self.pixmap = 0
        self.addProductButton = QtWidgets.QPushButton(self)
        self.spinBoxCount = QtWidgets.QSpinBox(self)
        self.spinBoxPrice = QtWidgets.QSpinBox(self)
        self.addPhotoButton = QtWidgets.QPushButton(self)
        self.labelPhoto = QtWidgets.QLabel(self)
        self.labelBrand = QtWidgets.QLabel(self)
        self.lineEditBrand = QtWidgets.QLineEdit(self)
        self.lineEditModel = QtWidgets.QLineEdit(self)
        self.labelModel = QtWidgets.QLabel(self)
        self.labelPrice = QtWidgets.QLabel(self)
        self.labelCount = QtWidgets.QLabel(self)
        self.labelAddProduct = QtWidgets.QLabel(self)
        self.setupUi()

        self.setWindowTitle("Добавление продукта")
        self.addProductButton.setText("Создать")
        self.labelBrand.setText("Бренд")
        self.labelModel.setText("Модель")
        self.labelPrice.setText("Цена")
        self.labelCount.setText("Количество")
        self.labelAddProduct.setText("Создание товара")
        self.addPhotoButton.setText("добавить фото")

    def setupUi(self):
        self.resize(380, 499)
        self.addProductButton.setGeometry(QtCore.QRect(130, 450, 93, 28))
        self.addProductButton.clicked.connect(self.createProduct)
        self.warning.setText('Ошибка')
        self.warning.hide()
        self.warning.move(self.width() // 2 - self.warning.width() // 2, 5)
        self.labelBrand.setGeometry(QtCore.QRect(70, 280, 55, 16))
        self.lineEditBrand.setGeometry(QtCore.QRect(150, 280, 141, 22))
        self.lineEditModel.setGeometry(QtCore.QRect(150, 320, 140, 22))
        self.labelModel.setGeometry(QtCore.QRect(70, 320, 50, 20))
        self.labelPrice.setGeometry(QtCore.QRect(70, 360, 55, 16))
        self.labelCount.setGeometry(QtCore.QRect(70, 400, 80, 16))
        self.labelAddProduct.setGeometry(QtCore.QRect(80, 0, 241, 60))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.labelAddProduct.setFont(font)
        self.addPhotoButton.setGeometry(QtCore.QRect(190, 100, 150, 150))
        self.addPhotoButton.setStyleSheet("QPushButton{\n"
                                          "border-style: solid;\n"
                                          "border-width: 1px;\n"
                                          "border-radius: 75%;\n"
                                          "border-color: red;}\n"
                                          "QPushButton:pressed{\n"
                                          "background-color: rgb(200, 200, 200);}")
        self.addPhotoButton.clicked.connect(self.addPhoto)
        self.spinBoxCount.setGeometry(QtCore.QRect(150, 400, 141, 22))
        self.spinBoxCount.setMinimum(1)
        self.spinBoxCount.setMaximum(1000000000)
        self.spinBoxPrice.setGeometry(QtCore.QRect(150, 360, 141, 22))
        self.spinBoxPrice.setMaximum(1000000000)

    def addPhoto(self):  # Добавление фото
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть изображение товара',
                                                              filter='Файлы изображений (*.png *.jpg *.bmp)')
        self.labelPhoto.move(20, 70)
        self.pixmap = QtGui.QPixmap(self.fname)
        self.pixmap = self.pixmap.scaled(QtCore.QSize(150, 200))
        self.labelPhoto.resize(150, 200)
        self.labelPhoto.setPixmap(self.pixmap)

    def createProduct(self):  # Создание продукта(если продукт не создается то отображается предупреждение)
        try:
            self.db.addProduct(self.fname, self.lineEditBrand.text(), self.lineEditModel.text(),
                               self.spinBoxPrice.text(), self.spinBoxCount.text())
            self.close()
        except FileNotFoundError:
            self.warning.show()
        except AttributeError:
            self.warning.show()

    def closeEvent(self, event):  # Макрос от pyqt срабатывающий при закрытии окна
        self.root.setEnabled(True)  # Говорим окну продолжить работу
        self.root.updateTable()

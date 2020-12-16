import sqlite3
import os
#  Импорт всех нужных библиотек, стилей
import shutil


class DB:
    def __init__(self):
        self.connect = sqlite3.connect('../DataBase/auth.db')  # Создаем соединение
        self.cur = self.connect.cursor()  # Создаем курсор

    def addProduct(self, path, brand, model, price, count):  # Функция для работы с базой данных.
        self.savePhoto(path)
        name = '../Image/DBImage/' + path[path.rfind('/') + 1:]
        self.cur.execute('INSERT INTO product (product_photo, product_brand, product_name, product_price,'
                         ' product_count, product_required) VALUES (?, ?, ?, ?, ?, ?)',
                         (name, brand, model, price, count, 0, ))
        self.commitConnection()
        # Проводим запрос

    def delProduct(self, product_id):
        result = self.cur.execute('select product_photo from product where product_id = ?', (product_id,)).fetchone()
        result = self.cur.execute('select product_photo from product where product_photo = ?', (result[0],)).fetchall()
        try:
            if len(result) == 1:
                self.delPhoto(product_id)
        except FileNotFoundError:
            pass
        self.cur.execute('delete from product where product_id = ?', (product_id,))
        self.commitConnection()

    def auth(self, login, password):
        result = self.cur.execute("select * from Auth where login = ? and password = ?",
                                  (login, password,)).fetchall()
        return result

    def updateTableRequest(self, text):
        result = self.cur.execute('select * from product where product_brand like ? or product_name like ?',
                                  ('%' + str(text) + '%', '%' + str(text) + '%',)).fetchall()
        return result

    def updateProduct(self, product_id, brand, name, price, count, required):
        self.cur.execute('update product set product_brand = ?, product_name = ?, product_price = ?, product_count = ?,'
                         'product_required = ? where product_id = ?', (brand, name, price, count, required, product_id))
        self.commitConnection()

    def updateProductPhoto(self, product_id, path):
        self.delPhoto(product_id)
        self.savePhoto(path)
        path = '../Image/DBImage/' + path[path.rfind('/') + 1:]
        self.cur.execute('update product set product_photo = ? where product_id = ?', (path, product_id))
        self.commitConnection()

    def checkUser(self, login, password):
        result = self.cur.execute("select * from Auth where login = ? and password = ?",
                                  (login, password,)).fetchall()
        return result

    def registrationUser(self, login, password):
        self.cur.execute('INSERT INTO Auth (login, password, admin) VALUES (?, ?, ?)', (login, password, 0,))
        self.commitConnection()

    def delPhoto(self, product_id):
        result = self.cur.execute('select product_photo from product where product_id = ?', (product_id,)).fetchone()
        result = self.cur.execute('select product_photo from product where product_photo = ?', (result[0],)).fetchall()
        try:
            if len(result) == 1:
                os.remove(result[0][0])
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    def savePhoto(self, path):
        try:
            shutil.copy(path, '../Image/DBImage/')
        except FileNotFoundError:
            pass
        except shutil.SameFileError:
            pass

    def getStats(self, user_login):
        result = self.cur.execute('select purchases, Money, counterProducts from Auth where login = ?',
                                  (user_login,)).fetchall()
        return result[0]

    def getUsers(self):
        result = self.cur.execute('select login from Auth').fetchall()
        return result

    def setAdmin(self, login):
        self.cur.execute('update Auth set admin = 1 where login = ?', (login,))
        self.commitConnection()

    def getTransactions(self):
        result = self.cur.execute('select * from product where product_count >= product_required '
                                  'and product_required != 0').fetchall()
        return result

    def buyProduct(self, transactions):
        self.cur.execute('update product set product_count = product_count - ?', (transactions[4],))
        self.commitConnection()

    def commitConnection(self):  # коммит
        self.connect.commit()

    def closeConnection(self):  # Закрываем соединение
        self.connect.close()

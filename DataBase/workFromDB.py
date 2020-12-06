import sqlite3
import os
#  Импорт всех нужных библиотек, стилей


class DB:
    def __init__(self):
        self.connect = sqlite3.connect('../DataBase/auth.db')  # Создаем соединение
        self.cur = self.connect.cursor()  # Создаем курсор

    def addProduct(self, name, brand, model, price, count):  # Функция для работы с базой данных.
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
                os.remove(result[0][0])
        except FileNotFoundError:
            pass
        self.cur.execute('delete from product where product_id = ?', (product_id, ))
        self.commitConnection()

    def auth(self, login, password):
        result = self.cur.execute("select * from Auth where login = ? and password = ?",
                                  (login, password,)).fetchall()
        return result

    def updateTableRequest(self, text):
        result = self.cur.execute('select * from product where product_brand like ? or product_name like ?',
                                  ('%' + str(text) + '%', '%' + str(text) + '%',)).fetchall()
        return result

    def updateProduct(self, id, brand, name, price, count, required):
        self.cur.execute('update product set product_brand = ?, product_name = ?, product_price = ?, product_count = ?,'
                         ' product_required = ? where product_id = ?', (brand, name, price, count, required, id))
        self.commitConnection()

    def checkUser(self, login, password):
        result = self.cur.execute("select * from Auth where login = ? and password = ?",
                                  (login, password,)).fetchall()
        return result

    def registrationUser(self, login, password):
        self.cur.execute('INSERT INTO Auth (login, password) VALUES (?, ?)', (login, password,))

    def commitConnection(self):  # коммит
        self.connect.commit()

    def closeConnection(self):  # Закрываем соединение
        self.connect.close()

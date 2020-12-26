import sqlite3
import os
import shutil


#  Импорт всех нужных библиотек, стилей

class DB:  # Класс для работы с базой данных
    def __init__(self):
        self.connect = sqlite3.connect('../DataBase/auth.db')  # Создаем соединение
        self.cur = self.connect.cursor()  # Создаем курсор

    def auth(self, login, password):
        result = self.cur.execute("select * from Auth where login = ? and password = ?",
                                  (login, password,)).fetchall()
        return result

    def addProduct(self, path, brand, model, price, count):  # Функция для работы с базой данных.
        self.savePhoto(path)
        if len(brand) == 0:
            brand = 'None'
        if len(model) == 0:
            model = 'None'
        name = '../Image/DBImage/' + path[path.rfind('/') + 1:]
        self.cur.execute('INSERT INTO product (product_photo, product_brand, product_name, product_price,'
                         ' product_count, product_required) VALUES (?, ?, ?, ?, ?, ?)',
                         (name, brand, model, price, count, 0,))
        if brand == 'None':
            product_id = self.cur.execute('select product_id from product where product_brand = ?', (brand, )).fetchone()
            self.cur.execute('update product set product_brand = ? where product_id = ?',
                             (product_id[0], product_id[0]))
        if model == 'None':
            product_id = self.cur.execute('select product_id from product where product_name = ?', (model,)).fetchone()
            self.cur.execute('update product set product_name = ? where product_id = ?',
                             (product_id[0], product_id[0]))
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

    def updateProduct(self, product_id, brand, name, price, count, required):
        self.cur.execute('update product set product_brand = ?, product_name = ?, product_price = ?, product_count = ?,'
                         'product_required = ? where product_id = ?', (brand, name, price, count, required, product_id))
        self.commitConnection()

    def buyProduct(self, transactions, login):
        self.cur.execute('update product set product_count = product_count - ? where product_brand = ? and '
                         'product_name = ?', (int(transactions[4]), int(transactions[0]), transactions[1],))
        self.cur.execute('update Auth set purchases = purchases + 1, money = money + ?,'
                         ' counterProducts = counterProducts + ? where login = ?',
                         (float(transactions[7]), int(transactions[4]), login,))
        self.commitConnection()

    def findTableRequest(self, text):  # Поиск по таблице
        result = self.cur.execute('select * from product where product_brand like ? or product_name like ?',
                                  ('%' + str(text) + '%', '%' + str(text) + '%',)).fetchall()
        return result

    def updateProductPhoto(self, product_id, path):  # Обновление фотографии
        self.delPhoto(product_id)
        self.savePhoto(path)
        path = '../Image/DBImage/' + path[path.rfind('/') + 1:]
        self.cur.execute('update product set product_photo = ? where product_id = ?', (path, product_id))
        self.commitConnection()

    def checkUser(self, login, password):  # Проверка пользователя на существование
        result = self.cur.execute("select * from Auth where login = ? and password = ?",
                                  (login, password,)).fetchall()
        return result

    def registrationUser(self, login, password):  # Зарегистрировать пользователя
        self.cur.execute('INSERT INTO Auth (login, password, admin) VALUES (?, ?, ?)', (login, password, 0,))
        self.commitConnection()

    def delPhoto(self, product_id):  # Удалить фото если оно не используется
        result = self.cur.execute('select product_photo from product where product_id = ?', (product_id,)).fetchone()
        result = self.cur.execute('select product_photo from product where product_photo = ?', (result[0],)).fetchall()
        try:
            if len(result) == 1:
                os.remove(result[0][0])
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    @staticmethod
    def savePhoto(path):  # Сохранить фото в папку с приложением
        try:
            shutil.copy(path, '../Image/DBImage/')
        except FileNotFoundError:
            pass
        except shutil.SameFileError:
            pass

    def getStats(self, user_login):  # Получить статистику для user_login пользователя
        result = self.cur.execute('select purchases, money, counterProducts from Auth where login = ?',
                                  (user_login,)).fetchall()
        return result[0]

    def getUsers(self):  # Получить всех пользователей
        result = self.cur.execute('select login from Auth').fetchall()
        return result

    def getTransactions(self):  # Получчить список продуктов готовых для транзакции
        result = self.cur.execute('select * from product where product_count >= product_required '
                                  'and product_required != 0').fetchall()
        return result

    def resetProductRequired(self):
        self.cur.execute('update product set product_required = 0')

    def setAdmin(self, login):  # Назначить администратора
        self.cur.execute('update Auth set admin = 1 where login = ?', (login,))
        self.commitConnection()

    def commitConnection(self):  # коммит
        self.connect.commit()

    def closeConnection(self):  # Закрываем соединение
        self.connect.close()

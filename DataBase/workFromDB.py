import sqlite3
#  Импорт всех нужных библиотек, стилей


class db:
    def __init__(self):
        self.connect = sqlite3.connect('../DataBase/auth.db')  # Создаем соединение
        self.cur = self.connect.cursor()  # Создаем курсор

    def addProduct(self, name, brand, model, price, count):  # Функция для работы с базой данных.
        self.cur.execute('INSERT INTO product (product_photo, product_brand, product_name, product_price,'
                          ' product_count) VALUES (?, ?, ?, ?, ?)',
                          ('../Image/DBImage' + name, brand, model, price, count,))
        self.commitConnection()
        # Проводим запрос

    def auth(self, login, password):
        result = self.cur.execute("select * from Auth where login = ? and password = ?",
                    (login, password,)).fetchall()
        return result

    def commitConnection(self):  # коммит
        self.connect.commit()

    def closeConnection(self):  # Закрываем соединение
        self.connect.close()

  #  Сделать иерархию окон
  #  Сделать класс для работы с бд
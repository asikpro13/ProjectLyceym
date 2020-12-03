import sqlite3  # Работа с бд
#  Импорт всех нужных библиотек, стилей


def db(zapr, *args):  # Функция для работы с базой данных
    connect = sqlite3.connect('../DataBase/auth.db')  # Создаем соединение
    cun = connect.cursor()  # Создаем курсор
    result = cun.execute(zapr, *args).fetchall()  # ->
    # Проводим запрос и получаем результат(если запрос это предусматривает)
    connect.commit()  # коммит
    connect.close()  # Закрываем соединение
    return result  # Возвращаем результат из бд
  #  Сделать иерархию окон
  #  Сделать класс для работы с бд
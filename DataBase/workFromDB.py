import sqlite3


def db(zapr, *args):
    connect = sqlite3.connect('../DataBase/auth.db')
    cun = connect.cursor()
    result = cun.execute(zapr, *args).fetchall()
    connect.commit()
    connect.close()
    return result
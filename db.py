import sqlite3

# подключение БД
db = sqlite3.connect('db/db.db')
cursor = db.cursor()

# вытягивание данных БД
def getData(id, column, table='users'):
    query = f""" SELECT {column} FROM {table} WHERE id = {id}"""
    cursor.execute(query)
    rows = cursor.fetchall()
    row = ""
    for row in rows:
        row = str(row).replace(",", "").replace("(", "").replace(")", "").replace("[", "").replace("'", "")
    return str(row)

# все зарегистрированные id
def getIDs():
    query = f""" SELECT id FROM users"""
    cursor.execute(query)
    rows = cursor.fetchall()
    rows = [row[0] for row in rows]
    return rows

# Добавление пользователя в игру
async def addToGame(id):
    if id not in getIDs():
        query = f" INSERT INTO users (id) VALUES ({id})"
        cursor.execute(query)
        db.commit()
        return True
    else:
        return False

async def deleteFromGame(id):
    query = f"DELETE FROM users WHERE id={id}"
    cursor.execute(query)
    db.commit()

# обновление данных в БД
def updateData(id, column, value, table='users'):
    if value == None:
        query = f" UPDATE {table} SET {column} = NULL WHERE id = {id} "
    else:
        query = f" UPDATE {table} SET {column} = '{value}' WHERE id = {id} "
    cursor.execute(query)
    db.commit()
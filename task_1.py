# Завдання 1
# Зробіть таблицю для підрахунку особистих витрат із такими полями: id, призначення, сума, час.

import sqlite3

connection = sqlite3.connect('db.sqllite3')
cursor = connection.cursor()

def init_db():
    create_table()
    add_values('продукти', 980)
    add_values('канцелярія', 3470)
    add_values('одяг', 35000)

def commit_decorator(func):
    def wrapper(*args, **kwargs):
        query = func(*args, **kwargs)
        cursor.execute(query)
        connection.commit()
    return wrapper

@commit_decorator
def create_table():
    query = '''CREATE TABLE IF NOT EXISTS Costs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purpose VARCHAR(255) NOT NULL,
        sum INTEGER,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )'''
    return query

def add_values(purpose:str, sum:int):
     if table_exists("Costs"):
        query = '''INSERT INTO Costs (purpose, sum) VALUES (?, ?)'''
        cursor.execute(query, (purpose, sum))
        connection.commit()

def table_exists(table_name: str) -> bool:
    query = '''SELECT name FROM sqlite_master WHERE type='table' AND name=?'''
    cursor.execute(query, (table_name,))
    return cursor.fetchone() is not None

init_db()

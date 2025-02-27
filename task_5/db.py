from config import cursor, connection
from monobank import data

keys = ["currency_code", "currency_name", "currency_value", "current_date"]

def init_db():
    create_table_currencies()
    add_values(*[get_value(data, 0, field) for field in keys])
    add_values(*[get_value(data, 1, field) for field in keys])

def commit_decorator(func):
    def wrapper(*args, **kwargs):
        query = func(*args, **kwargs)
        cursor.execute(query)
        connection.commit()
    return wrapper

@commit_decorator
def create_table_currencies():
    query = '''CREATE TABLE IF NOT EXISTS Currencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        currency_code INTEGER,
        currency_name TEXT,
        currency_value REAL,
        current_date DATETIME
    );'''
    return query

def add_values(code:int, name:str, value:float, date:str):
     if table_exists("Currencies"):
        query = '''INSERT INTO Currencies (
            currency_code,
            currency_name,
            currency_value,
            current_date
            ) VALUES (?, ?, ?, ?)'''
        cursor.execute(query, (code, name, value, date))
        connection.commit()

def get_by_code(currency_name:str):
    query = f'''SELECT currency_value FROM Currencies WHERE currency_name = "{currency_name}"'''
    result = cursor.execute(query)
    currency = result.fetchone()
    if currency:
        return currency[0]
    else:
        return None

def get_value(obj, idx:int, value:str):
    return obj[idx].get(value)

def table_exists(table_name: str) -> bool:
    query = '''SELECT name FROM sqlite_master WHERE type='table' AND name=?'''
    cursor.execute(query, (table_name,))
    return cursor.fetchone() is not None

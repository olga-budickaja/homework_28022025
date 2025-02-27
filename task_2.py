# Завдання 2
# Створіть консольний інтерфейс (CLI) на Python для додавання нових записів до бази даних.

import sqlite3


class CustomInputError(Exception):
    pass


#INTERFASE
expenses = [
    "Продукти",
    "Оренда житла",
    "Транспорт",
    "Комунальні послуги",
    "Зв'язок та інтернет",
    "Розваги",
    "Медицина",
    "Одяг",
    "Освіта",
    "Ресторани та кафе"
]

LIMIT_EXPENSES = 100000

def error_decorator(func):
    def wrapper(num:int, *args, length=LIMIT_EXPENSES, **kwargs,):
        while True:
            try:
                if not isinstance(num, int):
                    raise CustomInputError("Помилка! Введіть число.")

                if not (1 <= num <= length):
                    raise CustomInputError(f"Помилка! Введене число поза межами діапазону (1-{length}).")

                return func(num, *args, **kwargs)

            except (CustomInputError, ValueError) as e:
                print(e)
                num = int(input(f"Спробуйте ще раз. Введіть число між 1 і {length}: "))

    return wrapper

def expenses_menu():
    menu = "\n".join(f"{idx + 1}. {expense}" for idx, expense in enumerate(expenses))
    return menu

@error_decorator
def get_expense(num:int, length:int):
    return expenses[num -1]

@error_decorator
def get_sum_expense(num:int):
    return num


expense_number = input(f"Оберіть категорію витрат:\n\n{expenses_menu()}\n: ")
expanse = get_expense(int(expense_number), len(expenses))

sum_expense = int(input("Введіть суму витрати: "))
sum = get_sum_expense(sum_expense)


# DB
connection = sqlite3.connect('db.sqllite3')
cursor = connection.cursor()

def init_db():
    create_table()
    add_values(expense=expanse, sum=sum)


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
        expense VARCHAR(255) NOT NULL,
        sum INTEGER,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )'''
    return query

def add_values(expense:str, sum:int):
     if table_exists("Costs"):
        query = '''INSERT INTO Costs (expense, sum) VALUES (?, ?)'''
        cursor.execute(query, (expense, sum))
        connection.commit()

def table_exists(table_name: str) -> bool:
    query = '''SELECT name FROM sqlite_master WHERE type='table' AND name=?'''
    cursor.execute(query, (table_name,))
    return cursor.fetchone() is not None

init_db()

# Завдання 3
# Змініть таблицю так, щоби можна було додати не лише витрати, а й прибутки.

import sqlite3

class CustomInputError(Exception):
    pass

# INTERFACE
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
incomes = [
    "Зарплата",
    "Повернутий борг",
    "Подарунок",
]

LIMIT_EXPENSES = 100000

def error_decorator(func):
    def wrapper(*args, num='', length=LIMIT_EXPENSES, **kwargs):
        while True:
            try:
                if num != '':
                    if not num.isdigit():
                        raise CustomInputError("Помилка! Введіть число.")

                    if not (1 <= int(num) <= length):
                        raise CustomInputError(f"Помилка! Введене число поза межами діапазону (1-{length}).")
                return func(*args, **kwargs)
            except (CustomInputError, ValueError) as e:
                print(e)
                num = input(f"Спробуйте ще раз. Введіть число між 1 і {length}: ")
    return wrapper

def menu(obj):
    return "\n".join(f"{idx + 1}. {item}" for idx, item in enumerate(obj))

@error_decorator
def get_category(obj, num, length):
    if num != 0 and num != '':
        return obj[num - 1]
    else:
        return "-"

@error_decorator
def get_sum(num):
    return num if num not in (0, '') else 0

expense_number = input(f"Оберіть категорію витрат:\n\n{menu(expenses)}\n: ")
expense_sum_number = input("Введіть суму витрати: ")
income_number = input(f"Оберіть категорію прибутків:\n\n{menu(incomes)}\n: ")
income_sum_number = input("Введіть суму прибутку: ")

print("expense_number: ", expense_number)
print("expense_sum_number: ", expense_sum_number)
print("income_number: ", income_number)
print("income_sum_number: ", income_sum_number)

@error_decorator
def get_category(obj, num, length):
    if num != 0 and num != '':
        return obj[int(num) - 1]
    else:
        return "-"

data = (
    get_category(expenses, expense_number, len(expenses)),
    get_sum(expense_sum_number),
    get_category(incomes, income_number, len(incomes)),
    get_sum(income_sum_number),
)

expense, sum_expense, income, sum_income = data


# DB
connection = sqlite3.connect('db.sqllite3')
cursor = connection.cursor()

def init_db():
    create_table()
    add_values(expense=expense, sum_expense=sum_expense, income=income, sum_income=sum_income)


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
        expense VARCHAR(255),
        sum_expense INTEGER,
        income VARCHAR(255),
        sum_income INTEGER,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )'''
    return query

def add_values(expense:str, sum_expense:int, income:str, sum_income:int):
     if table_exists("Costs"):
        query = '''INSERT INTO Costs (expense, sum_expense, income, sum_income) VALUES (?, ?, ?, ?)'''
        cursor.execute(query, (expense, sum_expense, income, sum_income))
        connection.commit()

def table_exists(table_name: str) -> bool:
    query = '''SELECT name FROM sqlite_master WHERE type='table' AND name=?'''
    cursor.execute(query, (table_name,))
    return cursor.fetchone() is not None

init_db()

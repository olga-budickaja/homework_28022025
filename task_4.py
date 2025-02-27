# Завдання 4
# Створіть агрегатні функції для підрахунку загальної кількості  витрат i прибуткiв за місяць.
# Забезпечте відповідний інтерфейс користувача.

import sqlite3


#interface
menu = '''1. Сума витрат за місяць.\n2. Сума прибутків за місяць.\n2. Вихід'''

def get_menu_choice(menu: str, min_option: int, max_option: int) -> int:
    while True:
        print(menu)
        choice = input("Оберіть пункт меню: ").strip()

        if not choice.isdigit():
            print("Помилка! Введіть лише номер пункту меню.")
            continue

        choice = int(choice)

        if min_option <= choice <= max_option:
            return choice
        else:
            print(f"Помилка! Введене число повинно бути в діапазоні {min_option}-{max_option}.")

def get_month_date():
    while True:
        year = input("Введіть рік: ").strip()
        month = input("Введіть місяць: ").strip()

        if not year.isdigit() or not month.isdigit():
            print("Помилка! Введіть коректні числові значення.")
            continue

        if not (2024 <= int(year) <= 2025):
            print("Помилка! Рік має бути від 2024 до 2025.")
            continue

        if not (1 <= int(month) <= 12):
            print("Помилка! Місяць має бути від 01 до 12.")
            continue

        return f"{year}-{month}"

#db
connection = sqlite3.connect('db.sqllite3')
cursor = connection.cursor()

def init_db():
    while True:
        choice = get_menu_choice(menu, 1, 3)

        if choice == 1:
            date = get_month_date()
            sum_expense = aggregate_function("sum_expense", date)
            print(f"Сума витрат за {date}: {sum_expense}грн.")
        elif choice == 2:
            date = get_month_date()
            sum_income = aggregate_function("sum_income", date)
            print(f"Сума прибутків за {date}: {sum_income}грн.")
        elif choice == 3:
            print("Вихід із програми.")
            break

def aggregate_function(column_name: str, month: str):
    query = f"""
        SELECT SUM({column_name}) AS TotalSumExpense
        FROM Costs
        WHERE strftime('%Y-%m', date) = ?;
    """
    result = cursor.execute(query, (month,))
    data = result.fetchone()
    return data[0] if data[0] is not None else 0

init_db()

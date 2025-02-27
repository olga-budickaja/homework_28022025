# Create an Exchange Rates To USD db using API Monobank (api.monobank.ua).
# Do requests via request lib, parse results, write it into db. (3 examples required)
# Example:
# Table - Exchange Rate To USD:

# id (INT PRIMARY KEY) - 1, 2, 3, ...
# currency_name (TEXT) - UAH
# currency_value (REAL) - 39.5
# current_date (DATETIME) - 10/22/2022 7:00 PM


import schedule
from db import get_by_code, init_db


MENU = '''1. Перевести Гривні в Долари.\n2. Перевести Гривні в Євро.\n3. Вихід'''


rate_usd = get_by_code('USD')
rate_eur = get_by_code('EUR')

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

def convert_currency():
    while True:
        choice = get_menu_choice(MENU, 1, 3)
        if choice == 1:
            uah_amount = float(input("Кількість гривень: "))
            print(f"{uah_amount} гривен (UAH) = {uah_amount / rate_usd} долларов (USD)")
        elif choice == 2:
            uah_amount = float(input("Кількість гривень: "))
            print(f"{uah_amount} гривен (UAH) = {uah_amount / rate_eur} євро (EUR)")
        elif choice == 3:
            print("Вихід із програми.")
            break

schedule.every().day.at("09:00", "Europe/Amsterdam").do(init_db)
schedule.every().day.at("18:00", "Europe/Amsterdam").do(init_db)
convert_currency()

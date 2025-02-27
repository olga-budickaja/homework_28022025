import datetime
import time
import requests


def get_monobank_rates():
    url = "https://api.monobank.ua/bank/currency"

    try:
        response = requests.get(url)

        if response.status_code == 429:
            print("Забагато запитів. Очікування 10 секунд перед повтором...")
            time.sleep(10)
            return get_monobank_rates()

        if response.status_code == 200:
            data = response.json()

            rate_usd = data[0]['rateBuy']
            date_usd = data[0]['date']
            rate_eur = data[1]['rateBuy']
            date_eur = data[1]['date']

            return rate_usd, date_usd, rate_eur, date_eur

        else:
            print(f"Не вдалося отримати дані, статус код: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print("Помилка при отриманні даних:", e)
        return None

def create_data(rate:int, code:int, date:int):
    return {
        "currency_code": code,
        "currency_name": "USD" if code == 840 else "EUR",
        "currency_value": rate,
        "current_date": date
    }

def formated_date(date:int):
    dt_object = datetime.date.fromtimestamp(date)
    return dt_object.strftime("%m/%d/%Y %I:%M %p")

rate_usd, date_usd, rate_eur, date_eur = get_monobank_rates()

data_usd = create_data(rate_usd, 840, formated_date(date_usd))
data_eur = create_data(rate_eur, 978, formated_date(date_eur))

data = [data_usd, data_eur]

import json
import requests
from config import currency, API_KEY


class APIExeption(Exception):
    pass


class Convert:

    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = currency[base.lower()]
        except KeyError:
            raise APIExeption(f'Валюта {base} не найдена!')
        try:
            quote_key = currency[quote.lower()]
        except KeyError:
            raise APIExeption(f'Валюта {quote} не найдена!')
        if base_key == quote_key:
            raise APIExeption(f"Невозможно перевести одинаковые валюты!")
        try:
            amount = float(amount)
        except ValueError:
            raise  APIExeption(f"Невозможно обработать количество")
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={quote_key}&base={base_key}"
        payload = {}
        headers= dict(apikey=API_KEY)
        response = requests.get(url, headers=headers, data = payload)
        result = json.loads(response.content)['rates'][currency[quote]]
        price = result * amount
        text = f'Цена {amount} {base} в {quote}: {price:.2f}'
        return text

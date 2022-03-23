from config import exchanges, api_user
import requests
import json


class ConvertionExseption(Exception):
    pass


class Convertor:
    @staticmethod
    def convert(given: str, rate: str, amount: str):
        base = exchanges[given]
        sym = exchanges[rate]

        if base == sym:
            raise ConvertionExseption(f'Невозможно перевести одинаковые валюты')

        try:
            base_key = exchanges[given.lower()]
        except KeyError:
            raise ConvertionExseption(f'Не удалось обработать валюту {base}')

        try:
            sym_key = exchanges[rate.lower()]
        except KeyError:
            raise ConvertionExseption(f'Не удалось обработать валюту {sym}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExseption(f'Не удалось обработать количество {amount}')

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={api_user}&base={base}&symbols={sym}")
        resp = json.loads(r.content)
        new_price = resp['rates'][exchanges[rate]] * float(amount)
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message


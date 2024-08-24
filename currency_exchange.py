# currency_exchange.py
import requests

class CurrencyExchange:
    def __init__(self, api_key):
        self.api_key = api_key

    def convert_currency(self, source_currency, target_currency, amount):
        url = f'https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{source_currency}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            conversion_rates = data['conversion_rates']

            if target_currency in conversion_rates:
                exchange_rate = conversion_rates[target_currency]
                converted_amount = amount * exchange_rate
                return converted_amount
            else:
                return 'Currency not found'
        else:
            return 'Invalid API request'

    def display_conversion(self, source_currency, target_currency, amount):
        converted_amount = self.convert_currency(source_currency, target_currency, amount)
        if isinstance(converted_amount, float):
            print(f'The amount you entered is {amount} {source_currency}')
            print(f'Converted amount is {converted_amount:.2f} {target_currency}')
        else:
            print(converted_amount)

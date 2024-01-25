import currencyapicom
import datetime
import requests
import yaml

with open("currency_exchange_api/config.yaml", "r") as file:
    config = yaml.safe_load(file)

client = currencyapicom.Client(config['api_key'])

def get_available_currency_codes() -> list[str]:
    return list(client.currencies()["data"].keys())

def is_currency_valid(currency_code: str, currency_codes: list[str]) -> bool:
    return currency_code in currency_codes

def is_currencies_list_valid(currencies_list: str, currency_codes: list[str]):
    try:
        currencies = currencies_list.split(',')
    except:
        return False
    
    for currency in currencies:
        if not is_currency_valid(currency, currency_codes):
            return False
    return True

def is_amount_valid(amount: str) -> bool:
    try:
        float(amount)
    except:
        return False
    
    if float(amount) < 0.0:
        return False
    
    if '.' in amount:
        if len(amount.split('.')[1]) == 2: # check two decimal places
            return True
        
    return False

def is_date_valid(date: str) -> bool:
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        return False
    return True

def construct_request(endpoint: str, input_currency: str, output_currencies: str, amount: str, date: str) -> str:
    request = endpoint + '?'
    request += 'input_currency={} &'.format(input_currency)

    for currency in output_currencies.split(','):
        request += 'output_currencies={}&'.format(currency)
    
    request += 'amount={}&'.format(amount)
    request += 'date={}&'.format(date)

    return request

def prepare_response(input_currency: str, output_currencies: str, amount: str, date: str) -> None:
    endpoint = 'http://127.0.0.1:8000/currency_conversion'
    response = requests.get(construct_request(endpoint, input_currency, output_currencies, amount, date))
    data = response.json()

    print('\n')
    if response.status_code != 200:
        print('REQUEST FAILED')
        print(data['detail'])
        return
    
    print('DATA FOR {}:\n'.format(date))

    for rate in data:
        print('   -> {} {} = {} {}'.format(amount, input_currency, rate['currency'], rate['amount']))

def main() -> None:
    currency_codes = get_available_currency_codes()

    input_currency = input("Enter input currency: ")
    while not is_currency_valid(input_currency, currency_codes):
        input_currency = input("Specified currency is not valid. Please enter input currency once again: ")

    output_currencies = input("Enter output currency: ")
    while not is_currencies_list_valid(output_currencies, currency_codes):
        output_currencies = input("Specified currency is not valid. Please enter output currency once again: ")

    amount = input("Enter amount: ")
    while not is_amount_valid(amount):
        amount = input("Specified amount is not valid. Please enter amount once again: ")

    date = input("Enter date: ")
    while not is_date_valid(date):
        date = input("Specified date is not valid. Please enter date once again: ")

    prepare_response(input_currency, output_currencies, amount, date)


if __name__ == "__main__":
    main()

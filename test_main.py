from main import is_currency_valid, is_currencies_list_valid, is_amount_valid, is_date_valid, construct_request, get_available_currency_codes
import currencyapicom
import yaml

with open("currency_exchange_api/config.yaml", "r") as file:
    config = yaml.safe_load(file)

client = currencyapicom.Client(config['api_key'])

def test_is_currency_valid():
    currency_codes = get_available_currency_codes()
    assert is_currency_valid("EUR", currency_codes) == True
    assert is_currency_valid("EUR ", currency_codes) == False
    assert is_currency_valid("fdsfg", currency_codes) == False

def test_is_currencies_list_valid():
    currency_codes = get_available_currency_codes()
    assert is_currencies_list_valid("EUR,USD,PLN", currency_codes) == True
    assert is_currencies_list_valid("EUR, USD,PLN", currency_codes) == False
    assert is_currencies_list_valid("EUR,USD,PLN3", currency_codes) == False
    assert is_currencies_list_valid("EUR,", currency_codes) == False
    assert is_currencies_list_valid("EUR", currency_codes) == True
    assert is_currencies_list_valid(",EUR,USD,PLN", currency_codes) == False
    assert is_currencies_list_valid("EUR,USD,PLN,", currency_codes) == False

def test_is_amount_valid():
    assert is_amount_valid("14.65") == True
    assert is_amount_valid("0.00") == True
    assert is_amount_valid("14.655") == False
    assert is_amount_valid("13") == False
    assert is_amount_valid("14.") == False
    assert is_amount_valid("-1.43") == False
    assert is_amount_valid("-0.00") == True
    assert is_amount_valid("fsds") == False
    assert is_amount_valid("43.ds") == False

def test_is_date_valid():
    assert is_date_valid('2023-04-01') == True
    assert is_date_valid('2023-14-01') == False
    assert is_date_valid('1997-02-29') == False
    assert is_date_valid('01-12-2022') == False
    assert is_date_valid('2023/11/01') == False
    assert is_date_valid('gfgdsd') == False
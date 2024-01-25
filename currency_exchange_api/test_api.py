from fastapi.testclient import TestClient
from .api import app, round_up

client = TestClient(app)

def test_round_up():
    assert round_up(47.346632) == 47.35
    assert round_up(65.46164) == 65.47
    assert round_up(10.0) == 10.0
    assert round_up(54.001) == 54.01
    assert round_up(33.000) == 33.00

def test_get_currency_conversion_valid():
    response = client.get('/currency_conversion?input_currency=EUR&output_currencies=PLN&output_currencies=USD&amount=15.0&date=2024-01-03')
    assert response.status_code == 200

def test_get_currency_conversion_negative_amount():
    response = client.get('/currency_conversion?input_currency=EUR&output_currencies=PLN&output_currencies=USD&amount=-15.0&date=2024-01-03')
    assert response.status_code == 422

def test_get_currency_conversion_invalid_date():
    response = client.get('/currency_conversion?input_currency=EUR&output_currencies=PLN&output_currencies=USD&amount=15.0&date=03-01-2024')
    assert response.status_code == 422

    response = client.get('/currency_conversion?input_currency=EUR&output_currencies=PLN&output_currencies=USD&amount=15.0&date=2024-13-01')
    assert response.status_code == 422

def test_get_currency_conversion_future_date():
    response = client.get('/currency_conversion?input_currency=EUR&output_currencies=PLN&output_currencies=USD&amount=15.0&date=2028-11-01')
    assert response.status_code == 400

def test_get_currency_conversion_invalid_currency():
    response = client.get('/currency_conversion?input_currency=sddfds&output_currencies=PLN&output_currencies=USD&amount=15.0&date=2024-01-03')
    assert response.status_code == 400

    response = client.get('/currency_conversion?input_currency=EUR&output_currencies=dsds&output_currencies=USD&amount=15.0&date=2024-01-03')
    assert response.status_code == 400
from fastapi import FastAPI, Query, HTTPException
from datetime import date
from pydantic import BaseModel
from typing import Annotated
import currencyapicom
import yaml

app = FastAPI()

with open("currency_exchange_api/config.yaml", "r") as file:
    config = yaml.safe_load(file)

client = currencyapicom.Client(config['api_key'])

class CurrencyConversionResult(BaseModel):
    currency: str
    amount: float

def round_up(value: float) -> float:
    value_rounded = round(value, 2)
    if 0 < value - int(value * 100) / 100 < 0.005:
        value_rounded += 0.01
    return value_rounded

@app.get("/currency_conversion")
def get_currency_conversion(input_currency: str, output_currencies: Annotated[list[str], Query()], amount: float, date: date) -> list[CurrencyConversionResult]:
    """
    Get exchange rates from currencyapi, calculate equivalent amount in specified currency and round up.

    Returns list of jsons in format:
    [
        {
            "currency code": string,
            "amount": float
        }
    ]
    """
    if amount < 0:
        raise HTTPException(status_code=422, detail=f"Provided amount needs to be a positive value.")

    try:
        result = client.historical(date=date, base_currency=input_currency, currencies=output_currencies)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = result['data']
    conversions = []
    for currency in data:
        conversions.append(CurrencyConversionResult(currency=currency, amount=round_up(data[currency]['value'] * amount)))

    return conversions

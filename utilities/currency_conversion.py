from currency_converter import CurrencyConverter, RateNotFoundError, ECB_URL
from datetime import date, datetime
from fastapi import HTTPException

"""
currency_list = [JPY', 'PHP', 'SEK', 'EUR', 'NOK', 'ILS', 'THB', 'ISK', 'MXN', 'CAD', 'MTL', 'CNY', 'HUF', 'KRW',
 'IDR', 'GBP', 'EEK', 'INR', 'NZD', 'TRL', 'PLN', 'CYP', 'LVL', 'BRL', 'HKD', 'AUD', 'MYR', 'ROL', 'CHF', 'CZK', 'HRK', 
 'SKK', 'SIT', 'TRY', 'USD', 'RON', 'SGD', 'ZAR', 'BGN', 'RUB', 'DKK']
"""

cur = CurrencyConverter(
    ECB_URL, decimal=True, fallback_on_missing_rate=True, fallback_on_wrong_date=True
)


def convert_currency(amount, current_currency, target_currency, in_date):

    try:
        # new_date = datetime.strptime(in_date, "%Y-%m-%d").strftime("%Y-%m-%d")

        converted_amount = cur.convert(
            amount,
            current_currency.upper(),
            target_currency.upper(),
            date=date.fromisoformat(in_date),
        )

        exchange_rate = cur.convert(
            1,
            current_currency.upper(),
            target_currency.upper(),
            date=date.fromisoformat(in_date),
        )
    except RateNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="rate of the given currency is undefined for the given date ",
        )

    return {
        "code": 200,
        "message": "currency conversion from {} to {} ".format(
            current_currency.upper(), target_currency.upper()
        ),
        "payload": {
            "converted_amount": "{:.4f}".format(converted_amount),
            "exchange_rate": "{:.4f}".format(exchange_rate)
        },
    }

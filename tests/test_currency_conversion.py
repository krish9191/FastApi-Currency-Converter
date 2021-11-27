import pytest
from currency_converter import CurrencyConverter, ECB_URL

from datetime import date

from utilities.currency_conversion import convert_currency


@pytest.fixture
def create_instance_of_currency_converter():
    c = CurrencyConverter(
        ECB_URL,
        decimal=True,
        fallback_on_missing_rate=True,
        fallback_on_wrong_date=True,
    )
    return c


def test_converted_amount(create_instance_of_currency_converter):
    current_date = date.strftime(date.today(), "%Y-%m-%d")
    result = convert_currency(1, "eur", "usd", current_date)
    assert result["payload"]["converted_amount"] == str(create_instance_of_currency_converter.convert(
        1, "EUR", "USD", date=date.today()))


def test_exchange_rate(create_instance_of_currency_converter):
    current_date = date.strftime(date.today(), "%Y-%m-%d")
    result = convert_currency(1, "eur", "usd", current_date)
    exchange_rate = str((create_instance_of_currency_converter.convert(1, "EUR", "USD", date=date.today())))
    assert result["payload"]["exchange_rate"] == exchange_rate

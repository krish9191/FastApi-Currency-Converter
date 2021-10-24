import math
from typing import Optional
import uvicorn
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from fastapi import FastAPI

from utilities.currency_conversion import convert_currency, cur

app = FastAPI()


class CurrencyConvert(BaseModel):
    amount: Optional[float]
    current_currency: Optional[str]
    target_currency: str
    in_date: Optional[str]

    @validator("amount")
    def check_amount_is_nan(cls, value):
        if math.isnan(value):
            raise HTTPException(status_code=400, detail="amount must be only number")
        return value

    @validator("current_currency")
    def check_current_currency_in_currency_list(cls, value):
        if len(value) != 0 and value.upper() not in cur.currencies:
            raise HTTPException(
                status_code=400,
                detail="current currency is not define as supported currency",
            )
        return value

    @validator("target_currency")
    def check_target_currency_in_currency_list(cls, value):
        if len(value) == 0 or value.upper() not in cur.currencies:
            raise HTTPException(
                status_code=400,
                detail="target currency is not define as supported currency",
            )
        return value


currency_converter_router = APIRouter()


@app.post("/convert-currency")
def get_currency_conversion(c_obj: CurrencyConvert):
    return convert_currency(
        c_obj.amount, c_obj.current_currency, c_obj.target_currency, c_obj.in_date
    )


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8008)

import math
from typing import Optional
from pydantic import BaseModel, validator
from fastapi import HTTPException, Form


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
class CurrencyConvert(BaseModel):
    amount: Optional[float]
    date: Optional[str]

    @validator("amount")
    def check_amount_is_nan(cls, value):
        # if not value:
        #     raise HTTPException(status_code=400, detail="amount must be entered")

        if math.isnan(value):
            raise HTTPException(status_code=400, detail="amount must be only number")
        return value

    """
   def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

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

    """

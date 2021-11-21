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
        if value is None:
            raise HTTPException(status_code=400, detail="amount should be entered")

        if math.isnan(value):
            raise HTTPException(status_code=400, detail="amount must be only number")
        return value


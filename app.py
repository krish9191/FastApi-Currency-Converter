import uvicorn
from fastapi import Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from schemas import CurrencyConvert
from utilities.currency_conversion import convert_currency

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("currency_converter.html", {"request": request})


@app.post("/convert-currency", response_class=HTMLResponse, response_model=CurrencyConvert)
def get_currency_conversion(request: Request, form_data: CurrencyConvert = Depends(CurrencyConvert),
                            current: str = Form(...), target: str = Form(...)):

    func_response = convert_currency(form_data.amount, current, target, form_data.date)

    converted_amount = func_response.get("payload")["converted_amount"]
    exchange_rate = func_response.get("payload")["exchange_rate"]
    return templates.TemplateResponse("currency_converter.html", context={"request": request,
                                                                          "converted_amount": converted_amount,
                                                                          "exchange_rate": exchange_rate})


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

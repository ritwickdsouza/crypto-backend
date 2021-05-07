import datetime
from pydantic import BaseModel


class Currency(BaseModel):
    code: str
    name: str


class ExchangeRate(BaseModel):
    from_currency: Currency
    to_currency: Currency
    value: float
    refreshed_at: datetime.datetime

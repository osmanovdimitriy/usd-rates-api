from pydantic import BaseModel

class RateCreate(BaseModel):
    currency: str
    rate: float

class RateOut(BaseModel):
    currency: str
    rate: float

class CurrencyOut(BaseModel):
    code: str
    name: str
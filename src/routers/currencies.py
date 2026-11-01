from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models import Currency  # Импортируем модель
from src.schemas import CurrencyOut

router = APIRouter()


@router.get("/currencies", response_model=list[CurrencyOut])
async def get_currencies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Currency).limit(5))
    currencies: list[Currency] = result.scalars().all()
    return currencies
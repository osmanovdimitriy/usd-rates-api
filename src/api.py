from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database import get_db
from src.routers import currencies
from src.schemas import RateCreate, RateOut

myapp = FastAPI(docs_url=None, redoc_url=None)

myapp.mount("/static", StaticFiles(directory="static"), name="static")

@myapp.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=myapp.openapi_url,
        title=myapp.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@myapp.post("/rates")
async def create_rate(data: RateCreate):
    return {"status": "created", "received": data}

@myapp.get("/history")
async def get_history(currency: str = "USD", limit: int = 10):
    return {"currency": currency, "limit": limit}

@myapp.get("/rates/{currency}", response_model=RateOut)
async def get_rate(currency: str):
    if currency not in ["USD", "EUR"]:
        raise HTTPException(status_code=404, detail="Валюта не найдена")
    return {"currency": currency, "rate": 92.5}

myapp.include_router(currencies.router)

@myapp.post("/rates/db")
async def create_rate_db(data: RateCreate, db: AsyncSession = Depends(get_db)):
    await db.execute(
        text("INSERT INTO rates (currency, date, rate) VALUES (:cur, CURRENT_DATE, :rate)"),
        {"cur": data.currency, "rate": data.rate}
    )
    await db.commit()
    return {"status": "saved to db", "data": data}

@myapp.put("/rates/db/{rate_id}")
async def update_rate_db(rate_id: int, data: RateCreate, db: AsyncSession = Depends(get_db)):
    await db.execute(
        text("UPDATE rates SET rate = :rate WHERE id = :id"),
        {"rate": data.rate, "id": rate_id}
    )
    await db.commit()
    return {"status": "updated", "id": rate_id, "new_rate": data.rate}

@myapp.delete("/rates/db/{rate_id}")
async def delete_rate_db(rate_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(
        text("DELETE FROM rates WHERE id = :id"),
        {"id": rate_id}
    )
    await db.commit()
    return {"status": "deleted", "id": rate_id}
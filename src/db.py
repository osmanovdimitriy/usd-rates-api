import os
from datetime import date

import psycopg
from dotenv import load_dotenv

load_dotenv()


class RatesDB:
    """Обёртка над PostgreSQL для хранения курсов."""

    def __init__(self, dsn: str | None = None):
        self.dsn = dsn or os.getenv("DATABASE_URL")
        if not self.dsn:
            raise ValueError("DATABASE_URL не задан в .env")

    def _connect(self):
        return psycopg.connect(self.dsn)

    def init_schema(self) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS rates (
                        id SERIAL PRIMARY KEY,
                        currency VARCHAR(10) NOT NULL,
                        date DATE NOT NULL,
                        rate NUMERIC(12, 4) NOT NULL,
                        UNIQUE (currency, date)
                    )
                """)
            conn.commit()

    def save_rate(self, currency: str, rate: float, when: date | None = None) -> None:
        when = when or date.today()
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO rates (currency, date, rate)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (currency, date)
                    DO UPDATE SET rate = EXCLUDED.rate
                """, (currency, when, rate))
            conn.commit()

    def get_history(self, currency: str = "USD", limit: int = 10):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT date, rate FROM rates
                    WHERE currency = %s
                    ORDER BY date DESC
                    LIMIT %s
                """, (currency, limit))
                return cur.fetchall()


if __name__ == "__main__":
    db = RatesDB()
    db.init_schema()
    db.save_rate("USD", 92.5)
    print(db.get_history("USD"))
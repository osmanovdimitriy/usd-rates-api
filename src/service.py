from src.db import RatesDB
from src.parser import CbrParser


class RatesService:
    """Связка: парсер + БД."""

    def __init__(self, parser: CbrParser, db: RatesDB):
        self.parser = parser
        self.db = db

    def update_all(self) -> int:
        """Спарсил всё → сохранил всё. Возвращает кол-во валют."""
        rates = self.parser.get_all_rates()
        for r in rates:
            self.db.save_currency(r["code"], r["name"])
            self.db.save_rate(r["code"], r["rate"])
        return len(rates)
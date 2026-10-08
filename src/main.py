from src.db import RatesDB
from src.parser import CbrParser
from src.service import RatesService


def main() -> None:
    db = RatesDB()
    parser = CbrParser()
    service = RatesService(parser, db)

    db.init_schema()
    count = service.update_all()
    print(f"Обновлено валют: {count}")


if __name__ == "__main__":
    main()
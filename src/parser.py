import requests
from bs4 import BeautifulSoup


class CbrParser:
    """Парсер курсов с сайта ЦБ РФ."""

    BASE_URL = "https://www.cbr.ru/currency_base/daily/"

    def __init__(self, url: str | None = None):
        self.url = url or self.BASE_URL

    def get_rate(self, currency: str = "USD") -> float | None:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="data")
        if table is None:
            return None

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 5 and cols[1].text.strip() == currency:
                rate_str = cols[4].text.replace(",", ".")
                return float(rate_str)
        return None

class CryptoParser(CbrParser):
    """Наследник CbrParser — просто демонстрация наследования."""

    def get_rate(self, currency: str = "USD") -> float | None:
        return super().get_rate(currency)

if __name__ == "__main__":
    parser = CbrParser()
    print("USD:", parser.get_rate("USD"))
    print("EUR:", parser.get_rate("EUR"))

    crypto = CryptoParser()
    print("Crypto BTC:", crypto.get_rate())
    print("Crypto USD (унаследовано):", crypto.get_rate("USD"))
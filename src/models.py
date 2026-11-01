from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Numeric, Date, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    pass

class Currency(Base):
    __tablename__ = "currencies"
    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    symbol: Mapped[str | None] = mapped_column(String(5))

class Rate(Base):
    __tablename__ = "rates"
    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[str] = mapped_column(ForeignKey("currencies.code"))
    date: Mapped[Date] = mapped_column(Date)
    rate: Mapped[float] = mapped_column(Numeric(12, 4))
    source: Mapped[str | None] = mapped_column(String(50))

    __table_args__ = (UniqueConstraint("currency", "date"),)
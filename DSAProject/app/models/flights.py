from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Flight(Base):
    """Модель рейса для хранения в базе данных.

    Attributes:
        id (int): Внутренний первичный ключ БД(сам генерируется - с целыми числами БД легче работает, чем с самим первичным ключом таблицы).
        flight_id (str): Уникальный идентификатор рейса.
        airline (str): Название авиакомпании.
        origin_airport (str): Код аэропорта вылета.
        destination_airport (str): Код аэропорта назначения.
        departure_delay_min (int): Задержка вылета в минутах.
        aircraft_type (str): Модель воздушного судна.
        weather_condition (str): Погодные условия во время рейса.
        passenger_count (int): Количество пассажиров на борту.
        ticket_revenue_usd (float): Выручка от продажи билетов в долларах.
    """

    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)

    flight_id: Mapped[str] = mapped_column(String(50), unique=True)
    airline: Mapped[str] = mapped_column(String(100))
    origin_airport: Mapped[str] = mapped_column(String(10))
    destination_airport: Mapped[str] = mapped_column(String(10))
    departure_delay_min: Mapped[int] = mapped_column(default=0)

    aircraft_type: Mapped[str] = mapped_column(String(20), default="Unknown")
    weather_condition: Mapped[str] = mapped_column(String(50), default="Unknown")
    passenger_count: Mapped[int] = mapped_column(default=0)
    ticket_revenue_usd: Mapped[float] = mapped_column(default=0.0)
    # далее добавлю остальные поля для новых структур...
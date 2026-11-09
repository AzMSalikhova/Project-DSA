import pandas as pd
from sqlalchemy import select, func
from app.database import Base, engine, SessionLocal
from app.models.flights import Flight
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = BASE_DIR / "Airline_Operations_Analytics_Dataset.xlsx"


def init_db():
    Base.metadata.create_all(engine)

    with SessionLocal() as db:
        if db.scalar(select(func.count()).select_from(Flight)) == 0:
            print("Идет загрузка данных из xlsx в БД...")
            if not EXCEL_PATH.exists():
                print(f"Файл {EXCEL_PATH} не найден!")
                return

            df = pd.read_excel(EXCEL_PATH)
            flights = []
            for _, row in df.iterrows():
                flights.append(Flight(
                    flight_id=str(row["Flight_ID"]),
                    airline=str(row["Airline"]),
                    origin_airport=str(row["Origin_Airport"]),
                    destination_airport=str(row["Destination_Airport"]),
                    departure_delay_min=int(row["Departure_Delay_Min"]),
                    aircraft_type=str(row["Aircraft_Type"]),
                    weather_condition=str(row["Weather_Condition"]),
                    passenger_count=int(row["Passenger_Count"]),
                    ticket_revenue_usd=float(row["Ticket_Revenue_USD"])
                ))
            db.add_all(flights)
            db.commit()
            print("БД успешно заполнена!")
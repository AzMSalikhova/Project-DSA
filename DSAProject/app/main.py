from fastapi import FastAPI
from app.init_db import init_db
from app.routers import auth_routers, flights_routers

app = FastAPI(title="Airline CRM")

init_db()
flights_routers.load_structures()

app.include_router(auth_routers.router)
app.include_router(flights_routers.router)
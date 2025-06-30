from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from models.Trip import Trip


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello():
    test = Trip(trip_id="test", start_stop="test", end_stop="test", start_time="test", end_time="test", direction=1)
    await test.save()
    return {"hello": "world"}
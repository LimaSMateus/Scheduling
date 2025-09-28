from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routers import CreateSchedule, OptimizeSchedule


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(CreateSchedule.router)
app.include_router(OptimizeSchedule.router)

@app.get("/")
async def hello():
    return {"hello": "world"}
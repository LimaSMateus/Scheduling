from typing import Optional
from beanie import Document
from pydantic import Field


class Trip(Document):
    trip_set: str
    trip_id: str
    start_stop: str
    end_stop: str
    start_time: str
    end_time: str
    direction: int = Field(gt=0, lt=3)
    schedule_id: Optional[str] = None
    vehicle_block_id: Optional[str] = None

    class Settings:
        name = "trip_collection"
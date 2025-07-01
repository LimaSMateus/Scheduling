from pydantic import Field
from beanie import Document
from typing import Optional

class Schedule(Document):
    trip_set: str
    schedule_name: str
    vehicle_id: Optional[str] = None
    trip_id: Optional[str] = None
    event_type: str
    start_stop: str
    end_stop: str
    start_time: str
    end_time: str
    direction: Optional[int] = Field(gt=0, lt=3)
    distance: float = Field(gt=0)

    class Settings:
        name = "schedule_events"

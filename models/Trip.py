from beanie import Document
from pydantic import Field


class Trip(Document):
    trip_set: str
    trip_id: str
    route: str
    start_stop: str
    end_stop: str
    start_time: str
    end_time: str
    direction: int = Field(gt=0, lt=3)
    distance: float = Field(gt=0)

    class Settings:
        name = "trip_collection"
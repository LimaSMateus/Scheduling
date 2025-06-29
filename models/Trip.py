from beanie import Document


class Trip(Document):
    trip_id: str
    start_stop: str
    end_stop: str
    start_time: str
    end_time: str

    class Settings:
        name = "trip_collection"
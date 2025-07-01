from fastapi import APIRouter, HTTPException
from starlette import status
from models.Schedule import Schedule
from models.Trip import Trip

router = APIRouter()

@router.post("/trip-sets/{trip_set}/create-schedule/{new_schedule_name}", status_code=status.HTTP_201_CREATED)
async def create_schedule(trip_set: str, new_schedule_name: str):
    trip_set_query = await Trip.find(Trip.trip_set == trip_set).to_list()
    schedule_already_exists = await Schedule.find_one(Schedule.trip_set == trip_set, Schedule.schedule_name == new_schedule_name)

    if not trip_set_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip set not found")
    if schedule_already_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Schedule already exists")

    for trip in trip_set_query:
        schedule = Schedule(
            trip_set=trip_set,
            schedule_name=new_schedule_name,
            trip_id=trip.trip_id,
            event_type="service_trip",
            start_stop=trip.start_stop,
            end_stop=trip.end_stop,
            start_time=trip.start_time,
            end_time=trip.end_time,
            direction=trip.direction,
            distance=trip.distance)
        await schedule.save()
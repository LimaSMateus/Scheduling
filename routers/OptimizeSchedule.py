from fastapi import APIRouter
from starlette import status
from models.Schedule import Schedule
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpStatus, LpInteger

router = APIRouter()

DISTANCE_COST = 3
VEHICLE_FIXED_COST = 100


def parse_time(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m


@router.post("/trip-sets/{trip_set}/optimize-schedule/{schedule_name}", status_code=status.HTTP_204_NO_CONTENT)
async def optimize_schedule(trip_set: str, schedule_name: str):
    trips = await Schedule.find(
        Schedule.trip_set == trip_set,
        Schedule.schedule_name == schedule_name
    ).to_list()

    n = len(trips)
    if n == 0:
        return

    for trip in trips:
        trip.vehicle_id = None

    trips.sort(key=lambda t: parse_time(t.start_time))

    prob = LpProblem("VehicleScheduling", LpMinimize)

    # Decision variables
    x = {
        (i, j): LpVariable(f"x_{i}_{j}", cat=LpBinary)
        for i in range(n) for j in range(n)
        if i != j
        and trips[i].end_stop == trips[j].start_stop
        and parse_time(trips[i].end_time) <= parse_time(trips[j].start_time)
    }

    y = [LpVariable(f"y_{i}", cat=LpBinary) for i in range(n)]  # trip i starts a vehicle
    u = [LpVariable(f"u_{i}", lowBound=0, upBound=n, cat=LpInteger) for i in range(n)]

    # Objective: minimize distance + vehicle usage
    prob += (
        lpSum(x[i, j] * DISTANCE_COST * trips[i].distance for (i, j) in x) +
        lpSum(y[i] * VEHICLE_FIXED_COST for i in range(n))
    )

    # Each trip must be entered once (from another or from y)
    for j in range(n):
        prob += lpSum(x[i, j] for i in range(n) if (i, j) in x) + y[j] == 1

    # Each trip has at most one outgoing connection
    for i in range(n):
        prob += lpSum(x[i, j] for j in range(n) if (i, j) in x) <= 1

    # Subtour elimination via MTZ constraints
    for i in range(1, n):
        for j in range(1, n):
            if (i, j) in x:
                prob += u[i] + 1 <= u[j] + (1 - x[i, j]) * n

    # Solve
    prob.solve()

    if LpStatus[prob.status] != "Optimal":
        raise Exception("No optimal solution found.")

    # Build trips
    successors = {}
    for (i, j), var in x.items():
        if var.varValue == 1:
            successors[i] = j

    assigned = [False] * n
    vehicle_counter = 0

    for i in range(n):
        if assigned[i] or y[i].varValue != 1:
            continue

        chain = []
        current = i
        while True:
            chain.append(current)
            assigned[current] = True
            next_trip = successors.get(current)
            if next_trip is None or assigned[next_trip]:
                break
            current = next_trip

        vehicle_block_id = f"V{vehicle_counter}"
        vehicle_counter += 1
        for idx in chain:
            trips[idx].vehicle_id = vehicle_block_id
            await trips[idx].save()

# from fastapi import FastAPI
# import uvicorn
# from src.app.api.lifespan import lifespan
# from src.app.api.routes import router
from src.app.services.seats_aero.models import SeatAvailability
from src.app.services.seats_aero.seats_aero import fetch_seat_availability

# app = FastAPI(lifespan=lifespan)

# app.include_router(router)

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    data = SeatAvailability(
        origin_airport="GRU",
        destination_airport="IAH",
        cabin="",
        start_date="2025-04-16",
        end_date="2026-04-16",
        only_direct_flights=False,
        carrier="UA"
    )

    fetch_seat_availability(data)
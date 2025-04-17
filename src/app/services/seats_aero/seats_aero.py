
import requests
import os
import json
from dotenv import load_dotenv
from src.app.redis.redis import redis_client
from src.app.services.seats_aero.models import SeatAvailability, AvailabilityResponse, RouteType

load_dotenv()

PARTNER_AUTHORIZATION = os.getenv("PARTNER_AUTHORIZATION")

# # URL da API
url = "https://seats.aero/"

# # Headers da requisição
headers = {
    "Partner-Authorization": PARTNER_AUTHORIZATION, 
    "Accept": "application/json"
}

def fetch_seat_availability(seat_information: SeatAvailability) -> None:
    routes_from_redis = redis_client.get("hst:routes")  # string JSON

    if routes_from_redis:
        parsed_routes = json.loads(routes_from_redis)  # isso vira uma list[dict]

        # Valida cada item da lista com o Pydantic
        routes = [RouteType.model_validate(route) for route in parsed_routes]
    else:
        print("Nenhuma Rota Encontrada no Redis")

    for route in routes:
        if(route.active):
            request_url = (
                f"{url}/partnerapi/search?"
                f"origin_airport={route.airports[0].airport_code}&"
                f"destination_airport={route.airports[1].airport_code}&"
                f"cabin={seat_information.cabin}&"
                f"start_date={seat_information.start_date}&"
                f"end_date={seat_information.end_date}&"
                f"take={1000}&"
                f"order_by={"lowest_mileage"}&"
                f"skip={0}&"
                f"only_direct_flights={seat_information.only_direct_flights}&"
                f"carriers={seat_information.carrier}&"
                )

            # Faz a requisição GET
            response = requests.get(request_url, headers=headers)

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                # Converte a resposta para JSON
                data = AvailabilityResponse.model_validate(response.json())
                print(data.hasMore)
            else:
                print(f"Erro na requisição: {response.status_code}")
                print(response.text)
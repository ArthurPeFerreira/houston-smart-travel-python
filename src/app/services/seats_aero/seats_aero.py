
import requests
import os
from dotenv import load_dotenv
from models import SeatAvailability, AvailabilityResponse
# from src.app.services.seats_aero.models import SeatAvailability, AvailabilityResponse

load_dotenv()

PARTNER_AUTHORIZATION = os.getenv("PARTNER_AUTHORIZATION")

# # URL da API
url = "https://seats.aero/partnerapi/search"

# # Headers da requisição
headers = {
    "Partner-Authorization": PARTNER_AUTHORIZATION, 
    "Accept": "application/json"
}

def fetch_seat_availability(seat_information: SeatAvailability) -> None:
    # Parâmetros da requisição
    params = {
        "origin_airport": seat_information.origin_airport,  # Aeroporto de origem
        "destination_airport": seat_information.destination_airport,  # Aeroporto de destino
        "cabin": seat_information.cabin,  # Classe de cabine
        "start_date": seat_information.start_date,  # Data de início
        "end_date": seat_information.end_date,  # Data de término
        "cursor": 0,
        "take": 1000,  # Número máximo de resultados
        "order_by": "lowest_mileage",  # Ordenar por menor milhagem
        "skip": 0,
        "include_trips": False,
        "only_direct_flights": seat_information.only_direct_flights,
        "carriers": "",
    }

    # # Faz a requisição GET
    response = requests.get(url, params=params, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Converte a resposta para JSON
        data = AvailabilityResponse.model_validate(response.json())
        print(data.data[0])
    else:
        print(f"Erro na requisição: {response.status_code}")
        print(response.text)


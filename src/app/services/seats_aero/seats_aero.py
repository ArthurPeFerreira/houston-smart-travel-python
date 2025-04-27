import requests
import os
import json
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from src.app.services.redis.redis import redis_client
from src.app.services.seats_aero.models import AvailabilityResponse, RouteType, FlightsAvailability
from src.app.services.seats_aero.mileage_programs import mileage_programs
from src.app.services.database.insert_routes_data import insert_routes_data
from src.app.services.database.reset_routes_data import reset_routes_data
from typing import List

load_dotenv()

PARTNER_AUTHORIZATION = os.getenv("PARTNER_AUTHORIZATION")

# # URL da API
url = "https://seats.aero"

# # Headers da requisição
headers = {
    "Partner-Authorization": PARTNER_AUTHORIZATION, 
    "Accept": "application/json"
}

def fetch_seat_availability() -> None:
    reset_routes_data()

    routes_from_redis = redis_client.get("hst:routes") 

    if routes_from_redis:
        parsed_routes = json.loads(routes_from_redis)

        routes = [RouteType.model_validate(route) for route in parsed_routes]

        date_today = date.today()
        date_1year = date_today + relativedelta(years=1)
        
        date_today_str = date_today.strftime("%Y-%m-%d")
        date_1year_str = date_1year.strftime("%Y-%m-%d")

        for route in routes:
            if(route.active):
                for direction in ["outbound", "return"]:
                    if direction == "outbound":
                        origin_airport = route.airports[0].airport_code
                        destination_airport = route.airports[1].airport_code
                    else:  # direction == "outbound"
                        origin_airport = route.airports[1].airport_code
                        destination_airport = route.airports[0].airport_code

                    print(f"Rota {route.id} | {origin_airport} -> {destination_airport} | Programa de Milhas: {route.mileage_program}")
                    for cabin in route.cabins:              
                        print(f"Cabine: {cabin.key}")
                        
                        request_url = (
                            f"{url}/partnerapi/search?"
                            f"origin_airport={origin_airport}&"
                            f"destination_airport={destination_airport}&"
                            f"cabin={cabin.key}&"
                            f"start_date={date_today_str}&"
                            f"end_date={date_1year_str}&"
                            f"take={1000}&"
                            f"order_by={"lowest_mileage"}&"
                            f"skip={0}&"
                            f"only_direct_flights={not route.enable_layovers}&"
                            f"carriers={mileage_programs[route.mileage_program].iataCode}&"
                            )
                        
                        # Faz a requisição GET
                        response = requests.get(request_url, headers=headers)

                        
                        # Verifica se a requisição foi bem-sucedida
                        if response.status_code == 200:
                            # Converte a resposta para JSON
                            data = AvailabilityResponse.model_validate(response.json())

                            seat_availability_list = data.data

                            while data.hasMore:                         
                                # Atualiza a URL para a próxima página de resultados
                                request_url = f"{url}{data.moreURL}" 
                                
                                # Faz a requisição GET novamente
                                response = requests.get(request_url, headers=headers)
                                
                                # Verifica se a requisição foi bem-sucedida
                                if response.status_code == 200:
                                    data = AvailabilityResponse.model_validate(response.json())

                                    seat_availability_list.extend(data.data)
                                else:
                                    print(f"Erro na requisição: {response.status_code}")
                                    print(response.text)
                                    break
                            

                            seat_availability_to_save : List[FlightsAvailability] = []

                            for seat_availability in seat_availability_list:
                                match cabin.key:
                                    case "economy":
                                        if seat_availability.YDirect and int(seat_availability.YDirectMileageCost) <= cabin.maximum_points and int(seat_availability.YDirectRemainingSeats) > 0:
                                                seat_availability_to_save.append(
                                                    FlightsAvailability(
                                                        routeId=route.id,
                                                        cabin_key=cabin.key,
                                                        date=seat_availability.Date,
                                                        direct=True,
                                                        origin_airport=origin_airport,
                                                        destination_airport=destination_airport,
                                                        seats=seat_availability.YDirectRemainingSeats,
                                                    )
                                                )
                                        else:
                                            if route.enable_layovers:
                                                if seat_availability.YAvailable and int(seat_availability.YMileageCost) <= cabin.maximum_points and int(seat_availability.YRemainingSeats) > 0:
                                                    seat_availability_to_save.append(
                                                        FlightsAvailability(
                                                            routeId=route.id,
                                                            cabin_key=cabin.key,
                                                            date=seat_availability.Date,
                                                            direct=False,
                                                            origin_airport=origin_airport,
                                                            destination_airport=destination_airport,
                                                            seats=seat_availability.YRemainingSeats,
                                                        )
                                                    )
                                            
                                    case "business":
                                        if seat_availability.JDirect and int(seat_availability.JDirectMileageCost) <= cabin.maximum_points and int(seat_availability.JDirectRemainingSeats) > 0:
                                                seat_availability_to_save.append(
                                                    FlightsAvailability(
                                                        routeId=route.id,
                                                        cabin_key=cabin.key,
                                                        date=seat_availability.Date,
                                                        direct=True,
                                                        origin_airport=origin_airport,
                                                        destination_airport=destination_airport,
                                                        seats=seat_availability.JDirectRemainingSeats,
                                                    )
                                                )
                                        else:
                                            if route.enable_layovers:
                                                if seat_availability.JAvailable and int(seat_availability.JMileageCost) <= cabin.maximum_points and int(seat_availability.JRemainingSeats) > 0:
                                                    seat_availability_to_save.append(
                                                        FlightsAvailability(
                                                            routeId=route.id,
                                                            cabin_key=cabin.key,
                                                            date=seat_availability.Date,
                                                            direct=False,
                                                            origin_airport=origin_airport,
                                                            destination_airport=destination_airport,
                                                            seats=seat_availability.JRemainingSeats,
                                                        )
                                                    )

                                    case "first":
                                        if seat_availability.FDirect and int(seat_availability.FDirectMileageCost) <= cabin.maximum_points and int(seat_availability.FDirectRemainingSeats) > 0:
                                                seat_availability_to_save.append(
                                                    FlightsAvailability(
                                                        routeId=route.id,
                                                        cabin_key=cabin.key,
                                                        date=seat_availability.Date,
                                                        direct=True,
                                                        origin_airport=origin_airport,
                                                        destination_airport=destination_airport,
                                                        seats=seat_availability.FDirectRemainingSeats,
                                                    )
                                                )
                                        else:
                                            if route.enable_layovers:
                                                if seat_availability.FAvailable and int(seat_availability.FMileageCost) <= cabin.maximum_points and int(seat_availability.FRemainingSeats) > 0:
                                                    seat_availability_to_save.append(
                                                        FlightsAvailability(
                                                            routeId=route.id,
                                                            cabin_key=cabin.key,
                                                            date=seat_availability.Date,
                                                            direct=False,
                                                            origin_airport=origin_airport,
                                                            destination_airport=destination_airport,
                                                            seats=seat_availability.FRemainingSeats,
                                                        )
                                                    )

                                    case "premium":
                                        if seat_availability.WDirect and int(seat_availability.WDirectMileageCost) <= cabin.maximum_points and int(seat_availability.WDirectRemainingSeats) > 0:
                                                seat_availability_to_save.append(
                                                    FlightsAvailability(
                                                        routeId=route.id,
                                                        cabin_key=cabin.key,
                                                        date=seat_availability.Date,
                                                        direct=True,
                                                        origin_airport=origin_airport,
                                                        destination_airport=destination_airport,
                                                        seats=seat_availability.WDirectRemainingSeats,
                                                    )
                                                )
                                        else:
                                            if route.enable_layovers:
                                                if seat_availability.WAvailable and int(seat_availability.WMileageCost) <= cabin.maximum_points and int(seat_availability.WRemainingSeats) > 0:
                                                    seat_availability_to_save.append(
                                                        FlightsAvailability(
                                                            routeId=route.id,
                                                            cabin_key=cabin.key,
                                                            date=seat_availability.Date,
                                                            direct=False,
                                                            origin_airport=origin_airport,
                                                            destination_airport=destination_airport,
                                                            seats=seat_availability.WRemainingSeats,
                                                        )
                                                    )

                            insert_routes_data([(
                                seat.routeId,
                                seat.cabin_key,
                                seat.date,
                                seat.direct,
                                seat.origin_airport,
                                seat.destination_airport,
                                seat.seats
                            ) for seat in seat_availability_to_save])
                                    
                        else:
                            print(f"Erro na requisição: {response.status_code}")
                            print(response.text)
    else:
        print("Nenhuma Rota Encontrada no Redis")
        return
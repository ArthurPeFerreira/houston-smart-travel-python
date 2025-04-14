import requests

# URL da API
url = "https://seats.aero/partnerapi/availability"

# Parâmetros da requisição
params = {
    "origin_airport": "GRU",  # Aeroportos de origem
    "destination_airport": "IAH",  # Aeroportos de destino
    "cabin": "economy",  # Classe de cabine
    "start_date": "2025-03-01",  # Data de início
    "end_date": "2026-03-01",  # Data de término
    "origin_region":"South America",
    "destination_region":"",
    "take": 1000,  # Número máximo de resultados
    "order_by": "lowest_mileage",  # Ordenar por menor milhagem
    "direct_only": "true"
}

# Headers da requisição (se necessário)
headers = {
    "Partner-Authorization": "pro_2qTufZqd6oNYUjOaOyCn1AvQzB9",  # Substitua pelo seu token de API
    "Accept": "application/json"
}

# Faz a requisição GET
response = requests.get(url, params=params, headers=headers)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Converte a resposta para JSON
    data = response.json()
    print(data)
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)
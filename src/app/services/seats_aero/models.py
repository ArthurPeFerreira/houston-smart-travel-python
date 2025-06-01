from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal

class RouteModel(BaseModel):
    ID: str
    OriginAirport: str
    OriginRegion: str
    DestinationAirport: str
    DestinationRegion: str
    NumDaysOut: int
    Distance: int
    Source: str

class AvailabilityModel(BaseModel):
    ID: str
    RouteID: str
    Route: RouteModel
    Date: str
    ParsedDate: str

    YAvailable: bool
    WAvailable: bool
    JAvailable: bool
    FAvailable: bool

    YAvailableRaw: bool
    WAvailableRaw: bool
    JAvailableRaw: bool
    FAvailableRaw: bool

    YMileageCost: str
    WMileageCost: str
    JMileageCost: str
    FMileageCost: str

    YMileageCostRaw: int
    WMileageCostRaw: int
    JMileageCostRaw: int
    FMileageCostRaw: int

    YDirectMileageCost: int
    WDirectMileageCost: int
    JDirectMileageCost: int
    FDirectMileageCost: int

    YDirectMileageCostRaw: int
    WDirectMileageCostRaw: int
    JDirectMileageCostRaw: int
    FDirectMileageCostRaw: int

    TaxesCurrency: str
    YTotalTaxes: int
    WTotalTaxes: int
    JTotalTaxes: int
    FTotalTaxes: int

    YTotalTaxesRaw: int
    WTotalTaxesRaw: int
    JTotalTaxesRaw: int
    FTotalTaxesRaw: int

    YDirectTotalTaxes: int
    WDirectTotalTaxes: int
    JDirectTotalTaxes: int
    FDirectTotalTaxes: int

    YDirectTotalTaxesRaw: int
    WDirectTotalTaxesRaw: int
    JDirectTotalTaxesRaw: int
    FDirectTotalTaxesRaw: int

    YRemainingSeats: int
    WRemainingSeats: int
    JRemainingSeats: int
    FRemainingSeats: int

    YRemainingSeatsRaw: int
    WRemainingSeatsRaw: int
    JRemainingSeatsRaw: int
    FRemainingSeatsRaw: int

    YDirectRemainingSeats: int
    WDirectRemainingSeats: int
    JDirectRemainingSeats: int
    FDirectRemainingSeats: int

    YDirectRemainingSeatsRaw: int
    WDirectRemainingSeatsRaw: int
    JDirectRemainingSeatsRaw: int
    FDirectRemainingSeatsRaw: int

    YAirlines: str
    WAirlines: str
    JAirlines: str
    FAirlines: str

    YAirlinesRaw: str
    WAirlinesRaw: str
    JAirlinesRaw: str
    FAirlinesRaw: str

    YDirectAirlines: str
    WDirectAirlines: str
    JDirectAirlines: str
    FDirectAirlines: str

    YDirectAirlinesRaw: str
    WDirectAirlinesRaw: str
    JDirectAirlinesRaw: str
    FDirectAirlinesRaw: str

    YDirect: bool
    WDirect: bool
    JDirect: bool
    FDirect: bool

    YDirectRaw: bool
    WDirectRaw: bool
    JDirectRaw: bool
    FDirectRaw: bool

    Source: str
    CreatedAt: str
    UpdatedAt: str
    AvailabilityTrips: Optional[str]


class AvailabilityResponse(BaseModel):
    data: List[AvailabilityModel]
    count: int
    hasMore: bool
    moreURL: Optional[str] = None
    cursor: int

class FlightsAvailability(BaseModel):
    routeId: int
    cabin_key: str
    date: str
    direct: bool
    seats: int
    origin_airport: str
    destination_airport: str
        

class AirportType(BaseModel):
    id: int
    city: str
    airport_code: str = Field(alias="airportCode")

class CabinsType(BaseModel):
    id: int
    key: str
    maximum_points: int = Field(alias="maximumPoints")
    bags_amount: int = Field(alias="bagsAmount")
    passage_price_from_airport_1_to_2: Decimal = Field(alias="passagePriceFromAirport1To2")
    passage_price_from_airport_2_to_1: Decimal = Field(alias="passagePriceFromAirport2To1")
    passage_price_round_trip: Decimal = Field(alias="passagePriceRoundTrip")

class RouteType(BaseModel):
    id: int
    mileage_program: str = Field(alias="mileageProgram")
    enable_layovers: bool = Field(alias="enableLayovers")
    active: bool
    airports: List[AirportType]
    cabins: List[CabinsType]

    class Config:
        populate_by_name = True  # permite usar nomes snake_case no código
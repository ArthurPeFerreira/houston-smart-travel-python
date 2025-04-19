from typing import Literal, Dict
from pydantic import BaseModel

# Define os possíveis valores para as chaves
MileageProgramKey = Literal[
    "eurobonus",
    "virginatlantic",
    "aeromexico",
    "american",
    "delta",
    "etihad",
    "united",
    "emirates",
    "aeroplan",
    "alaska",
    "velocity",
    "qantas",
    "connectmiles",
    "azul",
    "smiles",
    "flyingblue",
    "jetblue",
]

# Modelo Pydantic
class MileageProgram(BaseModel):
    key: str
    iataCode: str

# Dicionário com instâncias do modelo
mileage_programs: Dict[MileageProgramKey, MileageProgram] = {
    "eurobonus": MileageProgram(key="eurobonus", iataCode="SK"),
    "virginatlantic": MileageProgram(key="virginatlantic", iataCode="VS"),
    "aeromexico": MileageProgram(key="aeromexico", iataCode="AM"),
    "american": MileageProgram(key="american", iataCode="AA"),
    "delta": MileageProgram(key="delta", iataCode="DL"),
    "etihad": MileageProgram(key="etihad", iataCode="EY"),
    "united": MileageProgram(key="united", iataCode="UA"),
    "emirates": MileageProgram(key="emirates", iataCode="EK"),
    "aeroplan": MileageProgram(key="aeroplan", iataCode="AC"),
    "alaska": MileageProgram(key="alaska", iataCode="AS"),
    "velocity": MileageProgram(key="velocity", iataCode="VA"),
    "qantas": MileageProgram(key="qantas", iataCode="QF"),
    "connectmiles": MileageProgram(key="connectmiles", iataCode="CM"),
    "azul": MileageProgram(key="azul", iataCode="AD"),
    "smiles": MileageProgram(key="smiles", iataCode="G3"),
    "flyingblue": MileageProgram(key="flyingblue", iataCode="AF"),
    "jetblue": MileageProgram(key="jetblue", iataCode="B6"),
}

from pymongo import MongoClient
from typing import Optional
from pydantic import BaseModel

class Car(BaseModel):
    _id: Optional[str] 
    property: str
    brand: str
    model: str
    licensePlate: str

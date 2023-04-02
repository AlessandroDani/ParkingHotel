from fastapi import FastAPI, APIRouter,HTTPException, status, Depends
from db.models.schemas import Car
from db.schemas.cars import car_schema, cars_list_schema
from db.client import dbClient
from bson.objectid import ObjectId

# app = FastAPI()

router = APIRouter(prefix="/carsdb", tags=["carsdb"], responses=({status.HTTP_404_NOT_FOUND: {"message": "carro no encontrado"}}))


@router.get("/")
async def cars():
    return cars_list_schema(dbClient.cars.find())

@router.get("/{licensePlate}")
async def getCar(licensePlate: str):
    return searchCar(licensePlate)

@router.post("/")
async def postCar(car: Car):
    newCar = searchCar(car.licensePlate)
    if type(newCar) == Car:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Carro ya existe")
    
    carDict = car.dict()
    id = dbClient.cars.insert_one(carDict).inserted_id

    return Car(**carDict)


@router.put("/")
async def putCar(car: Car):
    try:
        car = dbClient.cars.find_one_and_replace({"licensePlate" : car.licensePlate})
        return Car(**car)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el vehículo")


@router.delete("/{licensePlate}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteCar(licensePlate: str):
    found = dbClient.cars.find_one_and_delete({"licensePlate" : licensePlate})

    if not found:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Carro no se encuentra")

def searchCar(licensePlate: str):
    try:
        car = dbClient.cars.find_one({"licensePlate" : licensePlate})
        if car == None:
            return car
        return Car(**car_schema(car))
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No se ha encontrado el vehiculo")
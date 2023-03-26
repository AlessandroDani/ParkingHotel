from fastapi import FastAPI, APIRouter,HTTPException, status, Depends
from db.models.schemas import Car
from db.schemas.cars import car_schema
from db.client import dbClient

app = FastAPI()

#class Car(car: Car):
 #   time: str

router = APIRouter(prefix="/carsdb", tags="carsdb", responses=({status.HTTP_404_NOT_FOUND: {"message": "carro no encontrado"}}))


carList = []

def searchCar(licensePlate: str):
    for carFound in carList:
        if carFound.licensePlate == licensePlate:
             return carFound
                 #carFound = filter(lambda car: car.licensePlate == licensePlate, carList)
    if not carFound:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No se ha encontrado el vehiculo")

@app.get("/")
async def cars():
    return carList

@app.get("/{licensePlate}")
async def getCar(licensePlate: str):
    return searchCar(licensePlate)

@app.post("/")

async def postCar(car: Car):
 #   if type(searchCar(car.licensePlate)) == Car:
  #      raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Carro ya existe")

    #carList.append(car)
    carDict = dict (car)
    del carDict["_id"]
    id = dbClient.cars.insert_one(car).inserted_id

    newCar = car_schema(dbClient.cars.find_one({"_id": id}))


    return Car(**newCar)

@app.put("/")
async def postCar(car: Car):
    for i in range(len(carList)):
        if car.licensePlate == carList[i].licensePlate:
            carList[i] = car
            return car
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el vehículo")

@app.delete("/{licensePlate}")
async def postCar(car: Car):
    if type(searchCar(car.licensePlate)) == Car:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Carro no se encuentra")

    for i in range(len(carList)):
        if car.licensePlate == carList[i].licensePlate:
            del carList[i]
            return carList

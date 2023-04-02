from fastapi import FastAPI, APIRouter,HTTPException, status, Depends
from db.models.schemas import Car
from src.routers import carsDB

app = FastAPI()

#Routers
app.include_router(carsDB.router)

carList = []
    #Car(id = "1", property= "Alessandro", brand = "Chevrolet", model = "Aveo", licensePlate = "AFE1INF"),
    #Car(id = "2", property= "Arnoldo", brand = "Mazda", model = "3", licensePlate = "ALORNEDC"),
    #Car(id = "3", property= "Umberto", brand = "Mercedes", model = "Benz", licensePlate = "KENCHDMA"),
    #Car(id = "4", property= "Alfonso", brand = "Honda", model = "x4", licensePlate = "PON54B"),
    #Car(id = "5", property= "Alberto", brand = "Ford", model = "Fiesta", licensePlate = "TUENSHF3")]

def searchCar(licensePlate: str):
    for carFound in carList:
        if carFound.licensePlate == licensePlate:
             return carFound
                 #carFound = filter(lambda car: car.licensePlate == licensePlate, carList)
    if not carFound:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No se ha encontrado el vehiculo")

@app.get("/cars")
async def cars():
    return carList

@app.get("/car/{licensePlate}")
async def getCar(licensePlate: str):
    return searchCar(licensePlate)

@app.post("/car")
async def postCar(car: Car):
    if type(searchCar(car.licensePlate)) == Car:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Carro ya existe")

    carList.append(car)
    return car

@app.put("/car")
async def postCar(car: Car):
    for i in range(len(carList)):
        if car.licensePlate == carList[i].licensePlate:
            carList[i] = car
            return car
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el vehículo")

@app.delete("/car/{licensePlate}")
async def postCar(car: Car):
    if type(searchCar(car.licensePlate)) == Car:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Carro no se encuentra")

    for i in range(len(carList)):
        if car.licensePlate == carList[i].licensePlate:
            del carList[i]
            return carList

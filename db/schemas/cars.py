def car_schema(car) -> dict:
    return {"_id": str(car["_id"]),
            "owner" : car["owner"],
            "brand" : car["brand"],
            "model" : car["model"],
            "licensePlate" : car["licensePlate"]
            }

def cars_list_schema(cars) -> list:
    return [car_schema(car) for car in cars]
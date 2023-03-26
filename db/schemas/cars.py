def car_schema(car) -> dict:
    return {"_id": str(car["_id"]),
            "property" : car["property"],
            "brand" : car["brand"],
            "model" : car["model"],
            "licensePlate" : car["licensePlate"]
            }
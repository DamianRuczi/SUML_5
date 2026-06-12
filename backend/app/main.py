"""FastAPI application exposing the Titanic model."""

from fastapi import FastAPI
from pydantic import BaseModel

from . import model_service


app = FastAPI(title="Titanic Survival API")


class Passenger(BaseModel):
    pclass: int
    age: float
    sibsp: int
    parch: int
    fare: float
    sex: str
    embarked: str


class TrainingPassenger(Passenger):
    survived: int


@app.post("/api/predict")
def predict(passenger: Passenger):
    return model_service.predict(passenger.model_dump())


@app.post("/api/train")
def train(passenger: TrainingPassenger):
    return model_service.train(passenger.model_dump())


@app.get("/api/data")
def training_data():
    return model_service.get_training_data()


@app.get("/api/model")
def model_info():
    return model_service.get_model_info()

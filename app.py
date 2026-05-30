import uvicorn
from fastapi import FastAPI, HTTPExecution, Form
from pathlib import Path
from typing import Annotated
from models.point import Point
from libs.model import train_linear_regression_model, predict_target_value


BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_DIR = Path(BASE_DIR).joinpath("ml_models")
DATA_DIR = Path(BASE_DIR).joinpath("data")


app = FastAPI()

@app.get("/", tags=["intro"])
def index():
    return {"message": "Linear Regression"}


@app.post("/model/train")
async def train_model():
    return {"message": "Should train model"}
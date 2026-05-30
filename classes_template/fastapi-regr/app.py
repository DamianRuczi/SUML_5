import uvicorn
from fastapi import FastAPI, HTTPException, Form
from typing import Annotated
from pathlib import Path

from models.point import Point
from libs.model import predict, train

BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_DIR = Path(BASE_DIR).joinpath("ml_models")
DATA_DIR = Path(BASE_DIR).joinpath("data")

app = FastAPI()


@app.get("/", tags=["intro"])
def index():
    return {'message': 'Linear Regression ML'}


@app.post("/model/point", tags=["data"], response_model=Point, status_code=200)
async def point(x: Annotated[float, Form()], y: Annotated[float, Form()]):
    return Point(x=x, y=y)


@app.post("/model/train", tags=["model"], status_code=200)
async def train_model(data: Point, data_name="10_points", model_name="our_model"):
    data_file = Path(DATA_DIR).joinpath(f"{data_name}.csv")
    model_file = Path(MODEL_DIR).joinpath(f"{model_name}.pkl")

    train(data.x, data.y, data_file, model_file)

    return {"model_fit": "OK", "model_save": "OK"}


@app.post("/model/predict", tags=["model"], response_model=Point, status_code=200)
async def get_prediction(data: Point, model_name="our_model"):
    model_file = Path(MODEL_DIR).joinpath(f"{model_name}.pkl")

    if not model_file.exists():
        raise HTTPException(status_code=400, detail="Model not found.")

    data.y = predict(data.x, model_file)

    return {"x": data.x, "y": data.y}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8008)
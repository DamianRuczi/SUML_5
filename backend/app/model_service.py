"""Functions used to work with the Titanic model."""

import pickle
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "DSP_6.csv"
MODEL_PATH = PROJECT_ROOT / "artifacts" / "model.pkl"

FEATURE_COLUMNS = [
    "Pclass",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Sex_male",
    "Embarked_Q",
    "Embarked_S",
]


def load_model() -> LogisticRegression:
    with MODEL_PATH.open("rb") as file:
        return pickle.load(file)


def passenger_to_features(passenger: dict) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Pclass": passenger["pclass"],
                "Age": passenger["age"],
                "SibSp": passenger["sibsp"],
                "Parch": passenger["parch"],
                "Fare": passenger["fare"],
                "Sex_male": int(passenger["sex"] == "male"),
                "Embarked_Q": int(passenger["embarked"] == "Q"),
                "Embarked_S": int(passenger["embarked"] == "S"),
            }
        ],
        columns=FEATURE_COLUMNS,
    )


def prepare_training_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    model_data = data[
        ["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare", "Sex", "Embarked"]
    ].copy()

    model_data["Age"] = model_data["Age"].fillna(model_data["Age"].median())
    model_data["Fare"] = model_data["Fare"].fillna(model_data["Fare"].median())
    model_data["Embarked"] = model_data["Embarked"].fillna(
        model_data["Embarked"].mode()[0]
    )

    model_data["Sex_male"] = (model_data["Sex"] == "male").astype(int)
    model_data["Embarked_Q"] = (model_data["Embarked"] == "Q").astype(int)
    model_data["Embarked_S"] = (model_data["Embarked"] == "S").astype(int)

    return model_data[FEATURE_COLUMNS], model_data["Survived"]


def predict(passenger: dict) -> dict:
    model = load_model()
    features = passenger_to_features(passenger)

    return {
        "prediction": int(model.predict(features)[0]),
        "survival_probability": float(model.predict_proba(features)[0, 1]),
    }


def train(passenger: dict) -> dict:
    data = pd.read_csv(DATA_PATH)
    passenger_id = int(data["PassengerId"].max()) + 1

    data.loc[len(data)] = {
        "PassengerId": passenger_id,
        "Survived": passenger["survived"],
        "Pclass": passenger["pclass"],
        "Name": f"API Passenger {passenger_id}",
        "Sex": passenger["sex"],
        "Age": passenger["age"],
        "SibSp": passenger["sibsp"],
        "Parch": passenger["parch"],
        "Ticket": f"API-{passenger_id}",
        "Fare": passenger["fare"],
        "Cabin": None,
        "Embarked": passenger["embarked"],
    }

    features, target = prepare_training_data(data)
    model = LogisticRegression(max_iter=500)
    model.fit(features, target)

    data.to_csv(DATA_PATH, index=False)
    with MODEL_PATH.open("wb") as file:
        pickle.dump(model, file)

    return {
        "message": "Nowy rekord został dodany, a model ponownie wytrenowany.",
        "training_rows": len(data),
        "prediction": predict(passenger),
    }


def get_training_data() -> dict:
    data = pd.read_csv(DATA_PATH)
    records = data.astype(object).where(pd.notna(data), None).to_dict(orient="records")
    return {"row_count": len(data), "records": records}


def get_model_info() -> dict:
    model = load_model()
    return {
        "type": type(model).__name__,
        "features": list(model.feature_names_in_),
        "classes": [int(value) for value in model.classes_],
        "intercept": float(model.intercept_[0]),
        "coefficients": [
            {"feature": feature, "coefficient": float(coefficient)}
            for feature, coefficient in zip(model.feature_names_in_, model.coef_[0])
        ],
        "parameters": model.get_params(),
    }

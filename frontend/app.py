"""Streamlit interface for the Titanic survival API."""

import streamlit as st
import requests
import os


API_URL = os.getenv("API_URL", "http://localhost:8000")



def predict(passenger):
    return requests.post(f"{API_URL}/api/predict", json=passenger, timeout=10).json()


def train(passenger):
    return requests.post(f"{API_URL}/api/train", json=passenger, timeout=30).json()

st.set_page_config(
    page_title="Predykcja przeżycia na Titanicu",
    layout="centered",
)

def passenger_fields(prefix: str) -> dict[str, object]:
    """Render passenger fields and return an API-ready payload."""
    first_column, second_column = st.columns(2)

    with first_column:
        pclass = st.selectbox(
            "Klasa pasażera",
            options=[1, 2, 3],
            key=f"{prefix}_pclass",
        )
        age = st.number_input(
            "Wiek",
            min_value=0.0,
            max_value=120.0,
            value=30.0,
            step=1.0,
            key=f"{prefix}_age",
        )
        sibsp = st.number_input(
            "Liczba rodzeństwa lub małżonków",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key=f"{prefix}_sibsp",
        )
        parch = st.number_input(
            "Liczba rodziców lub dzieci",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key=f"{prefix}_parch",
        )

    with second_column:
        fare = st.number_input(
            "Cena biletu",
            min_value=0.0,
            value=20.0,
            step=1.0,
            key=f"{prefix}_fare",
        )
        sex = st.radio(
            "Płeć",
            options=["female", "male"],
            format_func=lambda value: "kobieta" if value == "female" else "mężczyzna",
            horizontal=True,
            key=f"{prefix}_sex",
        )
        embarked = st.selectbox(
            "Port zaokrętowania",
            options=["C", "Q", "S"],
            format_func=lambda value: {
                "C": "Cherbourg (C)",
                "Q": "Queenstown (Q)",
                "S": "Southampton (S)",
            }[value],
            key=f"{prefix}_embarked",
        )

    return {
        "pclass": pclass,
        "age": age,
        "sibsp": sibsp,
        "parch": parch,
        "fare": fare,
        "sex": sex,
        "embarked": embarked,
    }


def show_prediction(result: dict[str, object]) -> None:
    prediction = int(result["prediction"])
    probability = float(result["survival_probability"])

    if prediction == 1:
        st.success("Model przewiduje, że pasażer przeżyje.")
    else:
        st.warning("Model przewiduje, że pasażer nie przeżyje.")

    st.metric("Prawdopodobieństwo przeżycia", f"{probability:.2%}")


st.title("Predykcja przeżycia pasażera Titanica")
st.caption("Interfejs komunikuje się z modelem przez backend FastAPI.")

prediction_tab, training_tab = st.tabs(["Predykcja", "Dotrenowanie modelu"])

with prediction_tab:
    st.subheader("Sprawdź prawdopodobieństwo przeżycia")

    with st.form("prediction_form"):
        prediction_payload = passenger_fields("prediction")
        predict_submitted = st.form_submit_button(
            "Wykonaj predykcję",
            type="primary",
        )

    if predict_submitted:
        show_prediction(predict(prediction_payload))

with training_tab:
    st.subheader("Dodaj oznaczonego pasażera")
    st.info(
        "Rekord zostanie dopisany do zbioru danych, a model ponownie wytrenowany."
    )

    with st.form("training_form"):
        training_payload = passenger_fields("training")
        survived = st.radio(
            "Rzeczywisty wynik",
            options=[0, 1],
            format_func=lambda value: "przeżył" if value == 1 else "nie przeżył",
            horizontal=True,
            key="training_survived",
        )
        train_submitted = st.form_submit_button(
            "Dodaj rekord i wytrenuj model",
            type="primary",
        )

    if train_submitted:
        result = train({**training_payload, "survived": survived})
        st.success(result["message"])
        st.write(f"Liczba rekordów treningowych: **{result['training_rows']}**")
        show_prediction(result["prediction"])

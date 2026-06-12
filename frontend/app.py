import streamlit as st
import pickle
import numpy as np

st.title("Predykcja przeżycia pasażera na katastrofie statku titanic")

try:
    with open("model.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    st.success("Wczytano model")


except Exception as e:
    st.error(f"Błąd wczytywania modelu: {e}")
    st.stop()



pclass = st.selectbox("PClass", [1, 2, 3])
age = st.slider("Age")
sibsp = st.slider("SibSp")
parch = st.slider("Parch")
fare = st.slider("Fare")

sex_d = {0: 'male', 1: 'female'}
sex_male = st.radio("Sex", options=sex_d.keys(), format_func=lambda x: sex_d[x])


embarked = st.selectbox("Embarked", ["C", "Q", "S"])
embarked_q = 1 if embarked == "Q" else 0
embarked_s = 1 if embarked == "S" else 0


if st.button("Sprawdź prawdopodobieństwo przeżycia"):
    try:
        features = np.array([[pclass, age, sibsp, parch, fare, sex_male, embarked_q, embarked_s]])

        prediction = loaded_model.predict(features)[0]
        probability = loaded_model.predict_proba(features)[0][1]

        st.write(f"Wynik predykcji (0 = nie przeżył, 1 = przeżył): **{prediction}**")
        st.write(f"Prawdopodobieństwo przeżycia: **{probability:.2%}**")

        if prediction == 1:
            st.balloons()
    except Exception as e:
        st.error(f"Błąd podczas predykcji: {e}")
# To będzie model - architektura aplikacji. To powinny znaleźć się te funkcję która trenuje i funkcja która dokonuje predykcji.


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

print("hello world, here is Ml model")

def train_linear_regression_model(csv_path, pickle_path = "our_model.pkl"):
    df = pd.read_csv(csv_path)
    X = df['x'].values.reshape(-1,1) # values converts it into a numpy array
    y = df['y'].values.reshape(-1,1) # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, y)
    pickle.dump(linear_regressor, open(pickle_path, 'wb'))

train_linear_regression_model('data/10_points.csv')


import numpy as np
import pickle

def predict_target_value(x, pickle_path = "our_model.pkl"):
    lr_model = pickle.load(open(pickle_path, 'rb'))
    input = np.array([x]).reshape(-1,1)
    prediction = lr_model.predict(input.reshape(-1,1))
    return prediction[0].reshape(1,-1).flatten()[0]


print(predict_target_value(4))
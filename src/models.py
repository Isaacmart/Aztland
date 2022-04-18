import tensorflow as tf
from tensorflow import keras
import pandas as pd

data = pd.read_csv("../../model_data_test/eth-usd.csv")

n = len(data)
train = data[0:int(n*0.7)]
val = data[int(n*0.7):int(n*0.9)]
test = data[int(n*0.9):]


model = keras.Sequentila([
    keras.layer.Dense(units=26, activation='relu'),
    keras.layer.Dense(units=20, activation='relu'),
    kera.layer.Dense(units=2, activation='softmax')
])

model.com

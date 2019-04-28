import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Activation
import numpy as np

# Dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Formateo
x_train=np.expand_dims(x_train,-1)
x_test=np.expand_dims(x_test,-1)

# Parámetros
img_shape = (28,28,1)

# Modelo
model = Sequential()

model.add(Conv2D(filters=64,kernel_size=3,padding="same",input_shape=img_shape))
model.add(Activation("relu"))
model.add(MaxPool2D(2))
model.add(Conv2D(filters=32,kernel_size=3,padding="same"))
model.add(Activation("relu"))
model.add(MaxPool2D(2))
model.add(Flatten())
model.add(Dense(10))
model.add(Activation("softmax"))

model.compile(loss="sparse_categorical_crossentropy", optimizer = "adam", metrics=["acc"])

model.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test,y_test))

model.save("model.h5")
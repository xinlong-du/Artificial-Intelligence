#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 15:50:58 2020

@author: mingyu.liu001

"""
import pickle
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler

with open('mnist_double_data.pickle', 'rb') as f:
    (x_train, y_train), (x_test, y_test) = pickle.load(f)
    
    
batch_size = 128
num_output = 1
epochs = 200

# input image dimensions
img_rows, img_cols = 10, 20
num_pixels = img_rows * img_cols

x_train = x_train.reshape(x_train.shape[0], num_pixels)
x_test = x_test.reshape(x_test.shape[0], num_pixels)
input_shape = (num_pixels,)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

#scale y_train data
y_train /= 99
y_test_unscale = y_test
y_test /= 99


model = Sequential()
model.add(Dense(num_output, input_shape=input_shape, activation='relu'))

model.compile(loss='mean_squared_error',
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])

model.summary()

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))


training  = model.evaluate(x_train, y_train, verbose=0)
print('Training loss:', training[0])
print('Training accuracy:', training[1])

test  = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', test[0])
print('Test accuracy:',test[1])


y_predict = model.predict(x_test)
y_predict_unscale =y_predict*99

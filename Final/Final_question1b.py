#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 16:47:51 2020

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
num_output = 100
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


y_train = keras.utils.to_categorical(y_train, num_output)
y_test = keras.utils.to_categorical(y_test, num_output)

#scale y_train data
#y_train /= 99
#y_test_unscale = y_test
#y_test /= 99


model = Sequential()
# model.add(Dense(num_output, input_shape=input_shape, activation='relu'))

# model.compile(loss='mean_squared_error',
#               optimizer=keras.optimizers.Adam(),
#               metrics=['accuracy'])

model.add(Dense(100, input_shape=input_shape,  activation='relu', name='hidden1'))
model.add(Dense(100, activation='sigmoid', name='hidden2'))
model.add(Dense(num_output,  activation='softmax', name='output'))

model.compile(loss=keras.losses.categorical_crossentropy,
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

y_predict_raw = model.predict(x_test)
y_predict=y_predict_raw.argmax(axis=1)
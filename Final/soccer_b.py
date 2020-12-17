#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignment5 Question 4a

@author: mingyu.liu001
"""

import pickle
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler


with open('soccer_data.pickle', 'rb') as f:
    (x_train, y_train), (x_test, y_test) = pickle.load(f)
    
batch_size = 400
num_output = 4
epochs = 200

input_shape = (22,)

#scale y_train data
scalar = MinMaxScaler()
scalar.fit(y_train)
y_train = scalar.transform(y_train)

#scale y_test data
y_test_unscale = y_test
scalar = MinMaxScaler()
scalar.fit(y_test)
y_test = scalar.transform(y_test)

# build the neural network model
model = Sequential()
model.add(Dense(50, input_shape=input_shape, activation='relu'))
model.add(Dense(50,  activation='relu'))
model.add(Dense(25,  activation='relu'))
model.add(Dense(num_output, activation='relu'))

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
y_predict_unscale =scalar.inverse_transform(y_predict)

y_predict_unscale[:,0]=np.round(y_predict_unscale[:,0])
y_predict_unscale[:,1]=np.round(y_predict_unscale[:,1])

y_error = y_predict_unscale-y_test_unscale

#calculate standard deviation of each variable
score_std = np.std(y_error[:,0])
print('Scored_SD:',score_std)
concede_std = np.std(y_error[:,1])
print('Conceded:',concede_std)
drink_std = np.std(y_error[:,2])
print('Drink_SD:',drink_std)
money_std = np.std(y_error[:,3])
print('Money_SD:',money_std)

#The network structure contains one input layer using relu activation function, three hidden, nonlinear and dense layers using the relu nonlinearity, and an output layer using the relu.
#The reason to use dense layer is that dense layer is the regular deeply connected neural network layer, it can add an interesting non-linearity property by using relu activation function.
#The number of epochs is 200.
#The final MSE for training and test sets are 0.0015 and 0.0056. The final accuracy for training and test sets are 0.8650 and 0.8390.
#The standard deviations of the prediction for each variable are 0.6120, 0.6293, 8.4181 and 137913.7332.
#This network performs better than (a) as it adds some hidden layers that increase a level of nonlinear complexity so that construct complicated nonlinear functions. 
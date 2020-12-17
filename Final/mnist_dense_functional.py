import keras
from keras.layers import Input, Dense, Dropout, Flatten
from keras.datasets import mnist
from keras.models import Sequential
from keras import backend as K
from keras.models import load_model, Model
import matplotlib.pyplot as plt

batch_size = 128
num_classes = 10
epochs = 20

# input image dimensions
img_rows, img_cols = 28, 28
num_pixels = img_rows * img_cols

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

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

# convert class vectors to binary class matrices (i.e., indivdual class indices to desired output vectors)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# build the neural network model
input_layer = Input(shape=input_shape)
hidden_layer = Dense(100, activation='sigmoid', name='hidden')(input_layer)
output_layer = Dense(num_classes,  activation='softmax', name='output')(hidden_layer)

model = Model(inputs=input_layer, outputs=output_layer)

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])

model.summary()

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save('mnist.hdf5', include_optimizer=True)

model2 = load_model('mnist.hdf5')
score = model2.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

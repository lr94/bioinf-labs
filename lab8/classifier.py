#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 8                                                                        #
#                                                                              #
# Luca Robbiano, 244033                                                        #
################################################################################

from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from keras.optimizers import SGD


class ConvolutionalClassifier:

    def __init__(self, learning_rate=0.01, epochs=10):
        self.model = Sequential()
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.sgd = SGD(lr=learning_rate, decay=learning_rate / epochs, nesterov=False)

    def fit(self, x, y):
        self.model.add(Conv1D(filters=128, kernel_size=3, input_shape=(60, 4), activation='relu'))
        self.model.add(MaxPooling1D(pool_size=2))

        self.model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
        self.model.add(MaxPooling1D(pool_size=2))

        self.model.add(Flatten())
        self.model.add(Dense(units=100, activation='relu'))
        self.model.add(Dense(units=len(y[0]), activation='softmax'))

        self.model.compile(optimizer=self.sgd, loss='categorical_crossentropy', metrics=['accuracy'])

        self.model.fit(x, y, batch_size=10, epochs=self.epochs, validation_split=0.1, verbose=True)

    def evaluate(self, x, y, verbose):
        return self.model.evaluate(x, y, verbose=verbose)

    def predict(self, x):
        return self.model.predict(x)

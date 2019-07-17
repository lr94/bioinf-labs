#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 9                                                                        #
#                                                                              #
# Luca Robbiano, 244033                                                        #
# NOTE: This classifier has a very poor accuracy (~0.5), so I might have       #
#       implemented something wrong                                            #
################################################################################

from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Bidirectional
from keras.optimizers import SGD


class RecurrentClassifier:

    def __init__(self, learning_rate=0.01, epochs=10, bidirectional=False):
        self.model = Sequential()
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.sgd = SGD(lr=learning_rate, decay=learning_rate / epochs, nesterov=False)
        self.bidirectional = bidirectional

    def fit(self, x, y):
        if self.bidirectional:
            self._init_bidirectional(len(y[0]), x.shape)
        else:
            self._init_monodirectional(len(y[0]), x.shape)
        self.model.compile(optimizer=self.sgd, loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(x, y, batch_size=10, epochs=self.epochs, validation_split=0.1, verbose=True)

    def _init_monodirectional(self, n_classes, x_shape):
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(x_shape[1], x_shape[2])))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(units=n_classes, activation='softmax'))

    def _init_bidirectional(self, n_classes, x_shape):
        self.model.add(Bidirectional(LSTM(units=50, return_sequences=True, input_shape=(x_shape[1], x_shape[2]))))
        self.model.add(Dropout(0.2))
        self.model.add(Bidirectional(LSTM(units=50, return_sequences=True)))
        self.model.add(Dropout(0.2))
        self.model.add(Bidirectional(LSTM(units=50, return_sequences=True)))
        self.model.add(Dropout(0.2))
        self.model.add(Bidirectional(LSTM(units=50)))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(units=n_classes, activation='softmax'))

    def evaluate(self, x, y, verbose):
        return self.model.evaluate(x, y, verbose=verbose)

    def predict(self, x):
        return self.model.predict(x)

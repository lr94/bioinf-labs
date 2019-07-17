#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 8                                                                        #
#                                                                              #
# Luca Robbiano, 244033                                                        #
################################################################################

import sys
import re
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from lab8.classifier import ConvolutionalClassifier


def main():
    filename = sys.argv[1]
    print("Loading dataset %s" % filename)
    sequences, labels = load_file(filename)

    # Encode labels
    label_binarizer = LabelBinarizer()
    y = label_binarizer.fit_transform(labels)
    # One-hot encoding
    code = {'A': [1, 0, 0, 0], 'T': [0, 1, 0, 0], 'C': [0, 0, 1, 0], 'G': [0, 0, 0, 1],
            'N': [0.25, 0.25, 0.25, 0.25], 'D': [0.33, 0.33, 0, 0.33], 'R': [0.5, 0, 0, 0.5], 'S': [0, 0, 0.5, 0.5]}
    x = np.zeros((len(sequences), len(sequences[0]), 4))
    for i in range(len(sequences)):
        x[i, :, :] = np.array([code[letter] for letter in sequences[i]])

    # Split dataset
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    print("%d samples loaded" % len(sequences))

    print("Training classifier")
    classifier = ConvolutionalClassifier(learning_rate=0.005, epochs=10)
    classifier.fit(x_train, y_train)
    print("Computing metrics")
    ev_result = classifier.evaluate(x_test, y_test, verbose=True)
    print("Loss: %0.6f" % ev_result[0])
    print("Accuracy: %0.6f" % ev_result[1])

    y_predicted_raw = classifier.predict(x_test)
    y_predicted = label_binarizer.inverse_transform(y_predicted_raw)
    y_true = label_binarizer.inverse_transform(y_test)
    print("\nConfusion matrix:")
    print(confusion_matrix(y_true, y_predicted))


def load_file(filename):
    r = re.compile(r',\s*')
    labels = []
    sequences = []
    with open(filename, 'r') as f:
        for raw_line in f:
            fields = r.split(raw_line.replace('\n', ''))
            labels.append(fields[0])
            sequences.append(fields[2])
    return sequences, labels


if __name__ == '__main__':
    main()

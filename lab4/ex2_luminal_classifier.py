#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 4                                                                        #
# Assignment 2                                                                 #
#                                                                              #
# Luca Robbiano, 244033                                                        #
################################################################################

import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import sklearn.metrics as metrics


def main():
    dataset_file = sys.argv[1]
    reduced_dataset_file = sys.argv[2]

    # Load the datasets
    print("Loading datasets")
    dataset = pd.read_csv(dataset_file)
    dataset['l'] = dataset['l'].str.strip()  # Remove trailing spaces from "Luminal A" and "Luminal B"
    reduced_dataset = pd.read_csv(reduced_dataset_file)
    # Actually this shouldn't bee needed since we produced reduced_dataset.csv without extra spaces in the first field
    reduced_dataset['l'] = reduced_dataset['l'].str.strip()

    # Split the datasets [1]
    dataset_train, dataset_test = train_test_split(dataset, test_size=0.2)
    reduced_dataset_train, reduced_dataset_test = train_test_split(reduced_dataset, test_size=0.2)

    # Split data in X (data) and Y (labels)
    dataset_train_x, dataset_train_y = split_x_y(dataset_train)
    dataset_test_x, dataset_test_y = split_x_y(dataset_test)
    reduced_dataset_train_x, reduced_dataset_train_y = split_x_y(reduced_dataset_train)
    reduced_dataset_test_x, reduced_dataset_test_y = split_x_y(reduced_dataset_test)

    # Standardize datasets [2]
    print("Standardizing datasets")
    dataset_train_x = standardize(dataset_train_x)
    dataset_test_x = standardize(dataset_test_x)
    reduced_dataset_train_x = standardize(reduced_dataset_train_x)
    reduced_dataset_test_x = standardize(reduced_dataset_test_x)

    # Dimensionality reduction: perform PCA on dataset.csv [3]
    feature_count = 80
    print("Reducing the full dataset to %d features using PCA" % feature_count)
    pca = PCA(feature_count)
    dataset_train_x = pca.fit_transform(dataset_train_x)
    dataset_test_x = pca.transform(dataset_test_x)

    # Train a KNN classifier on the full dataset [4]
    k = 10
    print("\nTraining a KNN classifier (k = %d) on the full dataset" % k)
    knn = KNeighborsClassifier(k)
    knn.fit(dataset_train_x, dataset_train_y)

    # Predict values [5]
    predicted = knn.predict(dataset_test_x)

    # Compute metrics [6]
    accuracy, precision, recall, f1 = compute_metrics(dataset_test_y, predicted, pos_label='Luminal A')
    sk_accuracy = metrics.accuracy_score(dataset_test_y, predicted)
    sk_precision = metrics.precision_score(dataset_test_y, predicted, pos_label='Luminal A')
    sk_recall = metrics.recall_score(dataset_test_y, predicted, pos_label='Luminal A')
    sk_f1 = metrics.f1_score(dataset_test_y, predicted, pos_label='Luminal A')
    print("                  Accuracy        Precision       Recall          F1")
    print("From scratch:     %0.8f      %0.8f      %0.8f      %0.8f" % (accuracy, precision, recall, f1))
    print("     sklearn:     %0.8f      %0.8f      %0.8f      %0.8f" % (sk_accuracy, sk_precision, sk_recall, sk_f1))
    print("\n----------------------------------------------------------------------------\n")

    # Train a KNN classifier on the reduced dataset [7]
    print("Training a KNN classifier (k = %d) on the reduced dataset" % k)
    knn = KNeighborsClassifier(k)
    knn.fit(reduced_dataset_train_x, reduced_dataset_train_y)
    predicted = knn.predict(reduced_dataset_test_x)
    display_metrics(reduced_dataset_test_y, predicted)

    # Train a SVM classifier on the reduced dataset [9.1]
    svc = SVC()
    print("Training a SVM classifier (%s kernel) on the reduced dataset" % svc.kernel)
    svc.fit(reduced_dataset_train_x, reduced_dataset_train_y)
    predicted = svc.predict(reduced_dataset_test_x)
    display_metrics(reduced_dataset_test_y, predicted)

    # Train a Random Forest classifier on the reduced dataset [9.2]
    rfc = RandomForestClassifier(n_estimators=100)
    print("Training a Random Forest classifier (%d estimators) on the reduced dataset" % rfc.n_estimators)
    rfc.fit(reduced_dataset_train_x, reduced_dataset_train_y)
    predicted = rfc.predict(reduced_dataset_test_x)
    display_metrics(reduced_dataset_test_y, predicted)

    # Train a Naive Bayes classifier on the reduced dataset [9.3]
    print("Training a Gaussian Naive Bayes classifier on the reduced dataset")
    nbc = GaussianNB()
    nbc.fit(reduced_dataset_train_x, reduced_dataset_train_y)
    predicted = nbc.predict(reduced_dataset_test_x)
    display_metrics(reduced_dataset_test_y, predicted)


def display_metrics(true_y, predicted_y):
    sk_accuracy = metrics.accuracy_score(true_y, predicted_y)
    sk_precision = metrics.precision_score(true_y, predicted_y, pos_label='Luminal A')
    sk_recall = metrics.recall_score(true_y, predicted_y, pos_label='Luminal A')
    sk_f1 = metrics.f1_score(true_y, predicted_y, pos_label='Luminal A')
    print("                  Accuracy        Precision       Recall          F1")
    print("      Metric:     %0.8f      %0.8f      %0.8f      %0.8f" % (sk_accuracy, sk_precision, sk_recall, sk_f1))
    print("\n----------------------------------------------------------------------------\n")


def split_x_y(dataframe: pd.DataFrame):
    x = dataframe.iloc[:, 1:]
    y = dataframe.iloc[:, 0]
    return x, y


def compute_metrics(true_y, predicted_y, pos_label):
    # Count positive predictions
    pp = sum(x == pos_label for x in predicted_y)
    # Count positive actual values
    pv = sum(x == pos_label for x in true_y)
    # Count true positives
    tp = sum(np.logical_and(np.equal(predicted_y, pos_label), np.equal(true_y, pos_label)))
    # Count false positives
    fp = sum(np.logical_and(np.equal(predicted_y, pos_label), np.logical_not(np.equal(true_y, pos_label))))
    # Count false negatives
    fn = sum(np.logical_and(np.logical_not(np.equal(predicted_y, pos_label)), np.equal(true_y, pos_label)))

    accuracy = float(np.equal(predicted_y, true_y).values.sum()) / len(true_y)
    precision = float(tp) / pp
    recall = float(tp) / pv
    f1 = float(2 * tp) / (2 * tp + fp + fn)

    return accuracy, precision, recall, f1


def standardize(dataframe: pd.DataFrame):
    # return (dataframe - dataframe.mean()) / dataframe.std()
    scaler = StandardScaler()
    return scaler.fit_transform(dataframe)


if __name__ == '__main__':
    main()

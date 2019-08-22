#!/usr/bin/env python

import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.utils.validation import column_or_1d
import numpy as np

def get_dataset():
    # Carregar os arquivos processados de bag of words (britanicos e suecos)
    X_native = np.loadtxt('native_content.csv',delimiter=',')
    X_non_native = np.loadtxt('non-native_content.csv',delimiter=',')
    
    # Adiconar coluna de classificação nativo para britanicos, não nativos para suecos
    y_native = np.full((len(X_native),1),1)
    y_non_native =  np.full((len(X_non_native),1),0)

    # Unir datasets
    X = np.concatenate((X_native,X_non_native), axis=0)
    y = np.concatenate((y_native,y_non_native), axis=0)

    return X, y

def get_etydataset(X):
    fingerprints = pd.read_csv('native_fingerprint.csv')
    fingerprints_non_native = pd.read_csv('non-native_fingerprint.csv')

    # Unir os dois com o dataset da bag of words
    X_fingerprints = fingerprints.append(fingerprints_non_native)
    X_fingerprints = X_fingerprints.fillna(0)

    X = np.concatenate((X,X_fingerprints.values), axis=1)

    return X


def svm_train(X, y, poly_degree):
    clf = svm.SVC(kernel="poly", gamma='scale', degree=poly_degree)
    scores = cross_val_score(clf, X, np.ravel(y), cv=5)

    return scores.mean()
    

if __name__ == '__main__':
    max_degree = 30

    # Carregar dataset
    X, y = get_dataset()
    # Dividir o dataset em dados de treinamento e test
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Treinar classficador
    results_only_words = {'degree': [], 'score': []}
    print("Acurácia do classificador SVM sem informação etimológica: ")
    for poly_degree in range(0, max_degree + 1):
        score = svm_train(X, y, poly_degree)
        results_only_words['degree'].append(poly_degree)
        results_only_words['score'].append(score)
        print("Degree " + str(poly_degree) + ": " +  str(score))
    
    pd.DataFrame(results_only_words).to_csv("results_only_words.csv")

    X = get_etydataset(X)
    # Dividir o dataset em dados de treinamento e test
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Treinar classficador
    results_fingerprint = {'degree': [], 'score': []}
    print("Acurácia do classificador SVM com informação etimológica: ")
    for poly_degree in range(0, max_degree + 1):
        score = svm_train(X, y, poly_degree)
        results_fingerprint['degree'].append(poly_degree)
        results_fingerprint['score'].append(score)
        print("Degree " + str(poly_degree) + ": " +  str(score))
        
    pd.DataFrame(results_fingerprint).to_csv("results_fingerprint.csv")
    
    
  

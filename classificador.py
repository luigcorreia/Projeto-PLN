#!/usr/bin/env python

import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
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



if __name__ == '__main__':

    # Carregar dataset
    X, y = get_dataset()
    # Dividir o dataset em dados de treinamento e test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Treinar classficador
    clf_1 = svm.SVC()
    clf_1.fit(X_train, y_train) 
    # Obter previsão
    y_pred = clf_1.predict(X_test)
    # Obter acurácia
    print("Acurácia do classificador SVM sem informação etimológica: ")
    print(accuracy_score(y_test, y_pred))
    

    X = get_etydataset(X)
    # Dividir o dataset em dados de treinamento e test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Treinar classficador
    clf_2 = svm.SVC()
    clf_2.fit(X_train, y_train) 
    # Obter previsão
    y_pred = clf_2.predict(X_test)
    # Obter acurácia
    print("Acurácia do classificador SVM sem informação etimológica: ")
    print(accuracy_score(y_test, y_pred))
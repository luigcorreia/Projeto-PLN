#!/usr/bin/env python

import sys
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import pandas as pd
import re
import collections
import string
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

re_punctuation = re.compile('[{0}]+'.format(string.punctuation))
def get_documents(directory_name, encoding='utf-8'):

    lemmatizer = WordNetLemmatizer() 
    documents = {}
    for filename in os.listdir(directory_name):
        # Ler documento
        document = open(directory_name + '/' + filename, 'r', encoding = encoding)
        content = document.read()

        # Obter tokens a partir do documento
        tokens = nltk.word_tokenize(content)
        # Remover stopwords
        stop_words = stopwords.words('english')
        tokens = [word.lower() for word in tokens if word not in stop_words]
        # Remover sinais de pontuação
        tokens = [x for x in tokens if not re_punctuation.fullmatch(x)]

        # Lemmatização
        tokens = list(map(lambda word: lemmatizer.lemmatize(word), tokens))

        # POS Tagging
        #tokens_tagged = nltk.pos_tag(tokens)
        
        documents[filename] = tokens

    return documents

def load_etymology():
    # Carregar dados da etytree
    used_rel_types = ['rel:etymology']
    etymwn = pd.read_csv('documentos/etymwn.tsv', sep='\t')
    etymwn.columns = ['word','relation','parent_word']
    etymwn = etymwn[etymwn['relation'].apply(lambda rel_type: rel_type in used_rel_types)]

    # Definir indice
    etymwn.index = etymwn['word']

    return etymwn


def origin_of(word, etymwn, lang='eng', level=1):
    # Consultar árvore etimologica e extrair idioma ancestral (primeiro nível ) da primeira ocorrência encontrada
    entrie = '{0}: {1}'.format(lang, word)
    try:
        lang, word = etymwn.loc[entrie]['parent_word'].split(': ')
        if level == 1:
            return lang, word
        else:
            return origin_of(word, etymwn, lang=lang, level=level-1)
    except:
        return None, None

def etymological_sig(document, etymwn):

    word_count = pd.DataFrame()

    for word in document:
        lang, parent_word = origin_of(word, etymwn)
        #print(lang)
        if lang is not None:
            if lang not in word_count:
                word_count[lang] = [0]
            word_count[lang] = word_count[lang] + 1

    return word_count

def generate_sig_dataset(documents, etymwn, filename):

    sig = pd.DataFrame()
    for name, document in documents.items():
        sig = sig.append(etymological_sig(document, etymwn))

    # Preencher valores ausentes com zero
    sig = sig.fillna(0)
    # Normalizar por total de palavras
    sig = sig.divide(sig.sum(axis=1),axis=0)
    # Salvar em disco
    sig.to_csv(filename)


def generate_content_dataset(documents, filename):

    data = list(map(lambda document: " ".join(documents[document]), documents))
    matrix = CountVectorizer(max_features=1000)
    X = matrix.fit_transform(data).toarray()
    
    # Normalizar por total de palavras
    X = (X.T / X.sum(axis=1)).T
    # Salvar em disco
    np.savetxt(filename, X, delimiter=',')


def generate_british_swedish_datasets():

    british_documents = get_documents('documentos/BWAE')
    print("Ensaios britânicos carregados")
    swedish_documents = get_documents('documentos/USE', encoding="ISO-8859-1")
    print("Ensaios suecos carregados")

    # Gerar datsets com bag of words
    generate_content_dataset(british_documents, 'native_content.csv')
    generate_content_dataset(swedish_documents, 'non-native_content.csv')

    # Carregar árvore etimológica
    etymwn = load_etymology()
    print("Árvore etimológica carregada")
    
    # Gerar datasets de assinaturas etimológicas
    print("Gerando assinaturas etimológicas para ensaios nativos")
    generate_sig_dataset(british_documents, etymwn, 'native_fingerprint.csv')
    print("Gerando assinaturas etimológicas para ensaios não-nativos")
    generate_sig_dataset(swedish_documents, etymwn, 'non-native_fingerprint.csv')

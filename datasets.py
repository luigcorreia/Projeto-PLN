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



def get_documents(directory_name):

    lemmatizer = WordNetLemmatizer() 
    documents = {}
    for filename in os.listdir(directory_name):
        # Ler documento
        document = open(directory_name + '/' + filename, 'r')
        content = document.read()

        # Obter tokens a partir do documento
        tokens = nltk.word_tokenize(content)
        # Remover stopwords
        stop_words = stopwords.words('english')
        tokens = [word for word in tokens if word not in stop_words]
        # Remover sinais de pontuação
        tokens = [x for x in tokens if not re.fullmatch('[{0}]+'.format(string.punctuation), x)]

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

    # Carregar somente palavras da lingua inglesa (acelerar busca de um só nível na árvore)
    etymwn = etymwn[etymwn['word'].apply(lambda w: w[0:3] == 'eng')]

    return etymwn


def origin_of(word, etymwn, lang='eng', level=1):
    # Consultar árvore etimologica e extrair idioma ancestral (primeiro nível ) da primeira ocorrência encontrada
    entries = etymwn[etymwn['word'].apply(lambda etymwn_word: '{0}: {1}'.format(lang, word) == etymwn_word)]
    lang, word = (entries['parent_word'].iloc[0].split(': ') if len(entries) else [None, None])
    if lang is None or level == 1:
        return lang, word
    else:
        return origin_of(word, etymwn, lang=lang, level=level-1)

def etymological_sig(document, etymwn):

    # Filtrar categoria de POS-Tagging

    word_count = pd.DataFrame()

    for word in document:
        lang, parent_word = origin_of(word, etymwn)
        #print(lang)
        if lang is not None:
            if lang not in word_count:
                word_count[lang] = [0]
            word_count[lang] = word_count[lang] + 1

    return word_count

def generate_sig_dataset(documents, filename):

    etymwn = load_etymology()

    sig = pd.DataFrame()
    for document in documents:
        sig = sig.append(etymological_sig(document, etymwn))
        print('Assinatura etimológica do documento "{0}": {1}'.format(document, sig))

    sig.to_csv(filename)

def generate_british_swedish():

    #british_documents = get_documents('documentos/BWAE')
    #swedish_documents = get_documents('documentos/USE')
    british_documents = get_documents('documentos/teste')

    # gerar datsets com bag of words para cada base de documento
    
    # Gerar datasets
    generate_sig_dataset(british_documents, 'native_fingerprint.csv')
    #generate_sig_dataset(swedish_documents, 'non-native_fingerprint.csv')

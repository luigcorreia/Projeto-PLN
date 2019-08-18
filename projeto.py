#!/usr/bin/env python

import sys
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import pandas as pd
from sklearn import svm
import re
import collections



def get_documents(directory_name):

    lemmatizer = WordNetLemmatizer() 
    documents = {}
    for filename in os.listdir(directory_name):
        # Ler documento
        document = open(directory_name + '/' + filename, 'r')
        content = document.read()

        # Obter tokens a partir do documento
        tokens = nltk.word_tokenize(content)
        stop_words = stopwords.words('english')
        tokens = [word for word in tokens if word not in stop_words]

        # Lemmatização
        tokens = map(lambda word: lemmatizer.lemmatize(word), tokens)

        # POS Tagging
        #tokens_tagged = nltk.pos_tag(tokens)
        
        documents[filename] = tokens

    return documents

def load_etymology():
    # Carregar dados da etytree
    used_rel_types = ['is_derived_from', 'etymology', 'etymologically_related', 'derived', 'etymologically']
    etymwn = pd.read_csv('documentos/etymwn.tsv', sep='\t')
    etymwn.columns = ['word','relation','parent_word']
    etymwn = etymwn[etymwn['relation'].apply(lambda rel_type: rel_type in used_rel_types)]

    return etymwn


def origin_of(word):
    # Consultar árvore etimologica e extrair idioma ancestral (primeiro nível ) da primeira ocorrência encontrada
    match = etymwn[etymwn['word'].apply(lambda etymwn_word: re.match('origin of ' + word, etymwn_word) is not None)]
    return (match['parent_word'][0][0:3] if len(match) else None)

languages = pd.DataFrame.from_dict({'eng':0,'ang':0}) # adiconar as válidas
def etymological_sig(document):

    # Filtrar categoria de POS-Tagging

    word_count = languages.copy()

    for word in document:
        origin = origin_of(word)

        if origin is not None and origin in languages:
            word_count[origin] = word_count[origin] + 1

    return word_count

if __name__ == '__main__':

    british_documents = get_documents('documentos/BWAE')
    #swedish_documents = get_documents('documentos/USE')

    print(len(british_documents))

    etymwn = load_etymology()

    sig = pd.DataFrame()
    for document in british_documents:
        sig = sig.append(etymological_sig(document))

    print(sig)
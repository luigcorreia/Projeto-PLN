#!/usr/bin/env python

import sys
import os
import nltk
from nltk.corpus import stopwords
import pandas as pd
import re

def get_documents(directory_name):

    documents = {}
    for filename in os.listdir(directory_name):
        # Ler documento
        document = open(directory_name + '/' + filename, 'r')
        content = document.read()

        # Obter tokens a partir do documento
        tokens = nltk.word_tokenize(content)
        stop_words = stopwords.words('english')
        tokens = [word for word in tokens if word not in stop_words]
        
        documents[filename] = tokens

    return tokens

def load_etymology():
    # Carregar dados da etytree
    used_rel_types = ['is_derived_from', 'etymology', 'etymologically_related', 'derived', 'etymologically']
    etymwn = pd.read_csv('documentos/etymwn.tsv', sep='\t')
    etymwn.columns = ['word','relation','parent_word']
    etymwn = etymwn[etymwn['relation'].apply(lambda rel_type: rel_type in used_rel_types)]

    return etymwn


def origin_of(word):
    candidates = etymwn[etymwn['word'].apply(lambda test_word: test_word in word)] # usar re
    return candidates['parent_word'][0][0:3]

if __name__ == '__main__':

    british_documents = get_documents('documentos/BWAE')
    swedish_documents = get_documents('documentos/USE')

    print(len(swedish_documents))

    #etymwn = load_etymology()


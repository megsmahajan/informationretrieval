import re
import os
import math
import numpy as np
from nltk.stem import PorterStemmer
from itertools import chain
from collections import Counter
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
import pickle
import cosine as cos


def tokenization(lines):
    special_tokens_rule_1_and_2 = re.findall(
        r"\w+-\n\w+|[\w\.-]+@[\w\.-]+|\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",lines)

    special_tokens_rule_3 = re.findall(r"|        \B['`].+?['`]\B|[A-Z][a-z']+(?=\s[A-Z])(?:\s[A-Z][a-z']+)+",lines)

    special_tokens_rule_4_and_5 = re.findall(r"(?:[a-zA-Z]\.){2,}|\b[A-Z]+(?:\s+[A-Z]+)*\b",lines)

    special_tokens = special_tokens_rule_1_and_2+special_tokens_rule_3+special_tokens_rule_4_and_5

    special_tokens = [w.replace('-\n', ' ') for w in special_tokens]

    file_tokens_1 = re.sub(
        r"\w+-\n\w+|[\w\.-]+@[\w\.-]+|\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", "",
        lines)

    file_tokens_2 = re.sub(r"|        \B['`].+?['`]\B|[A-Z][a-z']+(?=\s[A-Z])(?:\s[A-Z][a-z']+)+", "",  lines)

    file_tokens_3 = re.sub(r"(?:[a-zA-Z]\.){2,}|\b[A-Z]+(?:\s+[A-Z]+)*\b", "", lines)

    file_tokens = file_tokens_1+file_tokens_2+file_tokens_3

    file_tokens = re.split(r"( )|\n|\-\-|\[|\]|\.|\,|\:|\;|\"|\'|\(|\)|\?|\!|\}|\{|\/", file_tokens)

    final_tokens = []
    for tokens in file_tokens:
        if tokens!=None and tokens!= ' ' and tokens != '':
            final_tokens.append(tokens)

    final_tokens[:] = [tokens.strip('[-+=]') for tokens in final_tokens]

    return special_tokens, final_tokens


def removeStopWords(file_tokens, stopwords):
    with open(stopwords) as stop:
        stop_words=stop.read()
        stop_words = stop_words.lower()
        stop_words = stop_words.split('\n')

    file_tokens = [words for words in file_tokens if words not in stop_words]

    return file_tokens


# In[6]:

def stemming(file_tokens):
    stemmed_words = []
    ps = PorterStemmer()
    for word in file_tokens:
        stemmed_words.append(ps.stem(word))
    return stemmed_words


def index_documents(file_path, inverted_file ,stopwords):
    docs = []
    termsCollection = []
    final = []
    term_freq_dic = dict()
    idf_dict = dict()
    for files in os.listdir(file_path):
        lines = []
        read_file = os.path.join(file_path, files)
        if os.path.isfile(read_file) and read_file.endswith('.txt'):

            open_file = open(read_file, "r", encoding="utf-8-sig")
            lines = open_file.read()

            # Tokenize the document contents
            special_tokens, file_tokens = cos.tokenization(lines)

            # convert all tokens to lower case
            special_tokens[:] = [x.lower() for x in special_tokens]

            file_tokens[:] = [x.lower() for x in file_tokens]

            # Remove stop words
            file_tokens = removeStopWords(file_tokens, stopwords)

            # Stem all the tokens
            file_tokens = stemming(file_tokens)

            # Joining both token lists
            tokens = special_tokens + file_tokens

            # Calculate Term Frequencies
            term_freq = dict(Counter(tokens))
            term_freq_dic[files] = term_freq

            # Docs for Document Frequencies
            docs.append(list(set(term_freq.keys())))

    #             print(special_tokens)

    # Document Frequencies
    N = len(docs)
    #     print("N:",N)
    docs = list(chain.from_iterable(docs))
    document_frequency_dict = dict(Counter(docs))

    # Inverse Document Frequency
    idf_dict.update((key, round(np.log(N / (float(value) if value else 1)), 3)) for key, value in document_frequency_dict.items())

    # Vocabulary
    vocab = idf_dict.keys()
    vocab = sorted(vocab)
    
    inverted_file = createInvertedFile(idf_dict,term_freq_dic)


    with open('inverted.txt', 'w') as filehandle:
        for listitem in inverted_file:
            filehandle.write('%s\n' % listitem)

    with open('vocab.txt', 'w') as filehandle:
        for listitem in vocab:
            filehandle.write('%s\n' % listitem)

def createInvertedFile(idf_dict,term_freq_dic):
    # Inverted Index
    term_ind = []
    for terms in idf_dict:
        docs_terms = []
        docs_terms.append(terms)
        for key, value in term_freq_dic.items():
            if terms in value:
                docs_terms.append(key)
                docs_terms.append(str(value[terms]))
        docs_terms.append(str(idf_dict[terms]))
        docs_terms = ','.join(docs_terms)
        term_ind.append(docs_terms)

    return term_ind


def main():
    file_path = input("Input file path: ")
    stopwords = input("Input stopword file: ")
    inverted = input("Input inverted file: ")

    index = index_documents(file_path,inverted, stopwords)
    #print(index)

if __name__ == '__main__':
    main()


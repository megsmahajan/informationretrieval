import re
import os
import math
import numpy as np
from nltk.stem import PorterStemmer
from itertools import chain
from collections import Counter
from collections import OrderedDict
import indexing as index
import pickle
import cosine as cos

def do_search(index_dir,num_docs,keyword_list):
    #ifile = "inverted.txt"
    vfile = "vocab.txt"
    inverted_file = open(index_dir, "r", encoding="utf-8-sig")
    vocab_file = open(vfile, "r", encoding="utf-8-sig")
    inverted = inverted_file.read()
    vocab = vocab_file.read()
    inverted = re.split(r"\n", inverted)
    vocab = re.split(r"\n", vocab)
    inverted = [re.split(r",", i) for i in inverted]

    #print(inverted)

    docs = []
    for i in inverted:
        for x in range(1, len(i) - 1):
            if x % 2 != 0:
                docs.append(i[x])
            else:
                i[x] = float(i[x])
                i[x] = round(float(i[len(i) - 1]) * i[x], 3)

    docs = sorted(list(set(docs)))

    inverted = sorted(inverted)
    #     print(inverted)
    doc_vector = {}

    #print(inverted)

    for i in inverted:
        #         print("I:",i)
        doc_vector_dic = {}
        for x in range(1, len(i) - 1, 2):
            #             print("x:",i[x])
            doc_vector_dic[i[x]] = i[x + 1]
        #         doc_vector.append()
        doc_vector[i[0]] = doc_vector_dic

    #print(doc_vector)

    doc_vec = dict()

    for d in docs:
        weights = []
        for term in vocab:
            if d in doc_vector[term]:
                weights.append(doc_vector[term][d])
            else:
                weights.append(0)
        doc_vec[d] = weights

    # ***********************Query Vector*****************************

    query_tf = []
    #q = input("Enter your query: ")

    query = ""
    keyword_list = keyword_list[4:]
    for query_terms in keyword_list:
        query+=query_terms
        query+=" "

    print(query)

    special_query_tokens, query_tokens = cos.tokenization(query)

    # Convert query terms to Lower Case
    special_query_tokens[:] = [x.lower() for x in special_query_tokens]
    query_tokens[:] = [x.lower() for x in query_tokens]

    # Remove Stop Words from query
    query_tokens = index.removeStopWords(query_tokens, stopwords="D:/Semester_3/FIT5166/IR/stopwords_en.txt")

    # Stem words from query
    query_tokens = index.stemming(query_tokens)

    # Joining both files
    tokens = special_query_tokens + query_tokens

    # Term Frequencies of query
    query_term_freq = dict(Counter(tokens))

    queryWeights = {}
    for k, v in query_term_freq.items():
        for i in inverted:
            if k in i:
                queryWeights[k] = round((v * float(i[-1])), 3)

    print(queryWeights)

    for v in vocab:
        if v not in queryWeights.keys():
            queryWeights[v] = 0

    queryWeights = sorted(queryWeights.items())

    queryVectors = []
    for q in queryWeights:
        queryVectors.append(q[1])

    product_of_query_and_doc = {}
    for k, d in doc_vec.items():
        n = [round(a * b, 3) for a, b in zip(d, queryVectors)]
        product_of_query_and_doc[k] = n



    # sum of squares of Document Vector
    d_sq = []
    sum_d_sq = {}
    for k, dd in doc_vec.items():
        sum_of_squares = 0
        for weight in dd:
            d_sq.append(round(weight ** 2, 3))
        sum_d_sq[k] = (round(math.sqrt(sum(d_sq)), 3))
    #     print(sum_d_sq)


    denominator = cos.calculate_denominator(sum_d_sq)
    numerator = cos.calculate_numerator(doc_vec,queryVectors)


    cosine = {}
    for k, d in denominator.items():
        cosine[k] = round(numerator[k] / denominator[k], 3)
    #     print(cosine)

    cosine_sorted_keys = sorted(cosine, key=cosine.get, reverse=True)
    for r in cosine_sorted_keys:
        if cosine[r]>0.0:
            print(r, cosine[r])

def main():
    do_search("inverted.txt",1400,["D: / Semester_3 / FIT5166 / IR / MySearchEngine.py","search","D: / Semester_3 / FIT5166 / IR / inverted.txt","1400","what","are","the","discontinuity","stresses","at","junctions","in","pressurized","structures"])



if __name__ == '__main__':
    main()



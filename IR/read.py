"""
Description: Main file to index the docments and then perform search operations.
"""
from stemming import stem_for_str
from stop_list import is_stop_word
from inverted_list import IndexList
from tf_idf import idf
import functools
import math
from os import listdir
from os.path import isfile, join
import pickle
import re

dictionary = set()
length = dict()

# pre-process the word
def process(word):
    returned_word = word

    # check if it's made up of the symbols
    is_useless = True
    for ch in word:
        if ch not in {'~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=',
                          '{', '[', '}', ']', '\\', '|', ':', ';', '\'', '\"', '<', ',', '>', '.', '?', '/'}:
                is_useless = False
                break
        if is_useless:
            return ''

    returned_word = re.sub('[^a-zA-Z0-9 \n]', '', word)

    # convert into lower case
    returned_word = returned_word.lower()

    # stem
    if returned_word!='':
        returned_word = stem_for_str(returned_word)

    return returned_word


# process one document at a time
def read_doc(dir_path, list_of_docs, index_list, doc_id, file_title_list):
    #dir_name = (dir_path.partition('/'))[-1]
    dir_name = list_of_docs[doc_id]
    file_path = dir_path + '/' + dir_name

    reader = open(file_path, 'r', encoding="utf8")
    doc = reader.readlines()
    reader.close()

    doc = ''.join(doc).split('\n')
    while '' in doc:
        doc.remove('')

    file_title_list.append(doc[0])

    pos = 1
    for i in range(1, len(doc)):
        paragraph = doc[i]
        word_list = paragraph.split(sep=' ')
        for word in word_list:
            word = process(word)
            if word != '' and not is_stop_word(word):
                index_list.add(word, doc_id+1, pos)
            pos += 1


# process the whole document set
def read(dir_path,list_of_docs, index_list, doc_number, file_title_list):
    for doc_id in range(0, doc_number):
        read_doc(dir_path, list_of_docs, index_list, doc_id, file_title_list)

def imp(term,word_dict,number_of_docs,id):
    """Returns the importance of term in document id.  If the term
    isn't in the document, then return 0."""

    with open('term_freq.txt', 'rb') as file:
        term_freq = pickle.loads(file.read())

    #print(term_freq)

    if id+1 in term_freq[term]:
        #print(term_freq[term][id])
        return term_freq[term][id+1]*word_dict[term][1]#idf(term,number_of_docs,index_list)
    else:
        return 0.0


def initialize_lengths(number_of_docs,word_dict,dictionary):
    """Computes the scalar length for each document."""
    global length
    with open('document_filenames.txt', 'rb') as file:
        document_filenames = pickle.loads(file.read())

    for id in document_filenames:
        l = 0
        #print(dictionary)
        for term in dictionary:
            l += imp(term,word_dict,number_of_docs,id)**2
        length[id-1] = math.sqrt(l)

def do_search(index_file, number_of_docs, given_query):
    """Takes as input the query and number of documents. Find Cosine Similarity between the query and documents.
    Arrange the cosine similarity in descending order. Display the output as cosine similarity and the document
    it is associated with.
    """

    #print(number_of_docs)

    with open('document_filenames.txt', 'rb') as file:
        document_filenames = pickle.loads(file.read())

    #query = input('Please input your query (Enter \'q\' to quit): ')
    given_query = given_query[4:]
    #query = query.lower()
    #query = query.split(' ')

    query = []

    stemmed_query = [stem_for_str(keyword) for keyword in given_query]
    for query_terms in stemmed_query:
        if query_terms!='' and not is_stop_word(query_terms):
            query.append(query_terms)

    #print(query)

    with open('intermediate_file.txt', 'rb') as file:
        some_dict = pickle.loads(file.read())

    with open('dictionary.txt', 'rb') as fp:
        dictionary = pickle.load(fp)

    #print(dictionary)

    #initialize_lengths(number_of_docs,some_dict,dictionary)

    # find document ids containing all query terms.  Works by
    # intersecting the posting lists for all query terms.


    relevant_document_ids = intersection([set(some_dict[term][0].keys()) for term in query])

    print(relevant_document_ids)

    if not relevant_document_ids:
        print ("No documents matched all query terms.")
    else:
        scores = sorted([(id-1,similarity(query,some_dict,dictionary,number_of_docs,id-1))
                         for id in relevant_document_ids],
                        key=lambda x: x[1],
                        reverse=True)
        print ("Score: filename")
        for (id,score) in scores:
            print (str(score)+": "+ document_filenames[id+1])

    return scores

def intersection(sets):
    """Returns the intersection of all sets in the list sets. Requires
    that the list sets contains at least one element, otherwise it
    raises an error."""
    return functools.reduce(set.intersection, [s for s in sets])


def similarity(query,word_dict,dictionary,number_of_docs,id):
    """Returns the cosine similarity between query and document id.
    Note that we don't bother dividing by the length of the query
    vector, since this doesn't make any difference to the ordering of
    search results."""
    similarity = 0.0
    scalar_leng = 0.0
    for term in query:
        if term in dictionary:
            similarity += word_dict[term][1]*imp(term,word_dict,number_of_docs,id)

    for term in dictionary:
        scalar_leng += imp(term, word_dict, number_of_docs, id) ** 2

    final_scalar_leng = math.sqrt(scalar_leng)
    similarity = similarity / final_scalar_leng
    #print(similarity)
    return similarity


def index_documents(dir_path, index_path):
    index_list = IndexList()
    file_title_list = list()
    document_filenames = dict()

    onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    #print(onlyfiles[0])
    #print(len(onlyfiles))

    i = 1
    for files in onlyfiles:
        document_filenames.update({i: files})
        i += 1

    #print(document_filenames)

    read(dir_path, onlyfiles, index_list, len(onlyfiles), file_title_list)
    # print(file_title_list)
    # index_list.print()

    word_list = list()
    some_dict = dict()
    term_freq = dict()
    list_of_words = []
    index_dict = dict()
    final_position_dict = dict()

    for word in index_list.index_list:
        doc_dict = dict()
        position_dict = dict()

        list_of_words.append(word)
        idf_of_word = idf(word, len(onlyfiles), index_list)
        list_of_docs = []
        for doc_id in index_list.index_list[word].inverted_list:
            doc_dict.update({doc_id: len(index_list.index_list[word].inverted_list[doc_id])})
            position_dict.update({doc_id: index_list.index_list[word].inverted_list[doc_id]})
            list_of_docs.append(doc_id)
            index_dict.update({word: len(list_of_docs)})
            term_freq.update({word: doc_dict})
            some_dict.update({word: [doc_dict, idf_of_word]})
            final_position_dict.update({word: position_dict})

    dictionary = set(list_of_words)

    with open('dictionary.txt', 'wb') as fp:
        pickle.dump(dictionary, fp)

    #print(list_of_words)
    #print(dictionary)
    #print(some_dict)
    #print(final_position_dict)
    #print(index_dict)

    #initialize_lengths()

    with open(index_path, 'wb') as file:
        pickle.dump(final_position_dict,file)

    with open('term_freq.txt', 'wb') as file3:
        pickle.dump(term_freq,file3)

    with open('intermediate_file.txt', 'wb') as file1:
        pickle.dump(some_dict,file1)

    with open('document_filenames.txt', 'wb') as file2:
        pickle.dump(document_filenames,file2)

if __name__ == "__main__":
    dir_path = 'datafile/cnn'
    index_list = IndexList()
    file_title_list = list()
    document_filenames = dict()

    onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
   #print(onlyfiles[0])
    #print(len(onlyfiles))

    i = 1
    for files in onlyfiles:
        document_filenames.update({i:files})
        i+=1

    #print(document_filenames)

    read(dir_path, onlyfiles, index_list, len(onlyfiles), file_title_list)
    #print(file_title_list)
    #index_list.print()

    word_list = list()
    some_dict = dict()
    term_freq = dict()
    list_of_words = []
    index_dict = dict()
    final_position_dict = dict()

    for word in index_list.index_list:
        doc_dict = dict()
        position_dict = dict()

        list_of_words.append(word)
        idf_of_word = idf(word,len(onlyfiles),index_list)
        list_of_docs = []
        for doc_id in index_list.index_list[word].inverted_list:
            doc_dict.update({doc_id:len(index_list.index_list[word].inverted_list[doc_id])})
            position_dict.update({doc_id: index_list.index_list[word].inverted_list[doc_id]})
            list_of_docs.append(doc_id)
            index_dict.update({word:list_of_docs})
            term_freq.update({word:doc_dict})
            some_dict.update({word:[doc_dict,idf_of_word]})
            final_position_dict.update({word:position_dict})

    dictionary = set(list_of_words)
    #print(list_of_words)
    #print(dictionary)
    print (some_dict)
    #print(index_dict)
    #print(final_position_dict)
    print(final_position_dict)

    with open('file.txt', 'wb') as file:
        pickle.dump(final_position_dict,file)

    with open('intermediate_file.txt', 'wb') as file1:
        pickle.dump(some_dict,file1)

    with open('term_freq.txt', 'wb') as file2:
        pickle.dump(term_freq,file2)

    with open('dictionary.txt', 'wb') as fp:
        pickle.dump(dictionary, fp)

    with open('document_filenames.txt', 'wb') as file3:
        pickle.dump(document_filenames,file3)

    with open('term_freq.txt', 'rb') as file:
        term_freq_abc = pickle.loads(file.read())

    with open('intermediate_file.txt', 'rb') as file:
        some_dict = pickle.loads(file.read())

    initialize_lengths(20,some_dict,dictionary)

    #print(term_freq_abc)

    do_search("index.txt",20,"zika disease")



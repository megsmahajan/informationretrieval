import sys
import  read as read
#import read
import pickle
from stemming import stem_for_str
import file_abstract
import explicit_feedback

#java MySearchEngine index ~/mydocs ~/myindex ~/stopwords.txt

def main():
    query = input("Enter a query you want to search: ")
    targetPrecision = float(input("Enter the precision you want to achieve in the range (0.1-0.9): "))
    corpus = input("Enter the corpus path: ")
    indexFilePath = input("Path with filename to store Index: ")
    currentPrecision = 0.00
    numberOfDocs = int(input("Enter number of docs in the corpus: "))

    explicit = explicit_feedback.RocchioOptimizeQuery(query)

    with open('document_filenames.txt', 'rb') as file:
        document_filenames = pickle.loads(file.read())

    final_position_dict = dict()

    read.index_documents(corpus, indexFilePath)

    splitQuery = query.split(" ")

    splitQuery.insert(0, " ")
    splitQuery.insert(1, " ")
    splitQuery.insert(2, " ")
    splitQuery.insert(3, " ")

    # print(splitQuery[4:])

    searchResult = read.do_search(indexFilePath, numberOfDocs, splitQuery)

    while currentPrecision < targetPrecision:

        relevantDocuments = []
        nonRelevantDocuments = []

        currentPrecision = 0.00

        splitQuery = query.split(" ")

        splitQuery.insert(0," ")
        splitQuery.insert(1," ")
        splitQuery.insert(2," ")
        splitQuery.insert(3," ")

        #print(splitQuery[4:])

        searchResult = read.do_search(indexFilePath,numberOfDocs,splitQuery)

        with open(indexFilePath, 'rb') as file:
            intermidiatePos = pickle.loads(file.read())

        #print(intermidiatePos)

        splitQuery = splitQuery[4:]
        # query = query.lower()
        # query = query.split(' ')
        splitQuery = [stem_for_str(keyword) for keyword in splitQuery]

        positionalValues = []

        for (id,score) in searchResult:
            print (str(score)+": "+ document_filenames[id+1])

            for words in splitQuery:
                if (id+1) in intermidiatePos[words].keys():
                    print(intermidiatePos[words][id+1])
                    file_abstract.abstract(corpus,id+1,intermidiatePos[words][id+1])

            relevance = input("Is this a relevant document? (Y/N) :")

            if relevance.upper() == 'Y':
                currentPrecision = currentPrecision + 1
                relevantDocuments.append(id)

            elif relevance.upper() == 'N':
                nonRelevantDocuments.append(id)
            else:
                print ('Invalid value entered!')


        currentPrecision = float(currentPrecision) / len(searchResult)

        with open('intermediate_file.txt', 'rb') as file:
            some_dict = pickle.loads(file.read())

        if (currentPrecision < targetPrecision):
            print('')
            print('Still below desired precision of %f' % targetPrecision)
            newQuery = explicit.Rocchio(some_dict,relevantDocuments,nonRelevantDocuments)  # optimize new query here

            query = query + " " + newQuery[0] + " " + newQuery[1]

            print(query)
                #firstPass = 0

                #print('Augmenting by %s %s' % (newTerms[0], newTerms[1]))'''


if __name__ == '__main__':
    main()
    #dir_path = 'datafile/cnn'
    #onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    #print (onlyfiles)
    #print(len(onlyfiles))
    #doc_number = 20
    #main(dir_path, doc_number)
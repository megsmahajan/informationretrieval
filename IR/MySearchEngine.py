import sys
import indexing as index
import search_documents as search

#java MySearchEngine index ~/mydocs ~/myindex ~/stopwords.txt

def main():
    if str(sys.argv[1])== "index":
        index.index_documents(str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))

    elif str(sys.argv[1])== "search":
        search.do_search(str(sys.argv[2]),str(sys.argv[3]),sys.argv)

if __name__ == '__main__':
    main()
    #dir_path = 'datafile/cnn'
    #onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    #print (onlyfiles)
    #print(len(onlyfiles))
    #doc_number = 20
    #main(dir_path, doc_number)

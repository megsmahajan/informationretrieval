import pickle

def abstract(dir_path, doc_id, pos_index):

    with open('document_filenames.txt', 'rb') as file:
        document_filenames = pickle.loads(file.read())



    dir_name = document_filenames[doc_id]
    file_path = dir_path + '/' + dir_name

    #print(file_path)

    reader = open(file_path, 'r', encoding="utf8")
    doc = reader.readlines()
    reader.close()
    doc = ''.join(doc).split('\n')
    while '' in doc:
        doc.remove('')

    #print(doc)
    final_word_list = []

    #pos = 1
    for i in range(1, len(doc)):
        paragraph = doc[i]
        #print(paragraph)
        #has_keyword = False
        output_paragraph = ''
        word_list = paragraph.split(sep=' ')

        for words in word_list:
            final_word_list.append(words)

    j=0
    print(len(final_word_list))


    for pos in pos_index:
        #print(pos)
        j = pos-5
        #print(final_word_list[j])
        while j < (pos):

            if j > len(final_word_list):
                j=len(final_word_list)-1
                output_paragraph += final_word_list[j]+" "
                break

            elif j <1:
                j=0
                output_paragraph += final_word_list[j] + " "

            else:
                output_paragraph += final_word_list[j] + " "

            j+=1
        output_paragraph += "..."

    print('\t' + output_paragraph)
    print()
import re
from stemming import stem_for_str
import pickle


def process(word):
    returned_word = word

    if re.match(r'^\d+\.\d+\.\d+\.\d+$',word):
        return word
    elif re.match(r'([A-Z]\.)+',word):
        return  word
    elif re.match(r'\b[a-z]+(?:[\'-]?[a-z]+)*\b',word):
        return word
    elif re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',word):
        return word
    elif re.match(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',word):
        return word
    else:
        # check if it's made up of the symbols

        returned_word = re.sub('[^a-zA-Z0-9 \n]', '', word)

        is_useless = True
        for ch in word:
            if ch not in {'~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=',
                          '{', '[', '}', ']', '\\', '|', ':', ';', '\'', '\"', '<', ',', '>', '.', '?', '/'}:
                is_useless = False
                break
        if is_useless:
            return ''



    # convert into lower case
    returned_word = returned_word.lower()

    # stem
    if returned_word != '':
        returned_word = stem_for_str(returned_word)

    return returned_word

def main():
    #my_str = "hey there["
    #lists = ['A','B','C','D','E','F']
    #my_new_string = re.sub('[^a-zA-Z0-9 \n]', '', my_str)
    '''your_ip = "10.10.10.10"
    #result = re.match(r'^\d+\.\d+\.\d+\.\d+$', your_ip)
    #print(result)
    #print(str(lists).lower())

    one = process(your_ip)

    three = process("abc123@xyz.com")
    four = process("https://www.google.com.au")
    five = process("U.S.")

    print(one)
    print(two)
    print(three)
    print(four)
    print(five)

    with open('document_filenames.txt', 'rb') as file:
        document_filenames = pickle.loads(file.read())

    #for id in document_filenames:
     #   print(id)

    with open('term_freq.txt', 'rb') as file:
        term_freq = pickle.loads(file.read())

    #process("abc")

    #for i in range(len(lists)+4):
     #   print(i)'''

    mylist = [1, 7, 7, 7, 3, 9, 9, 9, 7, 9, 10, 0]
    my_set = sorted(set([i for i in mylist if mylist.count(i) > 2]))
    print (my_set)

    with open('intermediate_file.txt', 'rb') as file:
        some_dict = pickle.loads(file.read())

    print(some_dict)

    three = "moeckel,w.e."

    #result = re.sub(r"\w+-\n\w+|[\w\.-]+@[\w\.-]+|\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+|        \B['`].+?['`]\B|[A-Z][a-z']+(?=\s[A-Z])(?:\s[A-Z][a-z']+)+|(?:[a-zA-Z]\.){2,}|\b[A-Z]+(?:\s+[A-Z]+)*\b","",two)

    special_tokens = re.findall(
        r"\w+-\n\w+|[\w\.-]+@[\w\.-]+|\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+|        \B['`].+?['`]\B|[A-Z][a-z']+(?=\s[A-Z])(?:\s[A-Z][a-z']+)+|(?:[a-zA-Z]\.){2,}|\b[A-Z]+(?:\s+[A-Z]+)*\b|\b[a-z]+(?:[\'-]?[a-z]+)*\b",
        three)

    file_tokens = "moeckel"
    file_tokens = re.split(r"( )|\n|\-\-|\[|\]|\.|\,|\:|\;|\"|\'|\(|\)|\?|\!|\}|\{|\/", file_tokens)

    print(file_tokens)
    print(special_tokens)



if __name__ == '__main__':
    main()
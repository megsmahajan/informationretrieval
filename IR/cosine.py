import re

def tokenization(lines):
    special_tokens = re.findall(
        r"\w+-\n\w+|[\w\.-]+@[\w\.-]+|\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+|        \B['`].+?['`]\B|[A-Z][a-z']+(?=\s[A-Z])(?:\s[A-Z][a-z']+)+|(?:[a-zA-Z]\.){2,}|\b[A-Z]+(?:\s+[A-Z]+)*\b",
        lines)

    special_tokens = [w.replace('-\n', ' ') for w in special_tokens]

    file_tokens = re.sub(
        r"\w+-\n\w+|[\w\.-]+@[\w\.-]+|\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+|        \B['`].+?['`]\B|[A-Z][a-z']+(?=\s[A-Z])(?:\s[A-Z][a-z']+)+|(?:[a-zA-Z]\.){2,}|\b[A-Z]+(?:\s+[A-Z]+)*\b",
        "", lines)
    #     print(lines)

    file_tokens = re.split(r"( )|\n|\-\-|\[|\]|\.|\,|\:|\;|\"|\'|\(|\)|\?|\!|\}|\{|\/", file_tokens)
    file_tokens = [x for x in file_tokens if x != None and x != ' ' and x != '']
    file_tokens[:] = [x.strip('[-+=]') for x in file_tokens]

    return special_tokens, file_tokens


def calculate_numerator(doc_vec,queryVectors):
    product_of_query_and_doc = {}
    for k, d in doc_vec.items():
        n = [round(a * b, 3) for a, b in zip(d, queryVectors)]
        product_of_query_and_doc[k] = n

    numerator = {}

    for k, e in product_of_query_and_doc.items():
        numerator[k] = round(sum(e), 3)
        # print(numerator)

    return numerator



def calculate_denominator(sum_document_sq):
    denominator = {}
    for k, i in sum_document_sq.items():
        denominator[k] = round(i, 3)

    return denominator





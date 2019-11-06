import re

def tokenization(lines):
    special_tokens_rule_1_and_2 = re.findall(
        r"\w+-\n\w+|^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$|^\d+\.\d+\.\d+\.\d+$|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",lines)

    special_tokens_rule_3 = re.findall(r"|        \B['`].+?['`]\B|[A-Z][a-z']+(?=\s[A-Z])(?:\s[A-Z][a-z']+)+",lines)

    special_tokens_rule_4_and_5 = re.findall(r"\b[a-z]+(?:[\'-]?[a-z]+)*\b|\b[A-Z]+(?:\s+[A-Z]+)*\b",lines)

    special_tokens = special_tokens_rule_1_and_2+special_tokens_rule_3+special_tokens_rule_4_and_5

    special_tokens = [w.replace('-\n', ' ') for w in special_tokens]

    file_tokens_1 = re.sub(
        r"\w+-\n\w+|^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$|^\d+\.\d+\.\d+\.\d+$|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", "",
        lines)

    file_tokens_2 = re.sub(r"|        \B['`].+?['`]\B|[A-Z][a-z']+(?=\s[A-Z])(?:\s[A-Z][a-z']+)+", "",  lines)

    file_tokens_3 = re.sub(r"\b[a-z]+(?:[\'-]?[a-z]+)*\b|\b[A-Z]+(?:\s+[A-Z]+)*\b", "", lines)

    file_tokens = file_tokens_1+file_tokens_2+file_tokens_3

    file_tokens = re.split(r"( )|\n|\-\-|\[|\]|\.|\,|\:|\;|\"|\'|\(|\)|\?|\!|\}|\{|\/", file_tokens)

    final_tokens = []
    for tokens in file_tokens:
        if tokens!=None and tokens!= ' ' and tokens != '':
            final_tokens.append(tokens)

    final_tokens[:] = [tokens.strip('[-+=]') for tokens in final_tokens]

    return special_tokens, final_tokens

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
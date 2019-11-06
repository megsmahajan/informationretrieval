from collections import defaultdict

docs = ["this red car is fast and new toyota is a good brand of car",
        "this automobile is red and the brand is toyota it is not very fast but it is cheap",
        "this green car is fast and the mileage is low",
        "the car with low mileage is under a tree",
        "the green tree is in the park",
        "the automobile is green and this car is cheap",
        "park the car under the tree",
        "the toyota has low mileage and is very cheap",
        "this car is not a good brand",
        "there is a automobile that is red and in the park"]

# split each doc into words
docs = [d.split() for d in docs]
queries = ["car", "toyota", "park", "green car low mileage", "toyota brand car"]
queries = [q.split() for q in queries]
# (i, j) is in the list if query qi is relevant to doc j
query_doc_relevant = [(1,1), (2,1), (5,1), (1,2), (2,2), (5,2), (1,3), (4,3), (1,4),(3,5), (1,6), (1,7), (3,7), (1,8), (2,8), (1,9), (1,10), (3,10)]
query_doc_relevant = [(x-1, y-1) for x, y in query_doc_relevant]

print(query_doc_relevant)

def word_probs(docs):
    """ word_probs(docs)[w] is the fraction of docs that contain w """
    probs = defaultdict(float)
    for d in docs:
        for w in set(d):
            probs[w] += 1.0 / len(docs)

    print(probs)
    return probs

def make_table(only_terms_in_query):
    """ Returns d such that d[i][j] is the probability document i is
    relevant to query j using the RSJ model. If only_terms_in_query is
    True, then equation 16 is used, otherwise equation 17 is used."""
    # estimate Pr(F[j])
    word_priors = word_probs(docs)
    doc_query_prob = defaultdict(lambda: defaultdict(float))
    for qi, query in enumerate(queries):
        rel_docs = [docs[dj] for qj, dj in query_doc_relevant if qj == qi]
        word_given_rel = word_probs(rel_docs)
    # estimate probability doc di is relevant to query qi
    # this is the product of
    for di, doc in enumerate(docs):
        doc_query_prob[qi][di] = 1.0
    # only use the words in the query if only_terms_in_query is True
    for w in (query if only_terms_in_query else word_priors.keys()):
        if w in set(doc):
        # Pr(F[j] = 0 | r, q)/Pr(F[j] = 0)
            doc_query_prob[qi][di] *= word_given_rel[w] / word_priors[w]
        else:
    # Pr(F[j] = 1 | r, q)/Pr(F[j] = 1)
            doc_query_prob[qi][di] *= (1.0 - word_given_rel[w])/(1.0 - word_priors[w])
    return doc_query_prob

def print_table(doc_query_probs):
    for di, doc in enumerate(docs):
        row_probs = [doc_query_probs[qi][di] for qi in range(len(queries))]
    print (' '.join(("%.2f" % p).ljust(9) for p in row_probs))

def main():
    print('the entry at row i and col j is the probability doc i is relevant to query j')
    print('just terms in query')
    print_table(make_table(True))
    print('all terms')
    print_table(make_table(False))


if __name__ == '__main__':
    main()
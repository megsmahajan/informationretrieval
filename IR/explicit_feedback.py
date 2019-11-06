'''
Implement Rocchio algo on a corpus of relevant documents
by weighting based on td-idf to iteratively form a new query vector of weightings
for each unique term across all dictionaries (from invertedFiles) passed into Rocchio
'''

import math
import sys
import constants

class RocchioOptimizeQuery:

    def __init__(self, firstQueryTerm):
        '''
        Constructor
        '''
        self.query = {}
        self.query[firstQueryTerm] = 1

    def Rocchio(self,documentList, relevantDocuments, nonRelevantDocuments):

        relevantDocsTFWeights = {}
        nonrelevantDocsTFWeights = {}
        weights = {}
        termsInRelevantDocs = []
        termsInNonrelevantDocs = []


        allTermsInRelevantAndNonRelevantDocs =[]

        for docId in relevantDocuments:
            realDocId = docId+1

            for key,value in documentList.items():

                if realDocId in value[0].keys():

                    weights[key] = 0.0
                    termsInRelevantDocs.append(key)
                    allTermsInRelevantAndNonRelevantDocs.append(key)

                    if key in relevantDocsTFWeights:
                        relevantDocsTFWeights[key] = relevantDocsTFWeights[key] + value[0][realDocId]
                    else:
                        relevantDocsTFWeights[key] = value[0][realDocId]


        for docId in nonRelevantDocuments:

            realDocId = docId + 1

            for key, value in documentList.items():

                if realDocId in value[0].keys():

                    termsInNonrelevantDocs.append(key)
                    allTermsInRelevantAndNonRelevantDocs.append(key)
                    weights[key] = 0.0

                    if key in nonrelevantDocsTFWeights:
                        nonrelevantDocsTFWeights[key] = nonrelevantDocsTFWeights[key] + value[0][realDocId]
                    else:
                        nonrelevantDocsTFWeights[key] = value[0][realDocId]


        for terms in termsInRelevantDocs:

            idf = documentList[terms][1]

            weights[terms] = weights[terms] + constants.BETA * idf * (relevantDocsTFWeights[terms] / len(relevantDocuments))

        for terms in termsInNonrelevantDocs:

            idf = documentList[terms][1]

            weights[terms] = weights[terms] - constants.GAMMA * idf * (nonrelevantDocsTFWeights[terms] / len(nonRelevantDocuments))

        for allTerms in allTermsInRelevantAndNonRelevantDocs:

            if allTerms in self.query:
                self.query[allTerms] = constants.ALPHA * self.query[allTerms] + weights[allTerms]  # build new query vector of weights
            elif weights[allTerms] > 0:
                self.query[allTerms] = weights[allTerms]

        i = 0
        terms = []
        for term in sorted(self.query, key=self.query.get, reverse=True):
            terms.append(term)
            i = i + 1
            if i>2:
                break

        return terms












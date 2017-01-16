import json
import math
import collections
from pprint import pprint
import numpy

'''
how to do hierarchical clustering?

how to read data:

key is the person who was being reviewed, the keys of the dictionary
that the top level key points to are the coworkers who reviewed and
the numbers they point to are their score out of 5 for the reviewee

want to cluster people based on their coworkers' opinions of them
similar opinions, closer together
'''



def getPearsonCo(r1, r2):
    return numpy.corrcoef(r1, r2)

def cmp(x, y):
        if x[0] < y[0]:
                return -1
        if x[0] > y[0]:
                return 1
        return 0

def getSharedElements(r1, r2):
        n1 = map(lambda x: x[1], sorted([(k, v) for k, v in r1.items() if k in r2], lambda x, y: cmp(x, y)))
        n2 = map(lambda x: x[1], sorted([(k, v) for k, v in r2.items() if k in r1], lambda x, y: cmp(x, y)))
        return [n1, n2]


def getAllScores(reviews):
        scores = collections.defaultdict(int)
        for i in range(len(reviews)-1):
            for j in range(i+1, len(reviews)):
                a = reviews[i]
                b = reviews[j]
                for k, m in a.items():
                    for l, n in b.items():
                        shared = getSharedElements(m, n)
                        scores[k+l] = getPearsonCo(shared[0], shared[1])[0, 1]

        return scores



class Cluster:
    """
            binary tree node
            two child clusters
    """
    def __init__(self, data):
        self.score = 0
        self.children = []

with open('data.json') as data_file:
    delta = .5
    data = json.load(data_file)
    res = getAllScores(data)

    assert res["ab"] >= 0.995341 - delta and res["ab"] <= 0.995341 + delta

    x = Cluster(data)

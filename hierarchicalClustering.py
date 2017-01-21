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

need to make new data every time a new cluster is created
'''



def getPearsonCo(r1, r2):
    return numpy.corrcoef(r1, r2)

def cmp(x, y, accessor, reverse = False):
        if reverse:
            if accessor(x) > accessor(y):
                    return -1
            if accessor(x) < accessor(y):
                    return 1
            return 0
        else:
            if accessor(x) < accessor(y):
                    return -1
            if accessor(x) > accessor(y):
                    return 1
            return 0

def getSharedElements(r1, r2):
        n1 = map(lambda x: x[1], sorted([(k, v) for k, v in r1.items() if k in r2], lambda x, y: cmp(x, y, lambda a: a[0])))
        n2 = map(lambda x: x[1], sorted([(k, v) for k, v in r2.items() if k in r1], lambda x, y: cmp(x, y, lambda a: a[0])))
        return [n1, n2]

def getAllScores(reviews):
        scores = []

        for i in range(len(reviews)-1):
            for j in range(i+1, len(reviews)):
                a = reviews[i]
                b = reviews[j]
                for k, m in a.items():
                    for l, n in b.items():
                        shared = getSharedElements(m, n)
                        score = getPearsonCo(shared[0], shared[1])[0, 1]
                        scores.append((k, l, score))

        return sorted(scores, lambda x, y: cmp(x, y, lambda a: a[2]))

def getClosestPair(reviews):
    '''
        get closest pair
        turn into cluster
        average all data together
        keep score
        score against all other clusters and then find closest clusters again
        continue until only one cluster left
    '''
    allScores = getAllScores(data)
    return allScores.pop()

class HierarchicalCluster:
    """
        manages cluster creation and merging logic
    """
    def __init__(self, data):
        self.clusters = self.initClusters(data)

    def __str__(self):
        output = "["
        for i in range(len(self.clusters)):
            output += self.clusters[i].__str__()

        return output+"]"

    def initClusters(self, data):
        #assumes that data is a list of dicts
        return [ Cluster(d) for d in data ]


class Cluster:
    """
            binary tree node
            two or zero child clusters
    """
    def __init__(self, data, children = []):
        self.score = 1
        self.name = data.keys()[0]
        self.data = data
        self.children = children

        self.initCluster()

    def __str__(self):
        if len(self.children) > 0:
            return "{ score: s=%s, name: n=%s, data: d=%s, children: [x=%s, y=%s] }" % (str(self.score), self.name, self.data , self.children[0].__str__() , self.children[1].__str__())
        return "{ score: s=%s, name: n=%s, data: d=%s, children: [] }" % (str(self.score), self.name, self.data)


    def initCluster(self):
        if len(self.children) > 0:
            #combine child data to get curr data
            c1 = self.children[0]
            c2 = self.children[1]
            childName1 = c1.keys()[0]
            childName2 = c2.keys()[0]
            combinedChildren = { k: (v1 + c2[childName2][k])/2 for k, v1 in c1[childName1].items() if k in c2[childName2] }

            self.data = { childName1 + childName2: combinedChildren }
            self.name = nextName


with open('data.json') as data_file:
   # delta = .05
   data = json.load(data_file)
   # closestPair = getClosestPair(data)
   # print closestPair
   hc = HierarchicalCluster(data)

   print(hc)

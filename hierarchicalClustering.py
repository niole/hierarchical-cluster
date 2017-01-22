import json
import math
import collections
import numpy

'''
key is the person who was being reviewed, the keys of the dictionary
that the top level key points to are the coworkers who reviewed and
the numbers they point to are their score out of 5 for the reviewee

want to cluster people based on their coworkers' opinions of them
similar opinions, closer together
'''


class HierarchicalCluster:
    """
        manages cluster creation and merging logic
    """
    def __init__(self, data):
        self.clusters = []
        self.initClusters(data)

        self.build()


    def __str__(self):
        output = "["
        for i in range(len(self.clusters)):
            output += self.clusters[i].__str__()

        return output + "]"

    def initClusters(self, data):
        #assumes that data is a list of dicts
        self.clusters = [ Cluster(d) for d in data ]

    def build(self):
        clusters = self.clusters

        if len(clusters) > 1:
            '''
                combine more clusters
                get closest pair
                turn into cluster
                average all data together
                keep score
                score against all other clusters and then find closest clusters again
                continue until only one cluster left
            '''
            allScores = self.getAllScores(clusters)
            closestPair = allScores.pop()

            #remove closest pair from clusters and add new combined cluster
            newClusters = []
            newChildren = []
            for c in self.clusters:
                if c.name == closestPair[0] or c.name == closestPair[1]:
                    #combine
                    newChildren.append(c)
                else:
                    #keep in new clusters
                    newClusters.append(c)

            newClusters.append(Cluster({}, newChildren, closestPair[2]))
            self.clusters = newClusters

            return self.build()


    def getPearsonCo(self, r1, r2):
        return numpy.corrcoef(r1, r2)

    def cmp(self, x, y, accessor):
        if accessor(x) < accessor(y):
                return -1
        if accessor(x) > accessor(y):
                return 1
        return 0

    def getSharedElements(self, r1, r2):
            n1 = map(lambda x: x[1], sorted([(k, v) for k, v in r1.items() if k in r2], lambda x, y: self.cmp(x, y, lambda a: a[0])))
            n2 = map(lambda x: x[1], sorted([(k, v) for k, v in r2.items() if k in r1], lambda x, y: self.cmp(x, y, lambda a: a[0])))
            return [n1, n2]

    def getAllScores(self, reviews):
            #reviews are Cluster instances
            scores = []

            for i in range(len(reviews)-1):
                for j in range(i+1, len(reviews)):
                    a = reviews[i]
                    b = reviews[j]

                    shared = self.getSharedElements(a.data, b.data)
                    score = -1

                    if len(shared[0]) > 0:
                        score = self.getPearsonCo(shared[0], shared[1])[0, 1]
                        if math.isnan(score):
                            score = -1

                    scores.append((a.name, b.name, score))

            return sorted(scores, lambda x, y: self.cmp(x, y, lambda a: a[2]))



class Cluster:
    """
            binary tree node
            two or zero child clusters
    """
    def __init__(self, data = {}, children = [], score = 1):
        self.score = score
        self.name = ""
        self.data = data
        self.children = children

        self.initCluster(data)

    def __str__(self):
        if len(self.children) > 0:
            return "{ score: %s, name: %s, data: %s, children: [%s, %s] }" % (str(self.score), self.name, self.data , self.children[0].__str__() , self.children[1].__str__())
        return "{ score: %s, name: %s, data: %s, children: [] }" % (str(self.score), self.name, self.data)

    def getCombinedChildren(self):
        c1 = self.children[0]
        c2 = self.children[1]
        return { k: (v1 + c2.data[k])/2 for k, v1 in c1.data.items() if k in c2.data }

    def initCluster(self, data):
        if len(self.children) > 0:
            self.data = self.getCombinedChildren()
            self.name = "".join(map(lambda c: c.name, self.children))
        else:
            self.name = data.keys()[0]
            self.data = data[self.name]



with open('data.json') as data_file:
    data = json.load(data_file)
    hc = HierarchicalCluster(data)

import json
from pprint import pprint

'''
how to do hierarchical clustering?
'''

with open('data.json') as data_file:
    data = json.load(data_file)

    class MyClass:
        def __init__(self, data):
            """A simple example class"""
            self.data = data

        def f(self):
            return self.data

    x = MyClass(data)
    print(x.f())

from itertools import islice
from distance import DistanceFunctions
import pyarrow as pa


class Similarity:

    def __init__(self):
        self.dist = DistanceFunctions()
        self.dist_funcs = {
            'cosine': self.dist.cosine,
            'manhattan': self.dist.manhattan,
            'haversine': self.dist.haversine,
            "levenshtein": self.dist.levenshtein,
            "cosineText": self.dist.cosineText,
        }

    def getFunctionName(self, func):
        try:
            return func.to_pylist()[0]
        except IndexError as e:
            return func

    def getCenterPoint(self, center):
        return center.to_pylist()[0]

    def getRadius(self, radius):
        return radius.to_pylist()[0]

    def generateDistanceValues(self, func, center, attrib, *args):
        result = []

        func = self.getFunctionName(func)
        center = self.getCenterPoint(center)

        # print(type(attrib))
        # print(attrib)
        # print("b4 for")
        for value in attrib:
            # print(value)
            if func == 'cosine' and not type(value) == list:
                func = 'cosineText'

            if func == 'date':
                radius = args[0]
                unit = args[1]
                distance_value = self.dist_funcs[func](center, value, radius, unit)
            else:

                distance_value = self.dist_funcs[func](center, value)
                
            result.append(distance_value)

        return result

    def knn(self, func, k, center, attrib):
        # TODO review this
        distances = self.generateDistanceValues(func, center, attrib)
        positions = [pos for pos, value in sorted(
            enumerate(distances, start=1), key=lambda x: x[1])]
        # print(positions)
        return positions

    def rangeSim(self, func, radius, center, attrib):
        distances = self.generateDistanceValues(func, center, attrib)
        radius = self.getRadius(radius)

        result = [True if val < radius else False for val in distances]

        return result

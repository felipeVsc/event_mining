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
            "levenshtein":self.dist.levenshtein, 
            "cosineText":self.dist.cosineText,
        }

        # Aqui existem duas condições que tem que ser tratadas: virão duas colunas (lat long) ou um GEOMETRY numa vibe de POINT(X,Y)?? vou implementar primeiro para lat long

    # Para spatial, eu tenho que tratar tudo sempre como "LAT,LONG" não posso sair disso, desconsiderar os outros

    def getFunctionName(self, func):
        try:
            return func.to_pylist()[0]
        except IndexError as e:
            return func
        
    def getCenterPoint(self, center):
        return center.to_pylist()[0]
    
    def getRadius(self, radius):
        return radius.to_pylist()[0]

    def generateDistanceValues(self, func, center, attrib):
        result = []

        func = self.getFunctionName(func)
        center = self.getCenterPoint(center)
        
        for value in attrib:

            if func == 'cosine' and not type(value) == list:
                func = 'cosineText'

            distance_value = self.dist_funcs[func](center, value)
            
            result.append(distance_value)

        return result

    # Ambas funções vão ser apenas knn and range, porque servem para ambas

    def knn(self, func, k, center, attrib):

        distances = self.generateDistanceValues(func, center, attrib)
        # eu tenho uma lista com as distancias e eu tenho que retornar uma lista  com a ordem (1,2,3,4) daquelas distancias
        # entrada = [50, 70, 60] -> saida = [1, 3, 2] 

        # sorted_by_values = dict(
        #     sorted(distances.items(), key=lambda item: item[1]
        
        positions = [pos for pos, value in sorted(enumerate(distances, start=1), key=lambda x: x[1])]

        return positions

    def rangeSim(self, func, radius, center, attrib):
        # Ele vem repetido.. numa lista de mesmo tamanho que os attribs. Ele vem no formato [ [ [LAT,LONG ], [LAT, LONG] ] ]

        distances = self.generateDistanceValues(func, center, attrib)
        radius = self.getRadius(radius)


        # print("distances done")
        # sorted_by_values = dict(
        #     sorted(distances.items(), key=lambda item: item[1]))

        result = [True if val < radius else False for val in distances] 
        
        # 'Divisible by 2' if n % 2 == 0 else 'Divisible by 3'
        
        # {val: sorted_by_values[val]
        #        for val in distances if sorted_by_values[val] < radius}
        
        return result

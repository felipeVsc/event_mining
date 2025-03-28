from functools import partial
import duckdb
import duckdb.typing
from ml import MachineLearning
from visualizations import Visualization
from similarity_func import Similarity
from typing import Union
from duckdb import typing as tp
class EngineDuck:
    
    def __init__(self,host,port,name, user, password):
        self.pg_conn_string = f'host={host} port={port} user={user} password={password} dbname={name}'
        self.con = duckdb.connect()
        self.con.execute(f"INSTALL postgres_scanner; LOAD postgres_scanner; CALL postgres_attach('{self.pg_conn_string}')")
        self.vis = Visualization()
        self.ml = MachineLearning()
        self.sim = Similarity()
    
    def runQuery(self, query):
        result = self.con.execute(query).fetch_df()
        return result
    
    def getPublicMethodsClass(self,obj):
        return [method for method in dir(obj) if callable(getattr(obj, method)) and not method.startswith("_")]

    def _cluster_kmeans_udf(self, *args):
        return self.ml.cluster_kmeans(*args)

    def registerAllMlFunctions(self):
        # This function is responsible for registering all ML Functions

        # Need to define the essential parameters we will let the users choose.. cant be dynamic like it was
        cluster_kmeans_bound = partial(self.ml.cluster_kmeans) # Replicate this partial function for everyone
        self.con.create_function("CLUSTER_KMEANS", cluster_kmeans_bound, parameters=None, return_type=int, type="arrow") # Maybe this wont work
        
        self.con.create_function("CLUSTER_DBSCAN", lambda x: self.ml.cluster_dbscan(x), [float], int, type="arrow") # Maybe this wont work
        
        self.con.create_function("CLASSIFY_KNN", lambda x, y, predict: self.ml.knn_classifier(x,y,predict), [float,float,float], int, type="arrow")

        self.con.create_function("CLASSIFY_DECISION_TREE", lambda x, y, predict, visualize: self.ml.decision_tree(x,y,predict, visualize), [float,float,float, bool], int, type="arrow")

        self.con.create_function("CLASSIFY_LINEAR_REG", lambda x, y, predict: self.ml.linear_regression(x,y,predict), [float,float,float], int, type="arrow")

        return True

    def registerAllVisualizeFunctions(self):
        # TODO test everyone here again with the parameters=None.

        self.con.create_function("LINEPLOT", lambda x, y: self.vis.lineplot(x, y), [float,float], bool, type="arrow")
        
        self.con.create_function("BOXPLOT", lambda x, labels: self.vis.boxplot(x, labels), [float,str], float, type="arrow")

        # eu posso adicionar na chamada do hbar algo como hbar(*args) e provavelmente vai funcionar para pegar a lista de args. a partir disso eu posso checar os tipos e etc 
        
        self.con.create_function("HBAR", lambda x, y: self.vis.hbar(x, y), parameters=None, return_type=float, type="arrow")

        self.con.create_function("PIE", lambda x, labels: self.vis.pie(x, labels), parameters=None, return_type=str, type="arrow")

        self.con.create_function("SCATTER", lambda x, y, c: self.vis.scatter(x, y, c), [list[float],list[float], list[int]], float, type="arrow") #Blob Maybe??

        self.con.create_function("VBAR", lambda x, y: self.vis.vbar(x, y), [float,float], float, type="arrow")

        self.con.create_function("WORDCLOUD", lambda words: self.vis.wordcloud(words), [str], str, type="arrow")
        
        # 'LIST(LIST(FLOAT))'
        # vai vim do banco. como q eu passaria? Porque tem que ser 2d, entao como seria essa representação 2d vinda do banco?
        # self.visualize_functions['HEATMAP'] = self.vis.heatmap # TODO

        return True
        
    def registerAllSimilarityFunctions(self):
        # se não der pra ser assim, posso retornar normal??
        # talvez não, porque eu vou precisar pegar quem são os k mais próximos
        # só se eu fizer algo externo, que mantenha o controle pro knn.. pro range é mais facil, só conferir
        # mas pro knn eu tenho que manter uma lista dos k mais próximos


        # Especificar como esses dados vão chegar 
        self.con.create_function("KNN", lambda func, k, center, attrib: self.sim.knn(func, k, center, attrib), parameters=None, return_type=dict[str, float], type="arrow")
        
        self.con.create_function("RANGE", lambda func, radius, center, attrib: self.sim.rangeSim(func, radius, center, attrib), parameters=None, return_type=float, type="arrow")
        
        """ 
        Para texto:
            Center = [str]
            Attrib = [str, str, str, str] ou [[str], [str], [str]]

            

        Para spatial:
            Center = [LAT,LONG]
            Attrib = [[LAT,LONG], [LAT,LONG], [LAT,LONG]]

        
        Returns = Union Dict {str: float} str -> representação (POINT(X,Y): np.float(distance)
        
        
        """
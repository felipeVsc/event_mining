from functools import partial
import duckdb
import duckdb.typing
from ml import MachineLearning
from visualizations import Visualization
from similarity_func import Similarity
from typing import Union
from duckdb import typing as tp
import sqlparse
from sqlparse.sql import Identifier, Function, IdentifierList
from sqlparse.tokens import Keyword, DML

class EngineDuck:
    
    def __init__(self,host,port,name, user, password):
        self.pg_conn_string = f'host={host} port={port} user={user} password={password} dbname={name}'
        self.con = duckdb.connect()
        self.con.execute(f"INSTALL postgres_scanner; LOAD postgres_scanner; CALL postgres_attach('{self.pg_conn_string}')")
        self.vis = Visualization()
        self.ml = MachineLearning()
        self.sim = Similarity()
        self.functions = ['CLUSTER_DBSCAN', 'CLASSIFY_KNN', 'CLASSIFY_DECISION_TREE', 'CLASSIFY_LINEAR_REG','CLUSTER_KMEANS', 'LINEPLOT', "BOXPLOT", 'HBAR', 'SCATTER', 'PIE', 'VBAR', 'WORDCLOUD']
    
    def wrappingFunctionsWithArrayAgg(self, token):
        token.tokens.insert(0, sqlparse.sql.Token(Keyword, 'array_agg('))
        token.tokens.append(sqlparse.sql.Token(Keyword, ')'))

    def processingTokensForArrayAgg(self, tokens):
        for token in tokens:
            if isinstance(token, Function) and token.get_real_name().upper() in self.functions:
                for arg in token.get_parameters():
                    if isinstance(arg, sqlparse.sql.Identifier) or isinstance(arg,Function):
                        self.wrappingFunctionsWithArrayAgg(arg)
            elif token.is_group:
                self.processingTokensForArrayAgg(token.tokens)

    def transformQueryToArrayAgg(self, query):
        parsed = sqlparse.parse(query)
        for stmt in parsed:
            self.processingTokensForArrayAgg(stmt.tokens)
        return ''.join(str(stmt) for stmt in parsed)

    def runQuery(self, query):
        transformedQuery = self.transformQueryToArrayAgg(query) # This is a workaround for Duckdb's vectorization. Its only needed in ML and Vis functions.
        print(transformedQuery)
        print()
        result = self.con.sql(query).arrow().to_pandas()
        print(result)
        # print("Shape:")
        # print(result.read_next_batch().to_pandas().shape)

        # print("For")
        # for r in result:
        #     print(r.read_next_batch().to_pandas().shape)
        return result
    
    def getPublicMethodsClass(self,obj):
        return [method for method in dir(obj) if callable(getattr(obj, method)) and not method.startswith("_")]

    def registerAllMlFunctions(self):
        # This function is responsible for registering all ML Functions

        # Need to define the essential parameters we will let the users choose.. cant be dynamic like it was
        cluster_kmeans_bound = partial(self.ml.cluster_kmeans) # Replicate this partial function for everyone
        self.con.create_function("CLUSTER_KMEANS", cluster_kmeans_bound, parameters=None, return_type=int, type="arrow") # Maybe this wont work
        
        cluster_dbscan_bound = partial(self.ml.cluster_dbscan) # Replicate this partial function for everyone
        self.con.create_function("CLUSTER_DBSCAN", cluster_dbscan_bound, parameters=None, return_type=int, type="arrow") # Maybe this wont work
        
        knn_classifier_bound = partial(self.ml.knn_classifier) # Replicate this partial function for everyone
        self.con.create_function("CLASSIFY_KNN", knn_classifier_bound, parameters=None, return_type=int, type="arrow")

        decision_tree_bound = partial(self.ml.decision_tree) # Replicate this partial function for everyone
        self.con.create_function("CLASSIFY_DECISION_TREE", decision_tree_bound, parameters=None, return_type=list[int], type="arrow")

        linear_regression_bound = partial(self.ml.linear_regression) # Replicate this partial function for everyone
        self.con.create_function("CLASSIFY_LINEAR_REG", linear_regression_bound, parameters=None, return_type=int, type="arrow")

        return True

    def registerAllVisualizeFunctions(self):
        # TODO test everyone here again with the parameters=None.
        # And then, change for receiving a list   ax.barh(y.to_pylist()[0], x.to_pylist()[0], **kwargs) <- like this

        self.con.create_function("LINEPLOT", lambda x, y: self.vis.lineplot(x, y), parameters=None,return_type=bool, type="arrow")
        
        self.con.create_function("BOXPLOT", lambda x, labels: self.vis.boxplot(x, labels), parameters=None, return_type=bool, type="arrow")

        self.con.create_function("HBAR", lambda x, y: self.vis.hbar(x, y), parameters=None, return_type=bool, type="arrow")

        self.con.create_function("PIE", lambda x, labels: self.vis.pie(x, labels), parameters=None, return_type=bool, type="arrow")

        self.con.create_function("SCATTER", lambda x, y, c: self.vis.scatter(x, y, c), parameters=None, return_type=bool, type="arrow") #Blob Maybe??

        self.con.create_function("VBAR", lambda x, y: self.vis.vbar(x, y), parameters=None, return_type=bool, type="arrow")

        self.con.create_function("WORDCLOUD", lambda words: self.vis.wordcloud(words), parameters=None, return_type=bool, type="arrow")
        
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
from collections import defaultdict

import duckdb
from db_executor import DbExecutor

class Engine:

    def __init__(self):
        self.DATAFRAMES = {}
        self.TABLES = defaultdict(list)

    @property
    def getTablesDataframes(self):
        return self.DATAFRAMES
    
    def getListOfTablesFromQuery(self, root):
        # root = build_scope(ast)

        for index,scope in enumerate(root.traverse()):
            tableName = str(scope.tables[0])
            columnUsed = str(scope.columns[0]) 
            self.TABLES[tableName].append(columnUsed)

        return self.TABLES            
    
    def read_from_db(self):
        executor = DbExecutor(db_engine="postgres", db_name="postgres",
            user="postgres",
            password="password",
            host="localhost",
            port="5432")
        
        for table in self.TABLES.keys():

            query_string = f"SELECT {", ".join(self.TABLES[table])} FROM {table};"

            df = executor.queryPostgres(query_string)
    
            self.DATAFRAMES[table] = df
        
        return True

    def getArgsFromExpr(self, expression):
    # Talvez isso aqui vá ter diferentes valores na lista, então vai ter que fazer um loop
        args_list = expression.this
        return [arg.name for arg in args_list]

    def getClassNameFromExpr(self, expression):
        return expression.__class__.__name__

    def runFunctionExpr(self):

        args = self.getArgsFromExpr()
        pass

    def processSelectStatements(self, expr):
    # This function will iterate over Select expressions

        for expression in expr:
            name = self.getClassNameFromExpr(expr)

            # Check if is an alias
            if name == "Alias":
                expression = expression.this
            
            # I do not need to check for everythign else (such as only columns and etc because this will get recognized by the sql engine)
            if name not in udf_registry:
                print("erro")

            argsList = [expression.this.name for expression.this in expression]

            udf_registry[name].execute(*argsList)
            # Vai passar tudo em String, então teria que converter, pegar as coisas que for dos DF e etc
            


    def runSqlInDataframes(self,query):
        results = duckdb.query(query)
        return results.to_df() 
        


""" 
-> Pegar os dados das tabelas [OK]
-> Colocar tudo num DF [OK]
-> Lidar primeiro com os With 
-> Rodar os comandos do with, criando as CTEs
-> Rodar as queries básicsa "SELECT Cluster(price) FROM table" e salvra nos CTEs
-> Rodar o restante das queries já salvando os CTEs nos self.TABLE
-> Rodar os joins e etc com o duckdb


"""
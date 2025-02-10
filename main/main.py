class Main:
    # Essa classe vai ser responsável por ler e executar as coisas
    pass

# Simulando um DataFrame de entrada
df = pd.DataFrame({
    "id": range(1, 10),
    "price": [10, 20, 30, 200, 220, 250, 1000, 1100, 1200],
})

# Query SQL simulada
query = """
WITH resultados_cluster AS (SELECT CLUSTER(price) FROM df)  
SELECT * FROM resultados_cluster;
"""

# Parseando a query
expression = sqlglot.parse_one(query, dialect=CustomDialect)

# Encontrar a expressão CLUSTER na AST
cluster_expr = expression.find(Cluster)

# Executar a função CLUSTER e gerar um DataFrame com os resultados
df_clusterizado = cluster_expr.to_cte(df)

# Exibir o DataFrame final com os clusters
print(df_clusterizado)

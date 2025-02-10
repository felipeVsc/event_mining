class Language:
    # this file will only hold the information from the language (this will be implemented through sqlglot)
    pass


class Cluster(Func):
    arg_count = 1  # Aceita apenas 1 argumento (coluna)

    def execute(self, data):
        """
        Executa o algoritmo de clustering e retorna um DataFrame tabular.

        :param data: Lista de valores da coluna selecionada.
        :return: DataFrame representando os clusters.
        """
        if not isinstance(data, (list, np.ndarray, pd.Series)):
            raise ValueError("Os dados precisam ser uma lista ou array.")

        # Convertendo para array NumPy
        data = np.array(data).reshape(-1, 1)

        # Criando o modelo K-Means com 3 clusters
        kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
        clusters = kmeans.fit_predict(data)

        # Criando DataFrame com os resultados
        df_clusters = pd.DataFrame({"original_value": data.flatten(), "cluster": clusters})

        return df_clusters

    def to_cte(self, alias="resultados_cluster", data=None):
        """
        Gera uma CTE a partir da execução do clustering.

        :param alias: Nome da CTE.
        :param data: Lista de valores extraídos do banco de dados.
        :return: String SQL com a CTE gerada.
        """
        if data is None:
            raise ValueError("Os dados precisam ser fornecidos para a CTE.")

        df = self.execute(data)  # Executa o clustering
        columns = ", ".join(df.columns)  # Nome das colunas
        values = ", ".join(
            f"({', '.join(map(str, row))})" for row in df.values
        )  # Transformando valores para SQL

        # Criando a CTE
        return f"WITH {alias} AS (SELECT {columns} FROM (VALUES {values}) AS t({columns}))"


# Criando um dialeto personalizado para reconhecer CLUSTER()
class CustomDialect(Dialect):
    class Parser(Parser):
        FUNCTIONS = {**Parser.FUNCTIONS, "CLUSTER": Cluster.from_arg_list}

    class Generator(Generator):
        TRANSFORMS = {
            **Generator.TRANSFORMS,
            Cluster: lambda self, expr: f"CLUSTER({self.sql(expr.this)})",
        }


from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans, DBSCAN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MachineLearning:

    def __init__(self):
        pass

    def decision_tree(self,*args):
        """ 
        This function will create a decision Tree.

        Args:

        x - Data
        y - Label data
        predict - Data to predict
        visualize: boolean - If True, an image of the tree is saved
        """
        visualize = args[-1].to_pylist()[0]
        predict = args[-2].to_pylist()[0]
        y = args[-3].to_pylist()[0]

        argsToColumns = [column.to_pylist() for column in args[1:-3]]
        df_x = pd.DataFrame(np.array(argsToColumns).T, columns=[f"l{i+1}" for i in range(len(argsToColumns))])

        classifier = tree.DecisionTreeClassifier().fit(df_x, y)
        classifier_results = classifier.predict(predict)

        if visualize:
            fig, ax = plt.subplots()
            tree.plot_tree(classifier)
            fig.savefig("./tree.png")

        return classifier_results

    def linear_regression(self, *args):
        """ 
        This function will create a linear regression.

        Args:

        x - Data
        y - Label data
        predict - Data to predict
        """

        predict = args[-1].to_pylist()[0]
        y = args[-2].to_pylist()[0]

        argsToColumns = [column.to_pylist() for column in args[1:-2]]
        df_x = pd.DataFrame(np.array(argsToColumns).T, columns=[f"l{i+1}" for i in range(len(argsToColumns))])

        classifier = LinearRegression().fit(df_x, y)
        classifier_results = classifier.predict(predict)

        return classifier_results

    def knn_classifier(self, *args):
        """ 
        This function will create a KNN classifier

        Args:

        x - Data
        y - Label data
        predict - Data to predict
        """
        k = args[0].to_pylist()[0]
        y = args[-2].to_pylist()[0]
        predict = args[-1][0].as_py()
        print(len(args[1].to_pylist()))
        print(predict)
        # predict pode ser multiplas colunas, não apenas uma. tem que testar como quef ficaria com o []
        # print(args[1][0])

        # argsToColumns = [column.to_pylist() for column in args[1]]
        print(type(args[1][0].as_py()[0][0]))
        print(len(args[1][0]))
        df_x = pd.DataFrame(args[1][0].as_py(), columns=[f"l{i+1}" for i in range(3)])
        print("hiii")
        print(df_x)
        # print(y)

        for col in df_x.columns:
            df_x[col] = df_x[col].astype(float)
        print(df_x.dtypes)

        classifier = KNeighborsClassifier(n_neighbors=k).fit(df_x, y)
        print("erro no classifer")
        classifier_results = classifier.predict(predict)
        print("its here then")
        return classifier_results

    def cluster_kmeans(self, *args):
        k = args[0].to_pylist()[0]
        argsToColumns = [column.to_pylist() for column in args[1:]]
        print(len(argsToColumns[0]))


        df = pd.DataFrame(np.array(argsToColumns).squeeze().T, columns=[f"l{i+1}" for i in range(len(argsToColumns))])

        cluster = KMeans(k).fit_predict(df)
        print("Cluster called")
        import pyarrow as pa
        print(cluster)
        print(len(cluster))
        return [cluster]

    def cluster_dbscan(self, x, **kwargs):
        cluster = DBSCAN(**kwargs).fit(x)
        results = cluster.labels_

        return results

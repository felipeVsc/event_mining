from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans, DBSCAN
import pandas as pd
import matplotlib.pyplot as plt


class MachineLearning:

    def __init__(self):
        pass

    def decision_tree(self, x, y, predict, visualize=False, **kwargs):
        """ 
        This function will create a decision Tree.

        Args:

        x - Data
        y - Label data
        predict - Data to predict
        visualize: boolean - If True, an image of the tree is saved
        """

        classifier = tree.DecisionTreeClassifier(**kwargs).fit(x, y)
        classifier_results = classifier.predict(predict)

        if visualize:
            fig, ax = plt.subplots()
            tree.plot_tree(classifier)
            fig.savefig("./tree.png")

        return classifier_results

    # TODO Isso aqui deveria receber um DF contendo as coisas exatas e ele ja processar-
    def linear_regression(self, x, y, predict, **kwargs):
        """ 
        This function will create a linear regression.

        Args:

        x - Data
        y - Label data
        predict - Data to predict
        """

        classifier = LinearRegression(**kwargs).fit(x, y)
        classifier_results = classifier.predict(predict)

        return classifier_results

    def knn_classifier(self, x, y: pd.DataFrame, predict, **kwargs):
        """ 
        This function will create a KNN with k equals to number of classes - 1.

        Args:

        x - Data
        y - Label data
        predict - Data to predict
        """
        x = x.to_numpy().reshape(-1, 1)
        k = len(y.unique())-1
        classifier = KNeighborsClassifier(n_neighbors=k, **kwargs).fit(x, y)
        classifier_results = classifier.predict(predict)

        return classifier_results

    def cluster_kmeans(self, x, **kwargs):
        x = x.to_numpy().reshape(-1, 1)
        cluster = KMeans(**kwargs).fit_predict(x)

        return cluster

    def cluster_dbscan(self, x, **kwargs):
        cluster = DBSCAN(**kwargs).fit(x)
        results = cluster.labels_

        return results

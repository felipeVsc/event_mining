import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import pyarrow as pa
import pyarrow.compute as pc
import numpy as np


class Visualization:
    """
    This file represents a matplotlib wrapper, so you can use this class to create visualization such as 
    line plots, bar plots and others. It is possible to use any arguments available in matplotlib.

    Every visualization will create a image saved on the path and return True.

    """

    def __init__(self, path="./"):
        self.path = path+"figure.png"

    def lineplot(self, x, y, **kwargs):
        """ 
        Plot Y or multiples Y vs X in a line/markers

        x: X-axis values
        y: Y-axis values. If contains multiple arrays (e.g [[1,2,3],[3,2,1]]), every array will represent a new Y-axis.
        label: Label of each line
        linestyle: The style of the lines (default is '-', others are '--, '-.' and etc.)
        color: Color of the line.
        marker: Enables markers ('o', 's', '^', etc.).
        """
        try:
            fig, ax = plt.subplots()
            ax.plot(x.to_pylist()[0], y.to_pylist()[0], **kwargs)

            if 'label' in kwargs:
                fig.legend(kwargs['label'])

            fig.savefig(self.path)

        except Exception as e:
            raise e

        return [True]*len(x)

    def vbar(self, x, y, **kwargs):
        """ 
        Plot a vertical bar.

        x: Values on the X-axis.
        y: Height of the bars. If it contains more than one array, it indicates a stacked bar.
        color: Fill color of the bars.
        label: Label for the legend of the bars.
        """
        try:
            fig, ax = plt.subplots()
            ax.bar(x.to_pylist()[0], y.to_pylist()[0], **kwargs)
            fig.savefig(self.path)

        except Exception as e:
            raise e

        return [True]*len(x)

    def hbar(self, y, x, **kwargs):
        """ 

        Plot a horizontal bar.

        y: Values on the Y-axis.
        x: Height of the bars. If it contains more than one array, it indicates a stacked bar.
        color: Fill color of the bars.
        label: Label for the legend of the bars.
        """
        try:
            # TODO como vem uma lista agora, então tem que mudar pro [0]
            fig, ax = plt.subplots()
            ax.barh(y.to_pylist()[0], x.to_pylist()[0], **kwargs)
            fig.savefig(self.path)

        except Exception as e:
            return e

        return [True]*len(x)

    def scatter(self, x, y, c, **kwargs):
        """ 
        Plot a scatter X vs Y and saves the result into a png.

        x: Values on the X-axis.
        y: Values on the Y-axis.
        """
        try:
            print(type(c[0]))
            print(c.to_pylist()[0])
            print()
            print(c[0].as_py())
            print(len(c[0].as_py()))
            print(type(c[0].as_py()))
            fig, ax = plt.subplots()
            ax.scatter(x.to_pylist()[0], y.to_pylist()
                       [0], c=c[0].as_py(), **kwargs)
            fig.savefig(self.path)

        except Exception as e:
            raise e

        return [True]*len(x)

    def pie(self, x, labels, **kwargs):
        """ 
        Plots a pie chart and saves the result into a png.

        x: Sequence of values (proportions or frequencies).
        labels: Labels for the slices.
        colors: Colors for each slice.
        """
        try:
            fig, ax = plt.subplots()
            ax.pie(x.to_pylist()[0], labels=labels[0], **kwargs)
            fig.savefig(self.path)

        except Exception as e:
            raise e

        return [True]*len(labels)

    def boxplot(self, x, labels, **kwargs):
        """ 
        Generates a boxplot.

        data: Data to plot (list or array).
        bootstrap: Whether to use bootstrap or not.
        tick_labels: Labels for the data groups.
        """
        try:
            fig, ax = plt.subplots()
            ax.boxplot(x.to_pylist()[0],
                       labels=labels.to_pylist()[0], **kwargs)
            fig.savefig(self.path)

        except Exception as e:
            raise e

        return [True]*len(labels)

    def heatmap(self, data1, data2, **kwargs):
        """ 
        Plots a heatmap.

        data: 2D matrix of values to create the heatmap.
        cmap: Color map. It is defined as an integer but should be mapped to one of the color groups: 'viridis', 'hot', 'coolwarm'.
        """
        try:
            fig, ax = plt.subplots()
            # TODO fix this
            features = np.column_stack(
                (data1.to_pylist()[0], data2.to_pylist()[0]))
            ax.imshow(features, **kwargs)
            fig.savefig(self.path)

        except Exception as e:
            raise e

        return [True]*len(data1)

    def wordcloud(self, data):
        """
        Plots a wordcloud using WordCloud lib.

        data: column containing the phrases to be used
        columnName: the name of the column used
        """

        def clean_words(word):
            word = word.replace(".", "")
            word = word.replace(",", "")
            word = word.replace("'s", "")
            word = word.replace("'s", "")
            word = word.replace("‘", "")

            return word.lower()

        data = pc.drop_null(data)
        data = data[0].as_py()

        try:
            words = pc.list_flatten(pc.utf8_split_whitespace(data))

            cleaned_words = [clean_words(word.as_py()) for word in words]

            words_to_singlestring = " ".join(cleaned_words)

            wordcloud = WordCloud(background_color="white").generate(
                words_to_singlestring)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud)
            fig.savefig(self.path)

        except Exception as e:
            raise e

        return [True]

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from dateutil.parser import parse
from sentence_transformers import SentenceTransformer


class Helpers:
    """
    This file contains helpers functions such as removing null from a DataFrame and generating text embbeddings.
    """

    def __init__(self):
        self.model_path = "../all-MiniLM-L6-v2"

    def setModelPath(self, model):
        """
        This function will set the embedding model to be used.

        The default model is "all-MiniLM-L6-v2"
        """
        self.model_path = model


    def remove_null(self, df: pd.DataFrame):
        """ 
        This function will drop null values from a DataFrame and reset its index.

        Parameters:

        df: DataFrame

        Returns: DataFrame
        """
        return df.dropna(axis='index', ignore_index=True)

    def data_scaling(self, df: pd.DataFrame):
        """ 
        This function will normalize the DataFrame between 0 and 1 using MinMaxScaler

        Parameters:

        df: DataFrame

        Returns: Transformed array
        """

        scaler = MinMaxScaler()
        return scaler.fit_transform(df)

    def data_encoding(self, df: pd.DataFrame):
        """ 
        This function will turn categorical values into numeric values using OneHotEncoder.

        This is required by some classifiers.

        Parameters:

        df: DataFrame

        Returns: Transformed array
        """

        onehot_encoder = OneHotEncoder()
        return onehot_encoder.fit_transform(df)

    def date_formater(self, date: str):
        """ 
        This function will parse the date to ISO format YYYY-MM-DD

        Parameters:

        date: str

        Returns:

        date 
        """
        date_object = parse(date)
        iso_format = date_object.strftime('%Y-%m-%d')  # TODO check this

        return iso_format

    def generate_text_embedding(self, text: str):
        """ 
        This will use a all-MiniLM-L6-v2 model to generate text embbedings for cosine similarity.

        The model used is available at https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

        Parameters:

        text: str

        Returns:

        np.array
        """
        model = SentenceTransformer(self.model_path)
        return model.encode(text)

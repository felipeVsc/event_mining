import pandas as pd
import psycopg2


class DbExecutor:

    def __init__(self, db_engine, db_name, user, password, host, port):
        self.db_engine = db_engine
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connectPostgres(self):
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def disconnectPostgres(self):
        self.cursor.close()
        self.conn.close()

        return True

    def queryPostgres(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        return pd.DataFrame(rows, columns=columns)


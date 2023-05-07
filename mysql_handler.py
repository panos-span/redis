__authors__ = 'Panagiotis Spanakis, Emmanouil Dellatolas'

import mysql.connector as mysql


class MySQLHandler:
    """
    Class that handles the connection to the database

    Attributes
    ----------
    host : str
        The host of the database
    user : str
        The user of the database
    password : str
        The password of the database
    database : str
        The database name
    connection : mysql.connector.connection.MySQLConnection
        The connection to the database
    cursor : mysql.connector.cursor.MySQLCursor
        The cursor of the database
    """

    def __init__(self):
        """
        Constructor of the class
        """
        self.host = '195.251.249.131'
        self.user = 'ismgroup52'
        self.password = 'fk3qqz'
        self.database = 'ismgroup52'
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Connect to the database

        :return: nothing
        """
        self.connection = mysql.connect(host=self.host, port=3306,
                                        user=self.user,
                                        password=self.password,
                                        database=self.database)
        self.cursor = self.connection.cursor()

    def select(self, query):
        """
        Execute a select query

        :param query:
        :return: result of the query
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute(self, query, values):
        """
        Execute a query

        :param query: the query to execute
        :param values: the values to insert
        :return: result of the query
        """
        self.cursor.execute(query, values)
        self.connection.commit()

    def close(self):
        """
        Close the connection to the database

        :return: nothing
        """
        self.connection.close()
        self.cursor.close()

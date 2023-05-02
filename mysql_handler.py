import mysql.connector as mysql

class MySQLHandler:

    def __init__(self):
        self.host = '195.251.249.131'
        self.user = 'ismgroup52'
        self.password = 'fk3qqz'
        self.database = 'ismgroup52'
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connect(host=self.host, port=3306,
                                        user=self.user,
                                        password=self.password,
                                        database=self.database)
        self.cursor = self.connection.cursor()
        print("Connected to database")

    # Get select query
    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()
        self.cursor.close()

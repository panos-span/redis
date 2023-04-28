import mysql.connector as mysql
import pandas as pd
from objects import User
import threading
from scheduler import Scheduler


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

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()
        self.cursor.close()


connection = MySQLHandler()
connection.connect()
x = pd.DataFrame(connection.select("SELECT * FROM `users`"), columns=['id', 'username', 'age', 'Gender', 'email'])
# get row where username = nolis
print(x.iloc[0])
kwargs = x.iloc[0].to_dict()
user = User(**kwargs)
print(user.name)
scheduler = Scheduler()
threading.Timer(60.0, scheduler.checkActiveMeetings()).start()

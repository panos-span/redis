import redis


class RedisHandler:

    def __init__(self):
        self.connection = redis.Redis(host='localhost', port=6379, db=0)

    def executeQuery(self, query):
        return self.connection.execute_command(query)

    def __getattr__(self, item):
        return self.__dict__[item]

    def disconnect(self):
        self.connection.close()

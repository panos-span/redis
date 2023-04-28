from redis import Redis

if __name__ == "main":
    connection = Redis(host='localhost', port=6379, db=0)
    connection.g

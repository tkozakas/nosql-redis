import redis

from src.Interface import Interface
from src.Rent import Rent
from src.User import User

if __name__ == '__main__':
    connection = redis.Redis(host='localhost', port=6379, db=0)
    connection.flushdb()

    user = User(connection)
    rent = Rent(connection)
    interface = Interface(rent, user)
    interface.authentication()

import redis

import datetime
from datetime import datetime, timedelta

class RedisStore():


    def __init__(self, ip='localhost', port=6379, db=0, initial_flush=False):
        self.redis_server = redis.Redis(ip, port, db)
        if initial_flush:

            self.redis_server.flushdb()

    def contains(self, key):
        return bool(self.redis_server.get(key))

    def get_item(self, key):
        data = self.redis_server.get(key)
        if data:
            self.redis_server.expire(key, timedelta(minutes=15))
            return data
        else:
            return None

    def set_item(self, key, value):

        self.redis_server.set(key, value)
        self.redis_server.expire(key, timedelta(minutes=15))
        return key


    def del_item(self, key):
        self.redis_server.delete(key)

    def cleanup(self, timeout):
        pass

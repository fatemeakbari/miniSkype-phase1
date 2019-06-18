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
            #self.redis_server.expire(key, timedelta(minutes=15))
            return data
        else:
            return None

    def set_item(self, key, value):

        self.redis_server.set(key, value)
        #self.redis_server.expire(key, timedelta(minutes=15))
        return key


    def del_item(self, key):
        self.redis_server.delete(key)

    def cleanup(self, timeout):
        pass



class ChatStore():

    def __init__(self, ip='localhost', port=6379, db=0, initial_flush=False):
        self.redis_server = redis.Redis(ip, port, db)
        if initial_flush:
            self.redis_server.flushdb()


    def hmsetall(self, key, value):
        self.redis_server.hmset(key, value)

    def hmset(self, key, id1, value):
        dic = self.redis_server.hgetall(key)
        print(dic)
        dic[id1] = value

        self.redis_server.hmset(key, dic)

    def hmgetall(self, key):
        return self.redis_server.hgetall(key)

    def hmget(self, key, id1):
        dic = self.redis_server.hgetall(key)
        data = dic[id1]
        if data != None:
            return data
        return None


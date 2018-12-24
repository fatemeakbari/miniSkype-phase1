#from auth import RedisStore
from flask_restplus import Api

from flask_mongoengine import MongoEngine
from auth import RedisStore

redis_store = RedisStore()

db = MongoEngine()
api = Api(version ='1.0', title='Nimble Knight Document', description="simple doc of nimble knight's API")

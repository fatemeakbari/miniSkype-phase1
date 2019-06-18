#from auth import RedisStore
from flask_restplus import Api

from flask_mongoengine import MongoEngine
from auth import RedisStore, ChatStore

redis_store = RedisStore()
chat_store = ChatStore()

db = MongoEngine()
api = Api(version ='1.0', title='Skype Document', description="simple doc of Skype's API")

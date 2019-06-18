import datetime
from bson import ObjectId
from flask_mongoengine import MongoEngine
from dashboard import db
#from Friend import Friend

#db = MongoEngine()


class Chats(db.Document):
    
    Username = db.StringField(required=True)
    Message= db.StringField()
    RoomID = db.IntField( max_length=150, unique=True)
    

    def insertMessage(username, message):
	    try:
	     
	        chat = Chats(Username=username, message=message)
	        chat.save()
	        return chat
	    except:
	        return None


    def insertRoomID(roomID):
	    try:
	        chat = Chats(RoomID = roomID)
	        chat.save()
	        return chat
	    except:
	        return None

    def getMessages(roomID):
	    try:
	        chats = Users.objects(RoomID=roomID)
	        return chats
	    except:
	        return None

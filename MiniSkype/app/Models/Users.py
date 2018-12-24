import datetime
from bson import ObjectId
from flask_mongoengine import MongoEngine
from dashboard import db
#from Friend import Friend

#db = MongoEngine()


class Users(db.Document):
    _id = db.ObjectIdField(required=True, default=ObjectId, primary_key=True)
    #SessionId = db.ObjectIdField(required=True, default=ObjectId)
    Username = db.StringField(required=True, max_length=17, unique=True)
    Password = db.StringField(required=True, max_length=256)
    Email = db.StringField(required=False, max_length=150, unique=True)
    #Stats = db.EmbeddedDocumentField(Stats)
    Online = db.BooleanField(required=False, default=False)  # to code avali false bood

    #Friends = db.ListField(db.StringField())
    #Friends_Count = db.IntField(required=True, default=0)  # friend count

    def insertUser(username, password, email):
	    try:
	     
	        user = Users(Username=username, Password=password, Email=email)
	        user.save()
	        return user
	    except:
	        return None


    def getUserByUsername(username):
	    try:
	        user = Users.objects(Username=username).first_or_404()
	        return user
	    except:
	        return None

    def getUserByEmail(email):
	    try:
	        user = Users.objects(Email=email).first_or_404()
	        return user
	    except:
	        return None


    def getUserByUsernameAndPassword(username, password):
	    try:
	     
	        user = Users.objects(Username=username, Password=password).first_or_404()
	        return user
	    except:
	        return None


    def getUserByEmailAndPassword(email, passsword):
	    try:
	        user = Users.objects(Email = email, Passsword = passsword)
	        return user
	    except:
	        return None
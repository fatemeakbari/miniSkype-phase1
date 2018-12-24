
from flask import Flask, redirect, render_template, url_for, request, Blueprint, jsonify
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from API import *
from Models import *
from dashboard import db, api
from flask_sse import sse

flask_app = Flask(__name__)
admin = Admin()



#database config
flask_app.config["MONGO_URI"] = "mongodb://fateme:qwe321567UY@localhost:27017/chatRoom"

#app config
flask_app.config['DEBUG'] = True


#swagger config
flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
flask_app.config['RESTPLUS_VALIDATE'] = True
flask_app.config['RESTPLUS_MASK_SWAGGER'] = False

flask_app.config["REDIS_URL"] = "redis://localhost"


blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
#api.add_namespace(blog_posts_namespace)
flask_app.register_blueprint(blueprint)
#---add blueprint ---> bashe khob hala :)
flask_app.register_blueprint(sse, url_prefix='/stream')

db.app = flask_app
db.init_app(flask_app)
#db.create_all()

@flask_app.route("/chatRoom", methods=["GET"])
def chatRoom():
	return render_template('home.html')


@flask_app.route("/createChatRoom", methods = ["GET"])
def login():
	print("hyyyyyyyyyyyyy")
	
	test = {"username":"name"}
	#print(name)

	return jsonify(test)


@flask_app.route('/')
def home():
	return render_template('login.html')

@flask_app.route('/index')
def index():
    return render_template("index.html")	

admin = Admin(flask_app)
admin.add_view(ModelView(Users))

if __name__ == '__main__':
     flask_app.run(debug = True, host='0.0.0.0', port=5008)

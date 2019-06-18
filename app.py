
from flask import Flask, redirect, render_template, url_for, request, Blueprint, jsonify
from flask_socketio import SocketIO
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from API import *
from Models import *
from dashboard import db, api
from flask_sse import sse

flask_app = Flask(__name__)
admin = Admin()

flask_app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(flask_app)

#database config
flask_app.config["MONGO_URI"] = "mongodb://samin:samin@localhost:27017/chatDB"

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

'''
#......................................................
@flask_app.route("/chatRoom", methods=["GET"])
def chatRoom():
	return render_template('chat.html')
#......................................................
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')
'''
@flask_app.route("/createVideoCall", methods=["GET"])
def createV():
	return render_template('create.html')


@flask_app.route("/joinVideoCall", methods=["GET"])
def joinV():
	return render_template('join.html')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

#/..........................................................................

@flask_app.route("/home")
def home2():
	username = request.args.get('username')
	session_id = request.args.get('session_id')
	return render_template('home.html', username= username, session_id=session_id)



@flask_app.route('/')
def home():
	return render_template('login.html')

@flask_app.route('/index')
def index():
    return render_template("z.html")	

admin = Admin(flask_app)
admin.add_view(ModelView(Users))
admin.add_view(ModelView(Chats))

if __name__ == '__main__':
     socketio.run(flask_app, debug=True, host='0.0.0.0', port=5006)

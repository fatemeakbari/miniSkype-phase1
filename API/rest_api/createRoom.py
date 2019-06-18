from flask_restplus import Resource
from flask import request, make_response, jsonify
from flask_sse import sse
from werkzeug.security import check_password_hash
import hashlib
import string
from Models import *
from dashboard import api, redis_store, chat_store
from API.dataModel import createRoom_model

import random
ns = api.namespace('/')





@ns.route('/createRoom')
class CreateRoom(Resource):

    @api.expect(createRoom_model)
    def post(self):
        """
        create chatRoom
        """
        print("this is CreateRoom")
       
        data = request.json
        session_id = data['session_id']
        calleeUsername = data['calleeUsername']

        print(data)

        username = redis_store.get_item(session_id)
        if not username:
            return ({'Status' : 'Please Login'})

        username = username.decode('utf-8')   
        
        #generate random Room ID
        chars = string.ascii_uppercase + string.digits
        roomID = ''.join(random.choice(chars) for _ in range(8))

        #generate callee ssesion id
        calleeUsername = str(calleeUsername)
        calleeSession_id = hashlib.sha256(calleeUsername.encode()).hexdigest()

        print(1)
        #save roomid in chat_store
        #value = {'caller':username, 'message':''}
        #chat_store.hmsetall(roomID, value)
        #chat_store.hmset(roomID, 'message', 'hy')


        #check callee is login and send chat request\
     
        print(calleeUsername)
        print(2)
        if(redis_store.get_item(calleeSession_id) != None):
            print(3)
            sse.publish({"state": "invite",'roomID':roomID, "callerUsername":username}, type=calleeUsername+'calleeEvent')
            return jsonify({'status': 200, 'message': ' send your invitation to '+ calleeUsername ,
                'roomID': roomID})

        #sse.publish({"message": "Hello!"}, type='greeting')

        return jsonify({'status': 400})


from flask_restplus import Resource
from flask import request, make_response, jsonify
from flask_sse import sse
from werkzeug.security import check_password_hash
import hashlib
import string
from Models import *
from dashboard import api, redis_store
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



        username = redis_store.get_item(session_id)
        if not username:
            return ({'Status' : 'Please Login'})

        username = username.decode('utf-8')   
        print(type(username))
        #generate random Room ID
        chars = string.ascii_uppercase + string.digits
        roomID = ''.join(random.choice(chars) for _ in range(8))

        #generate callee ssesion id
        calleeUsername = str(calleeUsername)
        calleeSession_id = hashlib.sha256(calleeUsername.encode()).hexdigest()
        #check calle is login and send chat request\
        

        print("22")
        print(calleeUsername)
        sse.publish({"state": "invite", "callerUsername":username}, type=calleeUsername)
        if(redis_store.get_item(calleeSession_id) != None):
            sse.publish({"state": "invite", "callerUsername":username}, type=calleeUsername)
            return jsonify({'status': 200, 'message': ' send your invitation to '+ calleeUsername ,
                'roomID': roomID})

        #sse.publish({"message": "Hello!"}, type='greeting')

        return jsonify({'status': 400})


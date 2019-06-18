from flask_restplus import Resource
from flask import request, make_response, jsonify
from flask_sse import sse
from werkzeug.security import check_password_hash
import hashlib

from Models import *
from dashboard import api, redis_store
from API.dataModel import invite_model
ns = api.namespace('/')


@ns.route('/invite')
class Invite(Resource):

    @api.expect(invite_model)
    def post(self):
        """
        login
        """
        print("this is invite.py   ")
        data = request.json
        session_id = data['session_id']
        audience = data['audience']


        if not data or not session_id or not audience:
            return ({'Status': 'Please Fill All Fields'})
        sse.publish({"message": "Hello!"}, type='greeting')

        return jsonify({'Status': 'Success', 'session_id': session_id})
        '''
        username = redis_store.get_item(session_id)

        if not username:
            return ({'Status' : 'Please Login'})
        username = username.decode('utf-8')

        user = Users.getUserByUsername(username)


        if check_password_hash(user.Password, password):

            audienceSessionID = hashlib.sha256(audience.encode()).hexdigest()
            if(redis_store.get_item(session_id) != None):
                sse.publish({"message": "Hello!"}, type='greeting')

            return jsonify({'Status': 'Success', 'session_id': session_id})

        return ({'Status': 'The Password Is Incorrect'})'''

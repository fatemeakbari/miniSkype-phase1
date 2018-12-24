from flask_restplus import Resource
from flask import request, make_response, jsonify, redirect, url_for
from flask_sse import sse
from werkzeug.security import check_password_hash
import hashlib
import string
from Models import *
from dashboard import api, redis_store

from API.dataModel import join_model
ns = api.namespace('/')


@ns.route('/join')
class Join(Resource):

    @api.expect(join_model)
    def post(self):
        """
        login
        """
        print("this is login.py")
        data = request.json
        session_id = data['session_id']
        callerUsername = data['callerUsername']


        username = redis_store.get_item(session_id)

        if not username:
            return ({'Status' : 'Please Login'})


        #generate caller ssesion id
        callerUsername = str(callerUsername)
        callerSession_id = hashlib.sha256(callerUsername.encode()).hexdigest()
        #check caller is login and send chat request
        if(redis_store.get_item(callerSession_id) != None):
            sse.publish({"state":"accept","message" : " accept your invite"}, type=callerUsername)
            return "send your acception"

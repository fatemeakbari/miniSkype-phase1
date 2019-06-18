from flask_restplus import Resource
from flask import request, make_response, jsonify, redirect, url_for, render_template
from flask_sse import sse
from werkzeug.security import check_password_hash
import hashlib
import string
from Models import *
from dashboard import api, redis_store, chat_store

from API.dataModel import join_model
ns = api.namespace('/')


@ns.route('/join')
class Join(Resource):

    @api.expect(join_model)
    def post(self):
        """
        login
        """
        print("*************this is join.py*****************")
        data = request.json
        session_id = data['session_id']
        roomID = data['roomID']
        caller = data['caller']
        print(caller)
        username = redis_store.get_item(session_id)
        
        if not username:
            return ({'Status' : 'Please Login'})

    

        #generate caller ssesion id
        caller = str(caller)
        callerSession_id = hashlib.sha256(caller.encode()).hexdigest()
        print("sdfdf  ",caller+'callerEvent')
        #check caller is login and send chat request
        if(redis_store.get_item(callerSession_id) != None):
            
            
            sse.publish({"state":"accept","message" : " accept your invite"}, type=caller+'callerEvent')
            return render_template("join.html")

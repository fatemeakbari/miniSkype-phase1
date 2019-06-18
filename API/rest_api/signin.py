
from flask_restplus import Resource
from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from Models import *
from dashboard import api, redis_store
from API.dataModel import signin_model
import uuid


ns = api.namespace('/')

@ns.route('/signin')
class SignUp(Resource):

    @api.expect(signin_model)
    def post(self):

        """
        signup user
        """

        # get info from user
        data = request.json
        username = data['username']
        password = data['password']
        email = data['email']


        if not username or not password or not email  :
            return ({'Status': 'please fill all fields'})


        exist_user = Users.getUserByUsername(username)
        if exist_user:
            return ({'Status': 'username already exist'})

        exist_user = Users.getUserByEmail(email)
        if exist_user:
            return ({'Status': 'email already exist'})

        #save user in db
        password_hash = generate_password_hash(password, method='sha256')
        new_user = Users.insertUser(username, password_hash, email)

        #session
        if new_user:
            username_hash = hashlib.sha256(username.encode()).hexdigest()
            session_id = redis_store.set_item(key = username_hash, value = username)
            return (jsonify({ 'status': 200, 'message':'Success, welcome '+ username, "session_id": session_id}))
            

        else:
            return ({"status": 200, 'message': "Try again"})

from flask_restplus import Resource
from flask import request, make_response, jsonify, render_template

from werkzeug.security import check_password_hash
import hashlib

from Models import *
from dashboard import api, redis_store
from API.dataModel import login_model
ns = api.namespace('/')


@ns.route('/login')
class Login(Resource):

    @api.expect(login_model)
    def post(self):
        """
        login
        """
        print("this is login.py")
        data = request.json
        username = data['username']
        password = data['password']


        if not data or not username or not password:
            return ({'Status': 'Please Fill All Fields'})

        user = Users.getUserByUsername(username)

        if  user == None:
            return ({'Status': 'Please Signip'})

        if check_password_hash(user.Password, password):

            username_hash = hashlib.sha256(username.encode()).hexdigest()
            session_id = redis_store.set_item(key = username_hash, value = username)
            dat = jsonify({'status': 200, 'message': 'login is successfuly, welcome ', 'username' : username, 'session_id': session_id})
            print(22222)
            return dat

        return ({'status': 400, 'message': 'Try again'})

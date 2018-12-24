from flask_restplus import fields
from dashboard import api

signin_model = api.model('signin_model', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),

})


login_model = api.model('login_model', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),

})

invite_model = api.model('invite_model', {
    'session_id': fields.String(required=True),
    'audience': fields.String(required=True),

})
join_model = api.model('join_model', {
    'session_id': fields.String(required=True),
    'callerUsername': fields.String(required=True),
    #'roomID': fields.String(required=True),

})


createRoom_model = api.model('createRoom_model', {
    'session_id':fields.String(required = True),
    'calleeUsername': fields.String(required=True),

})

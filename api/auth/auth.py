from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, JWTManager
from models.user import SignUp

auth_namespace = Namespace(
    'auth', description='Authentication related operations')
signup_namespace = auth_namespace.model('signup', {
    'id': fields.Integer(readOnly=True, description='User identifier'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
    'mobile': fields.String(required=True, description='Mobile'),
    'country_code': fields.String(required=True, description='Country Code')
})
login_namespace = auth_namespace.model('login', {
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

jwt = JWTManager()


@auth_namespace.route('/signup')
class SignUpAuth(Resource):
    @auth_namespace.expect(signup_namespace)
    @auth_namespace.marshal_with(signup_namespace)
    def post(self):
        '''
            Sign Up auth for new users
        '''
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        mobile = data.get('mobile')
        country_code = data.get('country_code')
        user = SignUp(username=username, email=email, password=password,
                      mobile=mobile, country_code=country_code)
        user.save()

        return user, 201


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_namespace)
    def post(self):
        '''
            Login auth for existing users
        '''
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = SignUp.query.filter_by(email=email).first()
        if user and user.password == password:
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return {
                'message': 'Logged in as {}'.format(email),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'details': {
                    'username': user.username,
                    'email': user.email,
                }
            }
        else:
            return {'message': 'Bad email or password'}, 401


# create refresh token fore norebase users
@auth_namespace.route('/refresh/get_tokens')
class RefreshAuth(Resource):
    @jwt_required(refresh=True)
    def post(self):
        '''
            refresh token for norebase users
        '''
        username = get_jwt_identity()
        create_refresh_token = create_refresh_token(identity=username)
        return {
            'refresh-token': create_refresh_token,
            'detail': {
                'username': username
            }
        }, 200

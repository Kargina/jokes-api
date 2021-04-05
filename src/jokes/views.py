from jokes.db import create_user, check_password, joke_create_by_user, joke_get_all_by_user_id, \
    joke_get_by_id, JokeBadUserException, get_user_id_by_login, joke_update_by_id, remove_user_joke, JokeBadJokeException
from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
import requests
from werkzeug.exceptions import BadRequest, InternalServerError, Forbidden
from flask_jwt_extended import get_jwt_identity
from flask import request
from jokes.config import REQUESTS_TIMEOUT

# flask_restx doesn't support swagger 3.0 with bearerAuth :(
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    version='1.0.0', title='Joke API',
    description='A simple jokes API',
    authorizations=authorizations,
    security='apikey'
)

ns = api.namespace('api', description='API operations')

joke = api.model('Joke', {
    'text': fields.String(required=True, description='The joke text')
})

joke_with_id = api.model('JokeWithID', {
    'id': fields.Integer(required=True, description='The joke id'),
    'text': fields.String(required=True, description='The joke text')
})

user = api.model('User', {
    'login': fields.String(required=True, description='The user login'),
    'password': fields.String(required=True, description='The user password')
})

user_id = api.model('UserID', {
    'id': fields.String(required=True, description='The user id'),
})

response = api.model('Response', {
    'message': fields.String(description='The response details')
})

token = api.model('Token', {
    'token': fields.String(description='User token')
})


@ns.route('/user')
class User(Resource):
    @api.marshal_with(user_id, code=201, description="user created")
    @api.response(code=400, description='Error')
    @api.expect(user)
    @api.doc(security=[])
    def post(self):
        try:
            created_id = create_user(api.payload)
        except JokeBadUserException as e:
            raise BadRequest(e.msg)
        return {'id': created_id}, 201


@ns.route('/healthcheck')
class Healthcheck(Resource):
    @api.marshal_with(response, code=200, description="healthcheck")
    @api.doc(security=[])
    def get(self):
        return {'message': 'OK'}, 200


@ns.route('/auth')
@api.doc(security=[])
class Auth(Resource):
    @api.response(code=403, description='Bad credantionals')
    @api.marshal_with(token, code=200)
    @api.expect(user)
    def post(self):
        user_login = api.payload['login']
        print(request.remote_addr)
        password_correct = check_password(user_login,
                                          api.payload['password'])
        if password_correct:
            user_id = get_user_id_by_login(user_login)
            additional_claims = {"user_login": user_login}
            access_token = create_access_token(user_id, additional_claims=additional_claims)

            # access_token = create_access_token(identity=user_id)
            return {'token': access_token}, 200
        else:
            raise BadRequest('User does not exist or password incorrect')


@ns.route('/joke/<int:id>')
class Joke(Resource):

    @jwt_required()
    @api.marshal_list_with(joke_with_id, code=200)
    @api.response(code=400, description='Error')
    @api.response(code=401, description='UNAUTHORIZED')
    def get(self, id):
        user_id = get_jwt_identity()
        joke = joke_get_by_id(user_id=user_id, joke_id=id)
        if joke is None:
            raise BadRequest('User does not have such joke')
        return {'id': joke.id, 'text': joke.text}

    @jwt_required()
    @api.marshal_list_with(joke_with_id, code=200)
    @api.response(code=400, description='Error')
    @api.response(code=401, description='UNAUTHORIZED')
    @api.response(code=403, description='Joke not found or no permission')
    @api.expect(joke)
    def patch(self, id):
        joke_text = api.payload['text']
        user_id = get_jwt_identity()
        joke = joke_update_by_id(user_id=user_id, joke_id=id, joke_text=joke_text)
        if joke is None:
            raise Forbidden('User does not have joke with given id')
        return {'id': joke.id,
                'text': joke.text}, 200

    @jwt_required()
    @api.response(code=400, description='Error')
    @api.response(code=401, description='UNAUTHORIZED')
    @api.marshal_with(response, code=200)
    def delete(self, id):  # 7
        user_id = get_jwt_identity()
        try:
            remove_user_joke(user_id=user_id, joke_id=id)
        except JokeBadJokeException as e:
            raise BadRequest(e.msg)
        return {'message': 'Successfully deleted'}


@ns.route('/jokes')
class Jokes(Resource):
    @jwt_required()
    @api.marshal_list_with(joke_with_id, code=200)
    @api.response(code=400, description='Error')
    def get(self):
        user_id = get_jwt_identity()
        jokes = joke_get_all_by_user_id(user_id)
        return jokes

    @jwt_required()
    @api.marshal_with(joke_with_id, code=200)
    @api.response(code=400, description='Error')
    @api.expect(joke)
    def post(self):
        joke_text = api.payload['text']
        user_id = get_jwt_identity()
        joke_id = joke_create_by_user(user_id, joke_text)
        return {'id': joke_id, 'text': joke_text}, 200


@ns.route('/joke/random')
class RandomJoke(Resource):
    @jwt_required()
    @api.marshal_with(joke_with_id, code=200)
    @api.response(code=400, description='Error')
    def get(self):  # gat random joke and save to 'my' 3
        user_id = get_jwt_identity()
        try:
            joke = requests.get("https://geek-jokes.sameerkumar.website/api", timeout=REQUESTS_TIMEOUT)
        except requests.exceptions.RequestException as e:
            raise InternalServerError(f'external API error: {e}')
        joke_text = joke.text
        joke_id = joke_create_by_user(user_id, joke_text)
        return {'id': joke_id,
                'text': joke_text}, 200

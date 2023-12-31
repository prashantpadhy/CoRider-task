from flask import Flask
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://localhost:27017/flask')
db = client['userdb']
users_collection = db['users']


class UserResource(Resource):
    
    def get(self, user_id=None):
        if user_id:
            return self.get_user(user_id)
        else:
            return self.get_all_users()

    def get_user(self, user_id):
        user = users_collection.find_one({'id': user_id}, {'_id': 0})
        if user:
            return user
        else:
            return {'message': 'User not found'}, 404

    def get_all_users(self):
        users = list(users_collection.find({}, {'_id': 0}))
        return users

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = {
            'id': args['id'],
            'name': args['name'],
            'email': args['email'],
            'password': args['password']
        }
        result = users_collection.insert_one(user)
        return {'message': 'User created', 'id': str(result.inserted_id)}, 201

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        updated_user = {
            'name': args['name'],
            'email': args['email'],
            'password': args['password']
        }
        result = users_collection.update_one({'id': user_id}, {'$set': updated_user})
        if result.modified_count > 0:
            return {'message': 'User updated'}
        else:
            return {'message': 'User not found'}, 404

    def delete(self, user_id):
        result = users_collection.delete_one({'id': user_id})
        if result.deleted_count > 0:
            return {'message': 'User deleted'}
        else:
            return {'message': 'User not found'}, 404

class UserAgeResource(Resource):
    def get(self, user_id, age):
        # Implement the logic to handle the user_id and age
        # Return the response accordingly
        return {'message': f'User ID: {user_id}, Age: {age}'}


class WelcomeScreen(Resource):
    def get(self):
        return f"Welcome to the crud app"
    
api.add_resource(UserResource, '/users', '/users/<string:user_id>')
api.add_resource(WelcomeScreen, '/')
api.add_resource(UserAgeResource, '/users/<string:user_id>/<int:age>')

if __name__ == '__main__':
    app.run(debug=True)

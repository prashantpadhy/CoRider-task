from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/flask')
db = client['userdb']
users_collection = db['users']


@app.route('/',methods =['GET'])
def welcome():
    return "<h1>Welcome to the crud application</h1>"

@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))
    return jsonify(users)
    
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = users_collection.find_one({'id': id}, {'_id': 0})
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = {
        'id': data['id'],
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    result = users_collection.insert_one(user)
    return jsonify({'message': 'User created', 'id': str(result.inserted_id)}), 201


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    updated_user = {
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    result = users_collection.update_one({'id': id}, {'$set': updated_user})
    if result.modified_count > 0:
        return jsonify({'message': 'User updated'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = users_collection.delete_one({'id': id})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted'})
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)

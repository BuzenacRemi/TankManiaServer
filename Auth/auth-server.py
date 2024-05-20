import bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://api:Passw0rd@postgres:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
salt = bcrypt.gensalt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_pass = db.Column(db.String(120), nullable=False)
    uuid = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password, uuid):
        self.username = username
        self.hashed_pass = password
        self.uuid = uuid


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'password': user.hashed_pass,
            'uuid': user.uuid,
        }
        result.append(user_data)
    return jsonify(result)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'password': user.hashed_pass,
            'uuid': user.uuid,
        }
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_pass = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
    new_user = User(username=data['username'], password=hashed_pass.decode('utf8'), uuid=uuid.uuid4())
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Username already exists'}), 400


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.username = data['username']
        user.hashed_pass = data['password']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


'''@app.route('/users/auth', methods=['POST'])
def get_user_uuid():
    hashed_password = User.query.filter_by(username=request.get_json()['username']).first().hashed_pass
    data = request.get_json()
    if bcrypt.checkpw(data['password'].encode('utf-8'), hashed_password.encode('utf-8')):
        print("UUID : ", User.query.filter_by(username=data['username']).first().uuid)
        return jsonify({'uuid': User.query.filter_by(username=data['username']).first().uuid})

    else:
        return jsonify({'message': 'Invalid credentials'}), 401

'''

@app.route('/users/auth', methods=['POST'])
def test_random_uuid():
    return jsonify({'uuid': uuid.uuid4()})


@app.route('/users/uuid/<uuid>', methods=['GET'])
def get_user_by_uuid(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'password': user.hashed_pass,
            'uuid': user.uuid,
        }
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404

app.run(debug=False, host='0.0.0.0', port=5000)

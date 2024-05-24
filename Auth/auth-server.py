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

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid_player = db.Column(db.String(120), db.ForeignKey('user.uuid'), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __init__(self, uuid_player, value):
        self.uuid_player = uuid_player
        self.value = value

class GameHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid_player1 = db.Column(db.String(120), db.ForeignKey('user.uuid'), nullable=False)
    uuid_player2 = db.Column(db.String(120), db.ForeignKey('user.uuid'), nullable=False)
    uuid_winner = db.Column(db.String(120), db.ForeignKey('user.uuid'))

    def __init__(self, uuid_player1, uuid_player2, uuid_winner):
        self.uuid_player1 = uuid_player1
        self.uuid_player2 = uuid_player2
        self.uuid_winner = uuid_winner

class GameStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('game_history.id'), nullable=False)
    id_player = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    success_missiles = db.Column(db.Integer, nullable=False)
    missiles_launched = db.Column(db.Integer, nullable=False)
    damages_received = db.Column(db.Integer, nullable=False)
    movement_distance = db.Column(db.Integer, nullable=False)

    def __init__(self, id_game, id_player, success_missiles, missiles_launched, damages_received, movement_distance):
        self.id_game = id_game
        self.id_player = id_player
        self.success_missiles = success_missiles
        self.missiles_launched = missiles_launched
        self.damages_received = damages_received
        self.movement_distance = movement_distance

# Routes for User
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{'id': user.id, 'username': user.username, 'uuid': user.uuid} for user in users]
    return jsonify(result)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'uuid': user.uuid})
    return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_pass = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
    new_user = User(username=data['username'], password=hashed_pass.decode('utf8'), uuid=str(uuid.uuid4()))
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
        if 'password' in data:
            user.hashed_pass = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt()).decode('utf8')
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/users/auth', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.hashed_pass.encode('utf-8')):
        return jsonify({'uuid': user.uuid})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/users/uuid/<string:user_uuid>', methods=['GET'])
def get_user_by_uuid(user_uuid):
    user = User.query.filter_by(uuid=user_uuid).first()
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'uuid': user.uuid})
    return jsonify({'message': 'User not found'}), 404

# Routes for Rank
@app.route('/rank', methods=['POST'])
def create_rank():
    data = request.get_json()
    new_rank = Rank(uuid_player=data['uuid_player'], value=data['value'])
    db.session.add(new_rank)
    db.session.commit()
    return jsonify({'message': 'Rank created successfully'})

@app.route('/rank/<string:uuid>', methods=['GET'])
def get_rank(uuid):
    rank = Rank.query.filter_by(uuid_player=uuid).first()
    if rank:
        return jsonify({'id': rank.id, 'uuid_player': rank.uuid_player, 'value': rank.value})
    return jsonify({'message': 'Rank not found'}), 404

@app.route('/rank/<int:id>', methods=['PUT'])
def update_rank(id):
    data = request.get_json()
    rank = Rank.query.get(id)
    if rank:
        rank.uuid_player = data['uuid_player']
        rank.value = data['value']
        db.session.commit()
        return jsonify({'message': 'Rank updated successfully'})
    return jsonify({'message': 'Rank not found'}), 404

@app.route('/rank/<int:id>', methods=['DELETE'])
def delete_rank(id):
    rank = Rank.query.get(id)
    if rank:
        db.session.delete(rank)
        db.session.commit()
        return jsonify({'message': 'Rank deleted successfully'})
    return jsonify({'message': 'Rank not found'}), 404

# Routes for GameHistory
@app.route('/game_history', methods=['POST'])
def create_game_history():
    data = request.get_json()
    new_game_history = GameHistory(uuid_player1=data['uuid_player1'], uuid_player2=data['uuid_player2'], uuid_winner=data['uuid_winner'])
    db.session.add(new_game_history)
    db.session.commit()
    return jsonify({'message': 'Game history created successfully'})

@app.route('/game_history/<int:id>', methods=['GET'])
def get_game_history(id):
    game_history = GameHistory.query.get(id)
    if game_history:
        return jsonify({
            'id': game_history.id,
            'uuid_player1': game_history.uuid_player1,
            'uuid_player2': game_history.uuid_player2,
            'uuid_winner': game_history.uuid_winner
        })
    return jsonify({'message': 'Game history not found'}), 404

@app.route('/game_history/<int:id>', methods=['PUT'])
def update_game_history(id):
    data = request.get_json()
    game_history = GameHistory.query.get(id)
    if game_history:
        game_history.uuid_player1 = data['uuid_player1']
        game_history.uuid_player2 = data['uuid_player2']
        game_history.uuid_winner = data['uuid_winner']
        db.session.commit()
        return jsonify({'message': 'Game history updated successfully'})
    return jsonify({'message': 'Game history not found'}), 404

@app.route('/game_history/<int:id>', methods=['DELETE'])
def delete_game_history(id):
    game_history = GameHistory.query.get(id)
    if game_history:
        db.session.delete(game_history)
        db.session.commit()
        return jsonify({'message': 'Game history deleted successfully'})
    return jsonify({'message': 'Game history not found'}), 404

# Routes for GameStats
@app.route('/game_stats', methods=['POST'])
def create_game_stats():
    data = request.get_json()
    new_game_stats = GameStats(id_game=data['id_game'], id_player=data['id_player'], success_missiles=data['success_missiles'],
                               missiles_launched=data['missiles_launched'], damages_received=data['damages_received'],
                               movement_distance=data['movement_distance'])
    db.session.add(new_game_stats)
    db.session.commit()
    return jsonify({'message': 'Game stats created successfully'})

@app.route('/game_stats/<int:id>', methods=['GET'])
def get_game_stats(id):
    game_stats = GameStats.query.get(id)
    if game_stats:
        return jsonify({
            'id': game_stats.id,
            'id_game': game_stats.id_game,
            'id_player': game_stats.id_player,
            'success_missiles': game_stats.success_missiles,
            'missiles_launched': game_stats.missiles_launched,
            'damages_received': game_stats.damages_received,
            'movement_distance': game_stats.movement_distance
        })
    return jsonify({'message': 'Game stats not found'}), 404

@app.route('/game_stats/<int:id>', methods=['PUT'])
def update_game_stats(id):
    data = request.get_json()
    game_stats = GameStats.query.get(id)
    if game_stats:
        game_stats.id_game = data['id_game']
        game_stats.id_player = data['id_player']
        game_stats.success_missiles = data['success_missiles']
        game_stats.missiles_launched = data['missiles_launched']
        game_stats.damages_received = data['damages_received']
        game_stats.movement_distance = data['movement_distance']
        db.session.commit()
        return jsonify({'message': 'Game stats updated successfully'})
    return jsonify({'message': 'Game stats not found'}), 404

@app.route('/game_stats/<int:id>', methods=['DELETE'])
def delete_game_stats(id):
    game_stats = GameStats.query.get(id)
    if game_stats:
        db.session.delete(game_stats)
        db.session.commit()
        return jsonify({'message': 'Game stats deleted successfully'})
    return jsonify({'message': 'Game stats not found'}), 404


app.run(debug=False, host='0.0.0.0', port=5000)

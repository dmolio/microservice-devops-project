from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_preferences.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False, unique=True)
    location = db.Column(db.String(120), nullable=False)
    temperature_unit = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'location': self.location,
            'temperature_unit': self.temperature_unit
        }

@app.route('/preferences', methods=['POST'])
def create_preference():
    data = request.json
    new_pref = UserPreference(
        user_id=data['user_id'],
        location=data['location'],
        temperature_unit=data['temperature_unit']
    )
    db.session.add(new_pref)
    db.session.commit()
    return jsonify(new_pref.to_dict()), 201

@app.route('/preferences/<user_id>', methods=['GET'])
def get_preference(user_id):
    pref = UserPreference.query.filter_by(user_id=user_id).first()
    if pref:
        return jsonify(pref.to_dict()), 200
    else:
        return jsonify({'message': 'User preference not found'}), 404

@app.route('/preferences/<user_id>', methods=['PUT'])
def update_preference(user_id):
    data = request.json
    pref = UserPreference.query.filter_by(user_id=user_id).first()
    if pref:
        pref.location = data['location']
        pref.temperature_unit = data['temperature_unit']
        db.session.commit()
        return jsonify(pref.to_dict()), 200
    else:
        return jsonify({'message': 'User preference not found'}), 404

@app.route('/preferences/<user_id>', methods=['DELETE'])
def delete_preference(user_id):
    pref = UserPreference.query.filter_by(user_id=user_id).first()
    if pref:
        db.session.delete(pref)
        db.session.commit()
        return jsonify({'message': 'User preference deleted'}), 200
    else:
        return jsonify({'message': 'User preference not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)


import json
import os
from flask import Flask, jsonify, request
from datetime import datetime
import uuid
from faker import Faker

app = Flask(__name__)
fake = Faker('ru_RU')

app_mode = os.getenv('APP_MODE', 'file').lower()
app.config['MODE'] = app_mode if app_mode in ['file', 'random'] else 'file'

users_data = []
if app.config['MODE'] == 'file':
    with open('users.json', 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    

def generate_random_user(user_id=None):
    if user_id is None:
        user_id = fake.uuid4()
    return {
        "id": user_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "registration_date": fake.date_between(start_date='-5y').isoformat(),
        "is_active": fake.boolean(chance_of_getting_true=75),
        "address": fake.address().replace('\n', ', '),
        "phone_number": fake.phone_number()
    }

@app.route('/users', methods=['GET'])
def get_users():
    if app.config['MODE'] == 'random':
        user_id = request.args.get("id")
        if user_id:
            return jsonify(generate_random_user(user_id))
        return jsonify([generate_random_user() for _ in range(100)])

    user_id = request.args.get("id")
    if user_id is None:
        return jsonify(users_data)
    for user in users_data:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    if app.config['MODE'] == 'random':
        new_user = generate_random_user()
        new_user["registration_date"] = datetime.now().isoformat()
        return jsonify(new_user), 201

    new_user = request.get_json()
    if not all(key in new_user for key in ['is_active', 'first_name', 'last_name', 'email', 'address', 'phone_number']):
        return jsonify({"error": "Bad request"}), 400
    user_id = str(uuid.uuid4())
    registration_date = datetime.now().isoformat()
    new_user["id"] = user_id
    new_user["registration_date"] = registration_date
    users_data.append(new_user)
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    return jsonify(new_user), 201

@app.route('/users', methods=['PUT'])
def update_user():
    if app.config['MODE'] == 'random':
        updated_data = request.get_json()
        if 'id' not in updated_data:
            return jsonify({"error": "User ID is required"}), 400
        updated_user = generate_random_user(updated_data['id'])
        return jsonify(updated_user), 200
    
    updated_user = request.get_json()
    if 'id' not in updated_user:
        return jsonify({"error": "User ID is required"}), 400
    found = False
    updated_user_obj = None
    for i, user in enumerate(users_data):
        if user['id'] == updated_user['id']:
            found = True
            registration_date = user['registration_date']
            for key in updated_user:
                if key not in ['id', 'registration_date']:
                    users_data[i][key] = updated_user[key]
            updated_user_obj = users_data[i]
            break
    if not found:
        return jsonify({"error": "User not found"}), 404
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    return jsonify(updated_user_obj), 200

@app.route('/users', methods=['DELETE'])
def delete_user():
    if app.config['MODE'] == 'random':
        return '', 204
    
    user_id = request.args.get("id")
    if user_id is None:
        return jsonify({"error":"User not found"}), 404
    user_to_delete = None 
    for user in users_data:
        if user["id"] == user_id:
            user_to_delete = user
            break
    if user_to_delete is None:
        return jsonify({"error": "User not found"}), 404
    users_data.remove(user_to_delete) 
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

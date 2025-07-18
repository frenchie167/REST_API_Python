
import json
from flask import Flask, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)

with open('users.json', 'r', encoding='utf-8') as f:
    users_data = json.load(f)


@app.route('/users', methods=['GET'])
def user_id():
    user_id = request.args.get("id")
    if user_id is None:
        return jsonify(users_data)
    for user in users_data:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
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
    app.run(debug=True)
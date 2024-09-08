from flask import Flask, request, jsonify
from mailersend import emails
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def load_users():
    with open('usuarios.json', 'r') as file:
        return json.load(file)

def load_users_telegram():
    with open('telegramIDs.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open('usuarios.json', 'w') as file:
        json.dump(users, file, indent=4)

def send_email(data):
    mail_body = {}

    mail_from = {
        "name": "Contacto Juan Carlos Giraldo",
        "email": "contacto@trial-z3m5jgrr3jmgdpyo.mlsender.net",
    }

    reply_to = {
        "name": "Name",
        "email": "reply@domain.com",
    }

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(data["recipients"], mail_body)
    mailer.set_subject(data["subject"], mail_body)
    mailer.set_html_content(data["content"], mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    return mailer.send(mail_body)

def send_message_telegram(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello World!'})

@app.route('/users', methods=['GET'])
def getUsers():
    users = load_users()
    return jsonify(users)

@app.route('/users/<int:userId>', methods=['GET'])
def getUser(userId):
    users = load_users()
    user = None
    i = 0
    found = False
    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
        i += 1
    if found:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def createUser():
    users = load_users()
    data = request.get_json()

    if len(users) > 0:
        i = 1
        last_user = users[0]

        while i < len(users):
            if users[i]['id'] > last_user['id']:
                last_user = users[i]
            i += 1

        new_id = last_user['id'] + 1
    else:
        new_id = 1

    new_user = {
        "id": new_id,
        "name": data['name'],
        "password": data['password'],
        "email": data['email'],
        "nickname": data['nickname']
    }

    users.append(new_user)
    save_users(users)
    return jsonify({"message": "User created successfully"}), 204
@app.route('/users/<int:userId>', methods=['PUT'])
def updateUser(userId):
    users = load_users()
    user = None
    i = 0

    found = False
    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
        i += 1

    if found:
        data = request.get_json()
        user['name'] = data['name']
        user['password'] = data['password']
        user['email'] = data['email']
        user['nickname'] = data['nickname']

        save_users(users)
        return jsonify({"message": "User updated successfully"})

    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    users = load_users()
    user = None
    i = 0

    found = False
    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
        i += 1

    if found:
        users.remove(user)
        save_users(users)
        return jsonify({"message": "User deleted successfully"})

    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/sendemail', methods=['POST'])
def sendemail():
    data = request.get_json()
    response = send_email(data)
    if int(response) == 202:
        return jsonify({"message": "Email sent successfully"})
    else:
        return jsonify({"error": "Error sending email"}), 500

@app.route('/sendmessage', methods=['POST'])
def sendmessage():
    data = request.get_json()
    response = send_message_telegram(data['chat_id'], data['text'])
    if response.status_code == 200:
        return jsonify({"message": "Message sent successfully"})
    else:
        return jsonify({"error": "Error sending message"}), 500

@app.route('/sendmessagemassive', methods=['POST'])
# Use telegramIDs.json to send messages to multiple users
def sendmessagemassive():
    data = request.get_json()
    users = load_users_telegram()
    for user in users:
        # Use "id" and "name" to send messages
        response = send_message_telegram(user['id'], f"Hola {user['name']}, {data['text']}")
        print("Message sent to", user['name'])
        if response.status_code != 200:
            return jsonify({"error": "Error sending messages"}), 500
    return jsonify({"message": "Messages sent successfully"})

if __name__ == '__main__':
    app.run(debug=True)
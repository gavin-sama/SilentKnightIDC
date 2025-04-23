from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import json
from cryptography.fernet import Fernet
import random

app = Flask(__name__)
app.secret_key = 'demokey'

FASTAPI_BASE_URL = "http://localhost:8000"

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            response = requests.get(f"{FASTAPI_BASE_URL}/users")
            if response.status_code == 200:
                users = response.json()
                for user in users:
                    if user['username'] == username and user['password'] == password:
                        session['username'] = username
                        print('Login successful')
                        return redirect(url_for('dashboard'))
                print('Invalid username or password')
            else:
                print('Error contacting user service')
        except Exception as e:
            print(f'API error: {str(e)}')

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        encryption = random.randint(1, 6)

        try:
            response = requests.post(f"{FASTAPI_BASE_URL}/users", json={
                "username": username,
                "password": password,
                "encryption": encryption
            })

            if response.status_code == 200:
                print('Registration successful. Please log in.')
                return redirect(url_for('login'))
            elif response.status_code == 400:
                print('Username already exists.')
            else:
                print('Error creating user.')
        except Exception as e:
            print(f'API error: {str(e)}')

        return redirect(url_for('register'))

    return render_template('register.html')

def encryption_selection(index:int):
    methods = {
        1:b'zVc8E3DjCtAoKYP6zTGNmPARxbTNmbwfW31tVosWy9E=',
        2:b'pfqKiXQMbowu3d64FZtZEOrbdIrGM3RsmJjRk4HW5Ps=',
        3:b'6sRtHQuy-yAufN1RSxbFTjsy_51UZ03C-hEh82wr-RE=',
        4:b'lJvrxODR4I31shhGrZQy-g1eDhYdLiXu5FG9YL7BJQs=',
        5:b'6TMfuujqXlaRK_acTzmyfZsNBtxIA0WZBt_cjmQv3-4=',
        6:b'87j-OoSkh_009MkuwkZpiuuq2ejU7DXbLS-1OqRS4EE='
    }

    return methods[int(index)]

def encrypt_message(encryption:int, message:str):
    cipher_suite = Fernet(encryption_selection(encryption))
    return cipher_suite.encrypt(message.encode()).decode()

def decrypt_message(encryption:int, message:str):
    cipher_suite = Fernet(encryption_selection(encryption))
    return cipher_suite.decrypt(message.encode()).decode()

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    messages = []

    try:
        results = requests.get(f"{FASTAPI_BASE_URL}/messages/{username}")
        messages = results.json()
        receiver_encryption = requests.get(f"{FASTAPI_BASE_URL}/encryption/{username}").text
        for message in messages:
            message["message"] = decrypt_message(int(receiver_encryption), message["message"])
    except Exception as e:
        print(f'API error: {str(e)}')
    
    return render_template('dashboard.html', username=username, messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    sender = session.get('username')
    receiver = request.form.get('receiver')
    message = request.form.get('message')

    receiver_encryption = requests.get(f"{FASTAPI_BASE_URL}/encryption/{receiver}").text

    message = encrypt_message(int(receiver_encryption), message)

    try:
        response = requests.post(f"{FASTAPI_BASE_URL}/send_message", json={
            "sender": sender,
            "receiver": receiver,
            "message": message
        })

        if response.status_code == 200:
            print('Message sent.')
            return redirect(url_for('dashboard'))
        elif response.status_code == 400:
            print('User not found.')
        else:
            print('Error sending message.')
    except Exception as e:
        print(f'API error: {str(e)}')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
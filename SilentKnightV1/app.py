from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import json

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

        try:
            response = requests.post(f"{FASTAPI_BASE_URL}/users", json={
                "username": username,
                "password": password
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

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    messages = []

    try:
        results = requests.get(f"{FASTAPI_BASE_URL}/messages/{username}")
        messages = results.json()
    except Exception as e:
        print(f'API error: {str(e)}')
    
    return render_template('dashboard.html', username=username, messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    sender = session.get('username')
    receiver = request.form.get('receiver')
    message = request.form.get('message')

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
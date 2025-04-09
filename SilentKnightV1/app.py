from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import json

app = Flask(__name__)
app.secret_key = 'demokey'

FASTAPI_BASE_URL = "http://localhost:8000/"

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
                        flash('Login successful')
                        return redirect(url_for('dashboard'))
                flash('Invalid username or password')
            else:
                flash('Error contacting user service')
        except Exception as e:
            flash(f'API error: {str(e)}')

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
                "password": password,
                "messages": "[]"
            })

            if response.status_code == 200:
                flash('Registration successful. Please log in.')
                return redirect(url_for('login'))
            elif response.status_code == 400:
                flash('Username already exists.')
            else:
                flash('Error creating user.')
        except Exception as e:
            flash(f'API error: {str(e)}')

        return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    messages = []

    try:
        unformatted_messages = requests.get(f"FASTAPI_BASE_URL/messages/{username}").text
        messages = json.loads(unformatted_messages)
    except Exception as e:
        flash(f'API error: {str(e)}')

    return render_template('dashboard.html', username=username, messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    receiver = request.form['receiver']
    message = request.form['message']

    try:
        response = requests.post(f"FASTAPI_BASE_URL/send_message", json={
            "receiver": receiver,
            "message": message
        })

        if response.status_code == 200:
            flash('Message sent.')
            return redirect(url_for('login'))
        elif response.status_code == 400:
            flash('User not found.')
        else:
                flash('Error sending message.')
    except Exception as e:
        flash(f'API error: {str(e)}')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
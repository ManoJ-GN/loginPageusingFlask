from flask import Flask, json, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_users():
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    return users

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

def validate_user(user_id, password):
    users = load_users()
    return user_id in users and users[user_id] == password

def user_exists(user_id):
    users = load_users()
    return user_id in users



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        if validate_user(user_id, password):
            return f"Welcome, {user_id}!"
        else:
            flash('Invalid user ID or password. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        if user_exists(user_id):
            flash('User ID already exists. Please choose a different one.')
            return redirect(url_for('register'))
        else:
            users = load_users()
            users[user_id] = password
            save_users(users)
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

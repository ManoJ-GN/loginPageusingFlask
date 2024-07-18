from flask import Flask, json, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_users():
    with open('users.json', 'r') as file:
        users = json.load(file)
    return users

def validate_user(user_id, password):
    users = load_users()
    if user_id in users and users[user_id] == password:
        return True
    return False

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

if __name__ == '__main__':
    app.run(debug=True)

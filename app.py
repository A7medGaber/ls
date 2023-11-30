# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Change this to a secure secret key
db.init_app(app)

# Create the database tables before the first request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username is already taken
        if User.query.filter_by(username=username).first():
            return render_template('register.html', message='Username already taken, choose another.')

        # Create a new user and add it to the database
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists and the password is correct
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username  # Store the username in the session
            return redirect(url_for('profile'))

        return render_template('login.html', message='Invalid username or password.')

    return render_template('login.html')

@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        return render_template('profile.html', user=user)

    # Redirect to login if not logged in
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear the session and redirect to the home page
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

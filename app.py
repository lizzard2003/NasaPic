import os
from flask import Flask, redirect, render_template, request, session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime
from dotenv import load_dotenv
import requests



load_dotenv()

app = Flask(__name__)

# Manually set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey2023'

# Initialize the Flask-SQLAlchemy extension
db = SQLAlchemy(app)

# this is going to be our table in the database
class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False)
    password= db.Column(db.String(80), nullable=False)

users={}

@app.route('/') # this gets user to the main page to sign up or login 
def landing():
    return render_template('landing.html', error ="")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        username= request.form.get('username') # this asks users for info 
        password = request.form.get('password')
        if username in users:
            error= "Pick another name as user name"
            return render_template('signup.html')
        users[username]=password

        session['username']= username
        return redirect('/picturepage')
    else:
        return render_template('signup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users or users[username] != password:
            error = "Sorry, Incorrect username or password."
            return render_template('login.html', error=error)
        session['username'] = username
        return redirect('/picturepage')
    else:
        return render_template('login.html')
@app.route('/picturepage')
def home():
    # Get the current date
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Fetch the NASA picture of the day
    api_key =os.getenv("NASA_API_KEY")
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date_today}"
    response = requests.get(url)
    data = response.json()
    
    # Render the template with the picture data
    return render_template('index.html', picture=data, current_date=date_today)

if __name__ == '__main__':
    app.run(debug=True)


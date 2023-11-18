import os
from flask import Flask, redirect, render_template, request, session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from dotenv import load_dotenv
import requests



load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey2023'

# Initialize the Flask-SQLAlchemy extension
db = SQLAlchemy(app)
migrate= Migrate(app, db)

# this is going to be our table in the database
class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False)
    password= db.Column(db.String(80), nullable=False)

users={}

@app.route('/') # this gets user to the main page to sign up or login 
def landing():
    error= None
    return render_template('landing.html', error ="")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error= None
    if request.method =='POST':
        username= request.form.get('username') # this asks users for info 
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            error= "Pick another name as user name"
            return render_template('signup.html', error= error)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()


        session['username']= username
        return redirect('/picturepage')
    else:
        return render_template('signup.html', error= error)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error= None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()


        if user:
            session['username'] = username
            
            return redirect('/picturepage')
        else:
            error = "Sorry, incorrect username or password."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html', error=error)
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


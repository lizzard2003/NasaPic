import os
from flask import Flask, render_template, request
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Manually set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey2023'

# Initialize the Flask-SQLAlchemy extension
db = SQLAlchemy(app)

# ... continue with your code

# this is going to be our table in the database
class User(db.Model,UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False)
    password= db.Column(db.String(80), nullable=False)


@app.route('/', methods=['GET', 'POST']) # this gets user to the main page to sign up or login 
def landing():
    if request.method =='POST':
        username= request.form.get('username') # this asks users for info 
        password = request.form.get('password')

        #validate_errors = validate_registration(username, password)
        #if validate_errors:
            #error = ",".join(validate_errors)
            #return render_template('signup.html', error=error)

        #else:
            #return render_template('landing.html')
    return render_template('landing.html', error ="")

@app.route('/signup')
def signup():
    return render_template('signup.html')
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


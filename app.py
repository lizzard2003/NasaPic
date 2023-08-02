import os
from flask import Flask, render_template, request, url_for
import requests


import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
def validate_registration(username,password):
    errors=[]
    if not username:
        errors.append("Username is required.")
    if not password:
        errors.append("Password is requred")
    return errors
@app.route('/', methods=['GET', 'POST']) # this gets user to the main page to sign up or login 
def landing():
    if request.method =='POST':
        username= request.form.get('username') # this asks users for info 
        password = request.form.get('password')

        validate_errors = validate_registration(username, password)
        if validate_errors:
            error = ",".join(validate_errors)
            return render_template('signup.html', error=error)

        else:
            return render_template('landing.html')
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


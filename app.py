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


@app.route('/')
def home():
    # Get the current date
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Fetch the NASA picture of the day
    api_key = os.getenv("NASA_API_KEY")

    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date_today}"
    response = requests.get(url)
    data = response.json()
    
    # Render the template with the picture data
    return render_template('index.html', picture=data, current_date=date_today)

if __name__ == '__main__':
    app.run(debug=True)


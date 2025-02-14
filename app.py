

from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify


from database import db, init_app
from models import Book, Member, Transaction

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
init_app(app)

@app.route("/")
def index():
    return "Home Page"

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def home():
    return render_template('homepage.html')


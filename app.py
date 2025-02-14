
from flask import render_template, request, redirect
from flask import Flask, jsonify
from models import db, Book, Member, Transaction, initialize_db

app = Flask(__name__)
initialize_db()

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def home():
    return render_template('homepage.html')


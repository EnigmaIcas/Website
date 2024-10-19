from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)

# Home Page Route
@app.route('/')
def home():
    return render_template('home.html')

# Register Page Route
@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=False)

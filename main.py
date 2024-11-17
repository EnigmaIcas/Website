from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'enigma.db')

# Database initialization function
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Create users table if it doesn't exist
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS Divisions (
        DivisionID INTEGER PRIMARY KEY AUTOINCREMENT,
        DivisionName TEXT NOT NULL,
        Building TEXT NOT NULL,
        Room TEXT NOT NULL
    );


    CREATE TABLE IF NOT EXISTS Universities (
  UniversityID INTEGER PRIMARY KEY AUTOINCREMENT,
  UniversityName VARCHAR(100),
  Country VARCHAR(100),
  City VARCHAR(100),
  NoOfStudents INTEGER
);

  
''')
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    show_login = request.args.get('show_login', False)
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        cur = db.cursor()
        
        # Check if email already exists
        cur.execute('SELECT email FROM users WHERE email = ?', (email,))
        user = cur.fetchone()
        
        if user:
            flash('Email already exists', 'error')
            return render_template('register.html', show_login=False)
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert new user
        try:
            cur.execute('''
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (?, ?, ?, ?)
            ''', (first_name, last_name, email, hashed_password))
            
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return render_template('register.html', show_login=True)
            
        except Exception as e:
            flash('An error occurred during registration', 'error')
            return render_template('register.html', show_login=False)
        
        finally:
            db.close()
            
    return render_template('register.html', show_login=show_login)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        cur = db.cursor()
        
        cur.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cur.fetchone()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['first_name'] = user['first_name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

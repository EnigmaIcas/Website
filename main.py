# Flask stuff
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Standard library
from pathlib import Path
import sqlite3

# Enviroment stuff
from dotenv import load_dotenv
from os import getenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY', 'your_secret_key_here')

# Database path
# FIXME: os.path is outdated, use pathlib.Path instead.
# os.path.join(os.path.dirname(__file__), 'enigma.db')
DB_PATH = Path(__file__).parent / "enigma.db" 

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
                              
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    branch TEXT NOT NULL,
    cgpa REAL,
    batch TEXT
);  

CREATE TABLE IF NOT EXISTS CountryDetails (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT NOT NULL UNIQUE,
    country_coordinates TEXT NOT NULL
);     
                      
CREATE TABLE IF NOT EXISTS CityDetails (
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    city_coordinates TEXT NOT NULL,
    country_id INTEGER NOT NULL,
    FOREIGN KEY (country_id) REFERENCES CountryDetails(country_id)
);
                          
   CREATE TABLE IF NOT EXISTS Universities (
    UniversityID INTEGER PRIMARY KEY AUTOINCREMENT,
    UniversityName VARCHAR(100),
    country_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,
    FOREIGN KEY (country_id) REFERENCES CountryDetails(country_id),
    FOREIGN KEY (city_id) REFERENCES CityDetails(city_id)
    );
                      

CREATE TABLE IF NOT EXISTS Batches (
    batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Student_University (
    student_id INTEGER,
    university_id INTEGER,
    batch_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (university_id) REFERENCES Universities(university_id),
    FOREIGN KEY (batch_id) REFERENCES Batches(batch_id),
    PRIMARY KEY (student_id, university_id, batch_id)
);   

CREATE TABLE IF NOT EXISTS Events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL
);
    
                 
    ''')
    
    conn.commit()
    conn.close()

"""
Code to insert data into enigma.db

INSERT INTO Events (event_id, name, image) VALUES
(1, 'Reverb', 'rb1.jpg'),
(2, 'Reverb', 'rb2.jpg'),
(3, 'Sports Day', 'sd1.jpg'),
(4, 'Sports Day', 'sd2.jpg');

INSERT INTO Universities (UniversityName, Country, City, country_coordinates, city_coordinates) VALUES
('University at Illinois at Urbana Champaign', 'USA', 'Urbana-Champaign', '37.0902,-95.7129', '40.1106,-88.2073'),
('Iowa State University', 'USA', 'Ames', '37.0902,-95.7129', '42.0308,-93.6319'),
('University of Queensland', 'Australia', 'Brisbane', '-25.2744,133.7751', '-27.4989,153.0138'),
('Andrews University', 'USA', 'Berrien Springs', '37.0902,-95.7129', '41.9570,-86.3561'),
('Carleton University', 'Canada', 'Ottawa', '56.1304,-106.3468', '45.3850,-75.6944'),
('University of Technology', 'Australia', 'Sydney', '-25.2744,133.7751', '-33.8833,151.2000'),
('University of British Columbia', 'Canada', 'Vancouver', '56.1304,-106.3468', '49.2606,-123.2460'),
('York University', 'Canada', 'Toronto', '56.1304,-106.3468', '43.7735,-79.5019'),
('University of Alberta', 'Canada', 'Edmonton', '56.1304,-106.3468', '53.5232,-113.5263'),
('Deakin University', 'Australia', 'Melbourne', '-25.2744,133.7751', '-37.8443,144.9681'),
('Manipal University Jaipur', 'India', 'Jaipur', '20.5937,78.9629', '26.8439,75.5647'),
('University of New South Wales', 'Australia', 'Sydney', '-25.2744,133.7751', '-33.9173,151.2313'),
('Australian National University', 'Australia', 'Canberra', '-25.2744,133.7751', '-35.2809,149.1300'),
('Western University', 'Canada', 'London', '56.1304,-106.3468', '43.0096,-81.2737'),
('The University of Sheffield', 'UK', 'Sheffield', '55.3781,-3.4360', '53.3811,-1.4701'),
('Radboud University', 'Netherlands', 'Nijmegen', '52.1326,5.8372', '51.8126,5.8372');

INSERT INTO Batches (batch_name) VALUES
('2018-20'),
('2020-22');

INSERT INTO Student_University (student_id, university_id, batch_id) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 5, 1),
(6, 6, 1),
(7, 7, 1),
(8, 3, 1),
(9, 3, 1),
(10, 8, 1),
(11, 9, 1),
(12, 3, 1),
(13, 10, 1),
(14, 11, 1),
(15, 11, 1),
(16, 8, 1),
(17, 3, 1),
(18, 6, 1),
(19, 7, 1),
(20, 11, 1),
(21, 3, 1),
(22, 7, 1),
(23, 12, 1),
(24, 9, 1),
(25, 3, 1),
(26, 7, 1),
(27, 9, 1),
(28, 9, 1),
(29, 13, 1),
(30, 7, 1),
(31, 3, 1),
(32, 14, 1),
(33, 11, 1),
(34, 7, 1),
(35, 12, 1),
(36, 15, 1),
(37, 12, 1),
(38, 16, 1),
(39, 11, 1),
(40, 11, 1);

INSERT INTO Students (name, branch, cgpa, batch) VALUES
('ROHEN AGARWAL', 'AVIATION', 3.70, '2018-20'),
('REDIJ MRINAL MANOJ', 'AVIATION', 3.51, '2018-20'),
('HARIHARAN V', 'AVIATION', 2.84, '2018-20'),
('RAHULKUMAR PATEL', 'AVIATION', 2.91, '2018-20'),
('VASANTHA KUMAR D', 'AVIATION', 3.13, '2018-20'),
('PRAGUN KALRA', 'CSE', 2.58, '2018-20'),
('TANMAY BUNDIWAL', 'CSE', 3.85, '2018-20'),
('PRITESH PADMANABHAN', 'CSE', 3.33, '2018-20'),
('PRANAV DHOOLIA', 'CSE', 3.39, '2018-20'),
('MUKUL CHAUHAN', 'CSE', 3.38, '2018-20'),
('SHUBHAM BAJORIA', 'CSE', 3.63, '2018-20'),
('REVANTH KUMAR PERLA', 'CSE', 3.60, '2018-20'),
('JAISHARAN S', 'CSE', 3.39, '2018-20'),
('MEDHA BADDAM', 'CSE', 3.25, '2018-20'),
('NEERAV CHAUDHARY', 'CSE', 2.78, '2018-20'),
('SIDDHANTH BAKSHI', 'CSE', 3.44, '2018-20'),
('ROHITH KOTIA PALAKIRTI', 'CSE', 3.32, '2018-20'),
('ACHINTYAA SREENATH', 'CSE', 3.74, '2018-20'),
('LAKSHYA AGARWAL', 'CSE', 3.92, '2018-20'),
('PRANOY SARKAR', 'CSE', 3.57, '2018-20'),
('RUCHIR MALIK', 'CSE', 3.90, '2018-20'),
('AVIJIT PRASAD', 'CSE', 3.69, '2018-20'),
('AKSHAT GULATI', 'CSE', 3.33, '2018-20'),
('VISHAL GUPTA', 'CSE', 3.23, '2018-20'),
('TUSHAR BHARDWAJ', 'CSE', 3.67, '2018-20'),
('RAGHAV CHANDAK', 'CSE', 3.88, '2018-20'),
('JANHAVI DESHMUKH', 'CSE', 3.77, '2018-20'),
('CHENNUGARI SAI SUDHIKSHA REDDY', 'CSE', 3.60, '2018-20'),
('BANSWADA SHIVANI REDDY', 'CSE', 3.93, '2018-20'),
('AKSHAY VARMA', 'CSE', 3.79, '2018-20'),
('ANURAJ KUMAR SINGH', 'CSE', 2.70, '2018-20'),
('IREENA BARO', 'CSE', 3.84, '2018-20'),
('RAYMON SAVION DSOUZA', 'Chem', 3.22, '2018-20'),
('GOKUL KRISHNA V', 'Chem', 3.00, '2018-20'),
('MUIRURI KERE G.', 'Chem', 2.73, '2018-20'),
('DHARAV CHITANIA', 'Chem', 2.56, '2018-20'),
('TANYA GUPTA', 'CSE', 3.58, '2018-20');     

INSERT INTO CountryDetails (country_name, country_coordinates) VALUES
('USA', '37.0902,-95.7129'),
('Australia', '-25.2744,133.7751'),
('Canada', '56.1304,-106.3468'),
('India', '20.5937,78.9629'),
('UK', '55.3781,-3.4360'),
('Netherlands', '52.1326,5.8372');
                      
INSERT INTO CityDetails (city_name, city_coordinates, country_id) VALUES
('Urbana-Champaign', '40.1106,-88.2073', (SELECT country_id FROM CountryDetails WHERE country_name = 'USA')),
('Ames', '42.0308,-93.6319', (SELECT country_id FROM CountryDetails WHERE country_name = 'USA')),
('Brisbane', '-27.4989,153.0138', (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia')),
('Berrien Springs', '41.9570,-86.3561', (SELECT country_id FROM CountryDetails WHERE country_name = 'USA')),
('Ottawa', '45.3850,-75.6944', (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada')),
('Sydney', '-33.8833,151.2000', (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia')),
('Vancouver', '49.2606,-123.2460', (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada')),
('Toronto', '43.7735,-79.5019', (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada')),
('Edmonton', '53.5232,-113.5263', (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada')),
('Melbourne', '-37.8443,144.9681', (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia')),
('Jaipur', '26.8439,75.5647', (SELECT country_id FROM CountryDetails WHERE country_name = 'India')),
('Sydney', '-33.9173,151.2313', (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia')),
('Canberra', '-35.2809,149.1300', (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia')),
('London', '43.0096,-81.2737', (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada')),
('Sheffield', '53.3811,-1.4701', (SELECT country_id FROM CountryDetails WHERE country_name = 'UK')),
('Nijmegen', '51.8126,5.8372', (SELECT country_id FROM CountryDetails WHERE country_name = 'Netherlands'));

INSERT INTO Universities (UniversityName, country_id, city_id) VALUES
('University at Illinois at Urbana Champaign', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'USA'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Urbana-Champaign')),
('Iowa State University', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'USA'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Ames')),
('University of Queensland', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Brisbane')),
('Andrews University', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'USA'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Berrien Springs')),
('Carleton University', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Ottawa')),
('University of Technology', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Sydney')),
('University of British Columbia', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Vancouver')),
('York University', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Toronto')),
('University of Alberta', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Edmonton')),
('Deakin University', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Melbourne')),
('Manipal University Jaipur', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'India'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Jaipur')),
('University of New South Wales', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Sydney')),
('Australian National University', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Australia'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Canberra')),
('Western University', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Canada'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'London')),
('The University of Sheffield', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'UK'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Sheffield')),
('Radboud University', 
    (SELECT country_id FROM CountryDetails WHERE country_name = 'Netherlands'), 
    (SELECT city_id FROM CityDetails WHERE city_name = 'Nijmegen'));

"""

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name    
    return conn

def get_division_names_from_db() -> list[str]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('SELECT DivisionName FROM Divisions;')
    query_result = cur.fetchall()
    return [
        record[0] 
        for record
        in query_result
    ]

def get_universities_from_db() -> list[str]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('SELECT DISTINCT Country FROM Universities;')
    query_result = cur.fetchall()
    return [
        record[0]
        for record
        in query_result
    ]

def get_events():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name, image FROM Events")
    events = cur.fetchall()
    print("Events from DB:", events)
    conn.close()
    return events


@app.route('/')
def home():
    return render_template(
        'home.html', 
        division_names=get_division_names_from_db()
    )

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
            cur.execute(
                '''
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (?, ?, ?, ?)
                ''', 
                (first_name, last_name, email, hashed_password)
            )
            
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

@app.route('/update', methods=['POST'])
def update_function():
    data = request.json
    selected_country = data.get('country', '')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print(selected_country)

    cur.execute('SELECT COUNT(su.student_id) FROM Universities uni INNER JOIN CountryDetails c on c.country_id = uni.country_id INNER JOIN Student_University su on su.university_id = uni.UniversityID WHERE c.country_name = ? ;', (selected_country,))
    total = cur.fetchone()[0]

    print(total)

    cur.execute('Select DISTINCT s.branch, COUNT(s.name) FROM Universities uni INNER JOIN Student_University su ON uni.UniversityID = su.university_id  INNER JOIN Students s on s.student_id = su.student_id INNER JOIN CountryDetails c on c.country_id = uni.country_id  WHERE c.country_name = ? GROUP BY s.branch ;', (selected_country,))
    branches = cur.fetchall()
    branches_name = [ record[0] for record in branches ]
    branches_count = [ record[1] for record in branches ]

    print(branches)
    
    cur.execute('SELECT uni.UniversityName, COUNT(uni.UniversityID) FROM Universities uni INNER JOIN Student_University su ON uni.UniversityID = su.university_id INNER JOIN CountryDetails c on c.country_id = uni.country_id  WHERE c.country_name = ? GROUP BY uni.UniversityName;', (selected_country,))
    universities = cur.fetchall()
    university_name = [ record[0] for record in universities ]
    university_count =  [record[1] for record in universities]

    print(universities)

    cur.execute('SELECT batch.batch_name, COUNT(su.student_id) FROM Batches batch INNER JOIN Student_University su on su.batch_id = batch.batch_id INNER JOIN Universities uni on su.university_id = uni.UniversityID INNER JOIN CountryDetails c on c.country_id = uni.country_id  WHERE c.country_name = ? GROUP BY batch.batch_name', (selected_country,))
    batches = cur.fetchall()
    batch_count = [record[1] for record in batches]
    batches = [record[0] for record in batches]

    cur.execute('SELECT country_coordinates FROM CountryDetails WHERE country_name = ? ;', (selected_country,))
    country_coordinates = cur.fetchone()[0]
    country_coordinates = [country_coordinates.split(",")[0], country_coordinates.split(",")[1]]

    cur.execute('SELECT city_name, city_coordinates FROM CityDetails city INNER JOIN CountryDetails country on country.country_id = city.country_id where country.country_name = ? ;', (selected_country,))
    city = cur.fetchall()   
    city_coordinates = {
    record[0]: [float(record[1].split(",")[0]), float(record[1].split(",")[1])] 
    for record in city
    }

    cur.execute('SELECT city.city_name, COUNT(su.student_id) FROM Student_University su INNER JOIN Universities uni on uni.UniversityID = su.university_id INNER JOIN CityDetails city on uni.city_id = city.city_id INNER JOIN CountryDetails country on country.country_id = uni.country_id WHERE country.country_name = ? GROUP BY city.city_name', (selected_country,))
    city_data = cur.fetchall()
    city_names = [record[0] for record in city_data]
    city_count = [record[1] for record in city_data]

    cur.execute('SELECT students.name, uni.UniversityName, students.cgpa FROM Universities uni INNER JOIN CountryDetails c on c.country_id = uni.country_id INNER JOIN Student_University su on su.university_id = uni.UniversityID INNER JOIN Students students on students.student_id = su.student_id WHERE c.country_name = ? ;', (selected_country,))
    student_data = cur.fetchall()
    student_names = [record[0] for record in student_data]
    university_names = [record[1] for record in student_data]
    cgpa = [record[2] for record in student_data]

    conn.close()

    return jsonify({"total": total, "branches": branches_name, "branches_count" : branches_count, "university_name": university_name, "university_count": university_count, "batches_name" : batches, "batches_count" : batch_count, "country_coordinates": country_coordinates, "city_coordinates": city_coordinates, "city_name": city_names, "city_count" : city_count, "student_names": student_names, "university_names": university_names, "cgpa": cgpa})

countries = []

@app.route('/universities')
def universities():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('SELECT DISTINCT country_name FROM CountryDetails;')
    query_result = cur.fetchall()
    cur.execute('SELECT COUNT(c.country_name) FROM Universities uni INNER JOIN CountryDetails c on c.country_id = uni.country_id WHERE c.country_name = ? ;', ('USA',))
    total = cur.fetchall()[0][0]
    countries = [ record[0] for record in query_result ]
    

    return render_template('university.html', countries=countries, total=total)

@app.route('/events')
def events():
    event_data = get_events()
    return render_template('events.html', events=event_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

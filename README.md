ENIGMA WEBSITE INSTALLATION GUIDE
================================

Prerequisites:
-------------
1. Python 3.x
2. *SQLite3*

Installation Steps:
------------------
1. Make sure you are in Correct directory:
   >cd Website-main   <br />
   >Eg  It should look like this: C:\path\to\Website-main>

2. Install required packages:
   > pip install flask python-dotenv werkzeug

3. Install an extension in your IDE to view the sql database<br>
   Eg: SQLite Viewer

Directory Structure:
------------------
![image](https://github.com/user-attachments/assets/e75050a1-2fc4-4c83-8871-3d9bd044076f)


Configuration:
-------------
1. Dont change .env Secret Key

2. Verify all static files are in the correct locations:
   - Images (.png, .jpg) → static/images/
   - Videos (.mp4) → static/videos/
   - CSS files → static/css/

Running the Application:
----------------------
1. Ensure you are in the correct directory: C:\path\to\Website-main>
2. Run: python main.py
3. Open browser: http://localhost:5000

Features:
---------
- User Registration
- Authentication
- Responsive Design
- Video Background
- Social Login UI
- SQLite Database

Troubleshooting:
---------------
1. Static files not loading:
   - Check file permissions
   - Verify file paths (case-sensitive)
   - Clear browser cache

2. Database errors:
   - Delete enigma.db and restart
   - Check file permissions

3. Application won't start:
   - Verify package installation
   - Check port 5000 availability
   - Ensure virtual environment is active

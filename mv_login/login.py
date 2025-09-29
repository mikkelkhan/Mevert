from flask import Flask, request, render_template, Blueprint, session
import pyodbc
from configparser import ConfigParser
import random
from string import Template
import base64

mv_login = Blueprint("login", __name__)

# Load configuration
config = ConfigParser()
config.read("config.ini")

# Connection string
cnxn = pyodbc.connect(config["MSSQL"]["connect"])

@mv_login.route('/api/user_fetch', methods=["POST"])
def fetch_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('login.html', show="Please enter both username and password")

    try:
        with cnxn.cursor() as cursor:
            # Secure parameterized query
            cursor.execute(
                Template(config["Query"]["fetch_username"]).safe_substitute(username=username, password=password))
            user_exists = cursor.fetchone()

            if not user_exists:
                return render_template('login.html', show="Username or password is wrong")

            # Fetch user data
            cursor.execute(Template(config["Query"]["fetch_user_data"]).safe_substitute(username=username))
            all_data = cursor.fetchall()

        if not all_data:
            return render_template('login.html', show="No user data found")

        # Convert to dictionary list
        data = [
            {
                'name': row[0],
                'city': row[1],
                'country': row[2],
                'age': row[3],
                'about': row[4],
                'profilePicture': row[5]
            }
            for row in all_data
        ]

        # Pick a random profile for display
        selected = random.choice(data)
        fetch_pro = None
        if selected.get('profilePicture'):
            fetch_pro = base64.b64encode(selected['profilePicture']).decode('utf-8')

        # Save session
        session['username'] = username

        return render_template(
            'profile.html',
            name=selected['name'],
            city=selected['city'],
            country=selected['country'],
            age=selected['age'],
            user=username,
            about=selected['about'],
            profilePicture=fetch_pro
        )

    except Exception as e:
        # Log error in production instead of returning
        return render_template('login.html', show="An error occurred, please try again later")


from flask import Flask, request, render_template, Blueprint
import pyodbc
from configparser import ConfigParser
from string import Template
import psycopg2
import os
from dotenv import load_dotenv
mv_signup = Blueprint("signup", __name__)


config = ConfigParser()
config.read("config.ini")

load_dotenv()

Database_connect = os.getenv("Database_connect")
cnxn = psycopg2.connect(Database_connect)
cursor = cnxn.cursor()

@mv_signup.route('/api/signupdata', methods=["POST"])
def signup_data():
    if request.method == 'POST':
        # Collect form data
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        age = request.form.get('age')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        pin = request.form.get('pin')


        if password != confirm_password:
            return render_template('signup.html', red="Passwords do not match")


        cursor.execute("SELECT COUNT(*) FROM signup WHERE username = %s", (username,))
        user_exists = cursor.fetchone()[0]

        if user_exists:
            return render_template('signup.html', red="Username already taken")

        cursor.execute(Template(config["Query"]["add_data"]).safe_substitute(name=name, username=username, email=email,
                                                                  password=password, age=age, city=city, state=state,
                                                                  country=country, pin=pin))
        cnxn.commit()

        return render_template('signup.html', red="Account created successfully")


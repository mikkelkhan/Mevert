from flask import Flask, request, render_template,Blueprint
import pyodbc
from configparser import ConfigParser
from string import Template
import random



mv_login = Blueprint("login",__name__)

config = ConfigParser()
config.read("config.ini")

cnxn = pyodbc.connect(config["MSSQL"]["connect"])
cursor = cnxn.cursor()

@mv_login.route('/api/user_fetch',methods=["POST"])
def fetch_user():
    username = request.form.get('username')
    password = request.form.get('password')
    email_con = cursor.execute(Template(config["Query"]["fetch_username"]).safe_substitute(username=username,password=password))
    email_fetch = cursor.fetchval()



    if email_fetch == username and password:
        fetch_data = cursor.execute(Template(config["Query"]["fetch_user_data"]).safe_substitute(username=username))
        all_data = cursor.fetchall()
        data = []
        for row in all_data:
            data.append({'name': row[0], 'city': row[1], 'country': row[2], 'age': row[3]})
        # fetch_name = data.get('name')
        random_folter = random.choice(data)
        fetch_name = random_folter.get('name')
        fetch_city = random_folter.get('city')
        fetch_country = random_folter.get('country')
        fetch_age = random_folter.get('age')
        return render_template('profile.html', name=fetch_name, city=fetch_city, country=fetch_country,age=fetch_age,user=username)



    else:
        return render_template('login.html',show="username or password is wrong")

















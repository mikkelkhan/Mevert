from flask import Flask, request, render_template,Blueprint
import pyodbc
from configparser import ConfigParser
from string import Template
from mv_signup.signup import mv_signup

mv_login = Blueprint("login",__name__)

config = ConfigParser()
config.read("config.ini")

cnxn = pyodbc.connect(config["MSSQL"]["connect"])
cursor = cnxn.cursor()

@mv_login.route('/api/email_fetch',methods=["POST"])
def fetch_user():
    email = request.form.get('email')
    password = request.form.get('password')
    email_con = cursor.execute(Template(config["Query"]["fetch_email"]).safe_substitute(email=email,password=password))
    email_fetch = cursor.fetchval()

    if email_fetch == email and password:
        return render_template('filter.html')

    else:
        return render_template('login.html',show="email or password is wrong")

















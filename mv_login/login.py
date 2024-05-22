from flask import Flask, request, render_template,Blueprint
import pyodbc
from configparser import ConfigParser
from string import Template



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
        return render_template('filter.html',user=username)

    else:
        return render_template('login.html',show="username or password is wrong")

















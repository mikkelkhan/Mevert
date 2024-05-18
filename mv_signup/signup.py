from flask import Flask, request, render_template,Blueprint
import pyodbc
from configparser import ConfigParser
from string import Template

mv_signup = Blueprint("signup",__name__)



config = ConfigParser()
config.read("config.ini")

cnxn = pyodbc.connect(config["MSSQL"]["connect"])
cursor = cnxn.cursor()

@mv_signup.route('/api/signupdata',methods=["POST"])
def signup_data():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        pin = request.form.get('pin')
        if password == confirm_password:
            add_data = cursor.execute(Template(config["Query"]["add_data"]).safe_substitute(name=name, username=username, email=email, password=password, city=city, state=state, country=country, pin=pin))
            cnxn.commit()
            return render_template('signup.html',red="account is created")
        else:
            return render_template('signup.html',red="password is wrong")


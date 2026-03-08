from flask import Flask, request, render_template,Blueprint
import pyodbc
from configparser import ConfigParser
from string import Template
from flask import session
import psycopg2
import os
from dotenv import load_dotenv

mv_edit_profile = Blueprint("edit_profile",__name__)
config = ConfigParser()
config.read("config.ini")
load_dotenv()

Database_connect = os.getenv("Database_connect")
cnxn = psycopg2.connect(Database_connect)
cursor = cnxn.cursor()


@mv_edit_profile.route('/api/edit_profile_about',methods=["POST"])
def edit_profile_about():
    username = session.get('username')
    about = request.form.get('about')
    fetch_data = cursor.execute(Template(config["Query"]["update_about_me_data"]).safe_substitute(username=username,about=about))
    cnxn.commit()
    return render_template('edit_profile_about.html', red="about me  is now updated")

@mv_edit_profile.route('/api/edit_profile_age',methods=["POST"])
def edit_profile_age():
    username = session.get('username')
    age = request.form.get('age')
    fetch_data = cursor.execute(Template(config["Query"]["update_age_data"]).safe_substitute(username=username,age=age))
    cnxn.commit()
    return render_template('edit_profile_about.html', red="age  is now updated")

@mv_edit_profile.route('/api/edit_profile_city',methods=["POST"])
def edit_profile_city():
    username = session.get('username')
    city = request.form.get('city')
    fetch_data = cursor.execute(Template(config["Query"]["update_age_city"]).safe_substitute(username=username,city=city))
    cnxn.commit()
    return render_template('edit_profile_about.html', red="city  is now updated")


@mv_edit_profile.route('/api/edit_profile_country',methods=["POST"])
def edit_profile_country():
    username = session.get('username')
    country = request.form.get('country')
    fetch_data = cursor.execute(Template(config["Query"]["update_age_country"]).safe_substitute(username=username,country=country))
    cnxn.commit()
    return render_template('edit_profile_about.html', red="country  is now updated")
from flask import Flask, request, render_template,Blueprint
import pyodbc
from configparser import ConfigParser
from string import Template
from mv_login.login import fetch_user



mv_events = Blueprint("event",__name__)
config = ConfigParser()
config.read("config.ini")

cnxn = pyodbc.connect(config["MSSQL"]["connect"])
cursor = cnxn.cursor()


@mv_events.route('/api/event',methods=["POST"])
def add_event():
    if request.method == 'POST':
        username = fetch_user.username
        artist_name = request.form.get('artist_name')
        date = request.form.get('date')
        location = request.form.get('location')
        city = request.form.get('city')
        country = request.form.get('country')
        add_data = cursor.execute(Template(config["Query"]["add_event"]).safe_substitute(username=username, artist_name=artist_name, date=date, location=location, city=city, country=country))
        cnxn.commit()
        return render_template('events.html',show="event is created")



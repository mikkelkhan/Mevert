from flask import Flask, request, render_template,Blueprint,jsonify,url_for
import pyodbc
from configparser import ConfigParser
from string import Template
from flask import session


mv_profile_matches = Blueprint("matches",__name__)
config = ConfigParser()
config.read("config.ini")
cnxn = pyodbc.connect(config["MSSQL"]["connect"])



@mv_profile_matches.route('/api/matches', methods=["GET"])
def fetch_matches():
    username = session.get('username')
    if not username:
        return {"error": "Unauthorized"}, 401



    cursor = cnxn.cursor()
    try:
        query = Template(config["Query"]["matches_data"]).safe_substitute(username=username)
        fetch_data = cursor.execute(query)
        all_data = cursor.fetchall()

        data = [
            {
                "profile_url": url_for('profile.other_profile', other_username=row[0]),
                "name": row[1],
                "age": row[2]
            }
            for row in all_data
        ]
        return jsonify(data)
    finally:
        cursor.close()

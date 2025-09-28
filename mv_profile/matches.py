from flask import Flask, request, render_template,Blueprint,jsonify,url_for
from werkzeug.utils import secure_filename
import pyodbc
from configparser import ConfigParser
from string import Template
from flask import session
import random
import base64

mv_profile_matches = Blueprint("matches",__name__)
config = ConfigParser()
config.read("config.ini")

cnxn = pyodbc.connect(config["MSSQL"]["connect"])
cursor = cnxn.cursor()


@mv_profile_matches.route('/api/matches', methods=["GET"])
def fetch_matches():
    username = session.get('username')
    if not username:
        return {"error": "Unauthorized"}, 401

    query = Template(config["Query"]["matches_data"]).safe_substitute(username=username)
    fetch_data = cursor.execute(query)
    all_data = cursor.fetchall()

    if not all_data:
        return {"error": "No matches found"}, 404

    data = []
    for row in all_data:
        data.append({
            "profile_url": url_for('profile.other_profile', other_username=row[0]),
            "name": row[1],
            "age": row[2]

        })

    return jsonify(data)








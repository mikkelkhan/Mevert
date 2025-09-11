from flask import Flask, request, render_template,Blueprint
from werkzeug.utils import secure_filename
import pyodbc
from configparser import ConfigParser
from string import Template
from flask import session
import random
import base64

mv_profile_main = Blueprint("profile",__name__)
config = ConfigParser()
config.read("config.ini")

cnxn = pyodbc.connect(config["MSSQL"]["connect"])
cursor = cnxn.cursor()


@mv_profile_main.route('/api/profile',methods=["POST"])
def fetch_profile():
    username = session.get('username')
    #username = "mikkellord"
    fetch_data = cursor.execute(Template(config["Query"]["fetch_user_data"]).safe_substitute(username=username))
    all_data = cursor.fetchall()
    data = []
    for row in all_data:
        data.append({'name': row[0], 'city': row[1], 'country': row[2], 'age': row[3],'about': row[4],'profilePicture': row[5]})
    #fetch_name = data.get('name')
    random_folter = random.choice(data)
    fetch_name = random_folter.get('name')
    fetch_city = random_folter.get('city')
    fetch_country = random_folter.get('country')
    fetch_age = random_folter.get('age')
    fetch_about = random_folter.get('about')
    fetch_image = random_folter.get('profilePicture')
    fetch_pro = base64.b64encode(fetch_image).decode('utf-8')
    return render_template('profile.html',name=fetch_name,city=fetch_city,country=fetch_country,age=fetch_age,user=username,about=fetch_about,profilePicture=fetch_pro)



@mv_profile_main.route('/api/profile/uploadPic',methods=["POST"])
def upload_pic():
    username = session.get('username')
    profilePicture = request.files['profilePicture']
    #profilePicture = "C:\Users\kashi\OneDrive\Pictures\Camera Roll"
    if not profilePicture:
        return render_template('upload_pic.html', red="No Picture is there")
    image_data = profilePicture.read()
    filename = secure_filename(profilePicture.filename)
    mimetype = profilePicture.mimetype
    add_pic = cursor.execute(config["Query"]["upload_pic"],(username, image_data))
    cnxn.commit()
    return render_template('upload_pic.html', red="Picture is uploaded now")





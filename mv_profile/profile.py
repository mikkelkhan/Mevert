from flask import Flask, request, render_template,Blueprint
from werkzeug.utils import secure_filename
import cloudinary.uploader
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


@mv_profile_main.route('/api/profile',methods=['GET', 'POST'])
def fetch_profile():
    username = session.get('username')
    if not username:
        return {"error": "Unauthorized"}, 401
    #username = "mikkellord"
    fetch_data = cursor.execute(Template(config["Query"]["fetch_user_data"]).safe_substitute(username=username))
    all_data = cursor.fetchall()
    if not all_data:
        return {"error": "User not found"}, 404
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
    if fetch_image:
        fetch_pro = fetch_image
    else:
        fetch_pro = None
    return render_template('profile.html',name=fetch_name,city=fetch_city,country=fetch_country,age=fetch_age,user=username,about=fetch_about,profilePicture=fetch_pro)




@mv_profile_main.route('/api/profile/uploadPic',methods=["POST"])
def upload_pic():
    username = session.get('username')

    if not username:
        return render_template('upload_pic.html', red="Not logged in")

    profilePicture = request.files.get('profilePicture')

    if not profilePicture:
        return render_template('upload_pic.html', red="No picture uploaded")

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(profilePicture)

    image_url = upload_result["secure_url"]

    # Store only image URL in DB
    cursor.execute(
        config["Query"]["upload_pic"],
        (username, image_url)
    )
    cnxn.commit()

    return render_template('upload_pic.html', red="Picture uploaded successfully")

@mv_profile_main.route('/profile/<string:other_username>', methods=["GET"])
def other_profile(other_username):
    fetch_data = cursor.execute(
        Template(config["Query"]["fetch_user_data"]).safe_substitute(username=other_username)
    )
    user_data = cursor.fetchone()
    if not user_data:
        return "User not found", 404

    fetch_name, fetch_city, fetch_country, fetch_age, fetch_about, fetch_image = user_data
    fetch_pro = fetch_image if fetch_image else None

    return render_template(
        'Profile_other.html',
        name=fetch_name,
        city=fetch_city,
        country=fetch_country,
        age=fetch_age,
        user=other_username,
        about=fetch_about,
        profilePicture=fetch_pro
    )



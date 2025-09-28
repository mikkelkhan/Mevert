import random
from flask import Flask, request, render_template,Blueprint,jsonify
import pyodbc
from configparser import ConfigParser
from string import Template
from flask import session
import base64




mv_filters = Blueprint("filter",__name__)
config = ConfigParser()
config.read("config.ini")

cnxn = pyodbc.connect(config["MSSQL"]["connect"])
cursor = cnxn.cursor()




@mv_filters.route('/api/filter',methods=["POST"])
def fetch_filter():
    if request.method == 'POST':
        city = request.form.get('city')
        country = request.form.get('country')
        button1 = {

            'city': city,
            'country': country,
            'api_url': '/api/filter'
        }
        filter_data = cursor.execute(Template(config["Query"]["fetch_all_filter"]).safe_substitute(city=city, country=country))
        filter_all= filter_data.fetchall()
        if filter_all == []:
            return render_template('filter.html',not_show="No one is going this city events")
        else:
            data = []
            for row in filter_all:
                data.append({'username': row[0], 'name': row[1], 'city': row[2], 'Country': row[3], 'new_city': row[5],
                             'new_Country': row[6], 'location': row[7], 'profilePicture': row[8]})

            random_folter = random.choice(data)
            filter_name = random_folter.get('name')
            filter_city = random_folter.get('city')
            filter_Country = random_folter.get('Country')
            filter_new_city = random_folter.get('new_city')
            filter_new_Country = random_folter.get('new_Country')
            filter_location = random_folter.get('location')
            receiver_username = random_folter.get('username')
            fetch_image = random_folter.get('profilePicture')
            if fetch_image:
                fetch_pro = base64.b64encode(fetch_image).decode('utf-8')
            else:
                fetch_pro = None
            return render_template('home.html', filter_name=filter_name, filter_city=filter_city,
                                   filter_Country=filter_Country, filter_new_city=filter_new_city,
                                   filter_new_Country=filter_new_Country, filter_location=filter_location,
                                   button1=button1,receiver_username=receiver_username,profilePicture=fetch_pro)





@mv_filters.route('/api/send_button_user_details',methods=["POST"])
def send_button_user_details():
    username = session.get('username')
    receiver = request.form.get('username')
    messaage = f"Hey {receiver} ,what’s up?"
    status = "2"
    send_request = cursor.execute(
        "INSERT INTO Matches (username, receiver, messaage, status) VALUES (?, ?, ?, ?)",
        (username, receiver, messaage, status)
    )
    cnxn.commit()
    return jsonify({"status": "success", "msg": f"✅ Request sent successfully to {receiver}"})











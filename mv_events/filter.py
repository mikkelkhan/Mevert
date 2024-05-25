import random
from flask import Flask, request, render_template,Blueprint
import pyodbc
from configparser import ConfigParser
from string import Template






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
        filter_data = cursor.execute(Template(config["Query"]["fetch_all_filter"]).safe_substitute(city=city, country=country))
        filter_all= filter_data.fetchall()

        data = []
        for row in filter_all:
            data.append({'username': row[0], 'name': row[1], 'city': row[2], 'Country': row[3],'new_city' : row[5],'new_Country' : row[6],'location' : row[7]})


        random_folter = random.choice(data)
        filter_name = random_folter.get('name')
        filter_city = random_folter.get('city')
        filter_Country = random_folter.get('Country')
        filter_new_city = random_folter.get('new_city')
        filter_new_Country = random_folter.get('new_Country')
        filter_location = random_folter.get('location')
        return render_template('home.html',filter_name=filter_name,filter_city=filter_city,filter_Country=filter_Country,filter_new_city=filter_new_city,filter_new_Country=filter_new_Country,filter_location=filter_location)



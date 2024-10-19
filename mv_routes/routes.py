from flask import Flask, request, render_template,Blueprint

app = Flask(__name__)

mv_routes = Blueprint("routes",__name__)

@mv_routes.route('/home')
def home():
    return render_template('home.html')

@mv_routes.route('/login')
def login():
    return render_template('login.html')

@mv_routes.route('/signup')
def signup():
    return render_template('signup.html')

@mv_routes.route('/filter')
def filter():
    return render_template('filter.html')

@mv_routes.route('/event')
def event():
    return render_template('events.html')

@mv_routes.route('/profile')
def profile():
    return render_template('profile.html')

@mv_routes.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')


@mv_routes.route('/request')
def request():
    return render_template('request.html')
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
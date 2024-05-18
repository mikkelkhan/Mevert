from flask import Flask, request, render_template,Blueprint

app = Flask(__name__)

front = Blueprint("routes",__name__)

@front.route('/home')
def home():
    return render_template('home.html')

@front.route('/login')
def login():
    return render_template('login.html')

@front.route('/signup')
def signup():
    return render_template('signup.html')
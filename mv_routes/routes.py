from flask import Flask, request, render_template,Blueprint

app = Flask(__name__)

mv_routes = Blueprint("routes",__name__)

@mv_routes.route('/home')
def home():
    return render_template('home.html')

@mv_routes.route('/')
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

@mv_routes.route('/edit_profile_about')
def edit_profile_about():
    return render_template('edit_profile_about.html')

@mv_routes.route('/edit_profile_age')
def edit_profile_age():
    return render_template('edit_profile_age.html')

@mv_routes.route('/edit_profile_city')
def edit_profile_city():
    return render_template('edit_profile_city.html')


@mv_routes.route('/edit_profile_country')
def edit_profile_country():
    return render_template('edit_profile_country.html')



@mv_routes.route('/request')
def request():
    return render_template('request.html')


@mv_routes.route('/upload_pic')
def upload_pic():
    return render_template('upload_pic.html')

@mv_routes.route('/other_profile')
def other_profile():
    return render_template('Profile_other.html')

@mv_routes.route('/chat')
def chat():
    return render_template('chat.html')

@mv_routes.route('/health')
def health():
    return {"status": "running"}
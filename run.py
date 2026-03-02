from flask import Flask, request, render_template
from db import close_db_connection
from flask_socketio import SocketIO
from mv_signup.signup import mv_signup
from mv_routes.routes import mv_routes
from mv_login.login import mv_login
from mv_events.event import mv_events
from mv_events.filter import mv_filters
from mv_profile.profile import mv_profile_main
from mv_profile.edit_profile import mv_edit_profile
from mv_profile.matches import mv_profile_matches
from mv_chats.chat import mv_chats
from extensions import socketio

import cloudinary
import os

app = Flask(__name__)

app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/'

cloudinary.config(
    cloud_name= "dhqgvahme",
    api_key="425469328355628",
    api_secret="y6lOC2NUYXjTkyEgnbtyJLH5VvU"
)


socketio.init_app(app)

app.register_blueprint(mv_signup)
app.register_blueprint(mv_routes)
app.register_blueprint(mv_login)
app.register_blueprint(mv_events)
app.register_blueprint(mv_filters)
app.register_blueprint(mv_profile_main)
app.register_blueprint(mv_edit_profile)
app.register_blueprint(mv_profile_matches)
app.register_blueprint(mv_chats)
app.teardown_appcontext(close_db_connection)





if __name__ == '__main__':
    socketio.run(app, debug=True)
    #app.run(debug=True)



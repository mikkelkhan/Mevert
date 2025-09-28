from flask import Flask, request, render_template
from db import close_db_connection
from mv_signup.signup import mv_signup
from mv_routes.routes import mv_routes
from mv_login.login import mv_login
from mv_events.event import mv_events
from mv_events.filter import mv_filters
from mv_profile.profile import mv_profile_main
from mv_profile.edit_profile import mv_edit_profile
from mv_profile.matches import mv_profile_matches
app = Flask(__name__)

app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/'
app.register_blueprint(mv_signup)
app.register_blueprint(mv_routes)
app.register_blueprint(mv_login)
app.register_blueprint(mv_events)
app.register_blueprint(mv_filters)
app.register_blueprint(mv_profile_main)
app.register_blueprint(mv_edit_profile)
app.register_blueprint(mv_profile_matches)
app.teardown_appcontext(close_db_connection)





if __name__ == '__main__':


    app.run(debug=True)



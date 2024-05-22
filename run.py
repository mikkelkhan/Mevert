from flask import Flask, request, render_template
from mv_signup.signup import mv_signup
from mv_routes.routes import mv_routes
from mv_login.login import mv_login
from mv_events.event import mv_events
from mv_events.filter import mv_filters

app = Flask(__name__)
app.register_blueprint(mv_signup)
app.register_blueprint(mv_routes)
app.register_blueprint(mv_login)
app.register_blueprint(mv_events)
app.register_blueprint(mv_filters)





if __name__ == '__main__':


    app.run(debug=True)



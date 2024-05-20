from flask import Flask, request, render_template
from mv_signup.signup import mv_signup
from mv_routes.routes import mv_routes
from mv_login.login import mv_login

app = Flask(__name__)
app.register_blueprint(mv_signup)
app.register_blueprint(mv_routes)
app.register_blueprint(mv_login)




if __name__ == '__main__':


    app.run(debug=True)



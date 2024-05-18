from flask import Flask, request, render_template
from mv_signup.signup import mv_signup
from mv_front.routes  import front

app = Flask(__name__)
app.register_blueprint(mv_signup)
app.register_blueprint(front)




if __name__ == '__main__':

    app.run(debug=True)



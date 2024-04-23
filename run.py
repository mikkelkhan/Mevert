from flask import Flask, request, render_template
import pyodbc


app = Flask(__name__)

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=Kashif;DATABASE=Mevert')
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM signup")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)



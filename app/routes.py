from flask import render_template
from app import app
from app.forms import LoginForm

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", titöe="Sign In", form=form)

@app.route("/")
@app.route("/index")
def index():
    user = {'username': 'Test'}
    return render_template("index.html", title="Home", user=user)
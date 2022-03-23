import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import calendar
from help import login_required

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    message = 'Hello! Welcome to The Orchid Project'
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("login.html", message = 'Please enter username')
        elif not request.form.get("password"):
            return render_template("login.html", message = 'Please enter password')
        rows = db.execute("SELECT * FROM project WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", message = 'Please enter valid username/password')
        session["user_id"] = rows[0]["user_id"]
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    message = "welcome to The Orchid Project's website! To be part of the community please register."
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not request.form.get("username"):
            return render_template("register.html", message = "please enter a username")

        elif not password:
            return render_template("register.html", message = "please enter a password")

        elif not confirmation:
            return render_template("register.html", message = "please enter the password again")

        elif password != confirmation:
            return render_template("register.html", message = "your passwords do not match. Try again!")
        list_users = db.execute("SELECT * FROM project WHERE username = ?;", username)
        passwordhash = generate_password_hash(password)
        if len(list_users) == 0:
            db.execute("INSERT INTO project(username, hash) VALUES(?,?);", username, passwordhash)
            return redirect("/login")
        else:
            return render_template("login.html", message = "your username is already registered login or try with another username!")
    else:
        return render_template("register.html")


@app.route("/aboutUs", methods=["GET"])
def aboutus():
    return render_template("aboutus.html")


@app.route("/journal", methods=["GET", "POST"])
def journal():
    message = "We, the team are very proud for you took a big step today!"
    if request.method == "POST":
        answer1 = request.form.get("answer1")
        answer2 = request.form.get("answer2")
        answer3 = request.form.get("answer3")
        answer4 = request.form.get("answer4")
        answer5 = request.form.get("answer5")
        if not answer1:
            return render_template("journal.html", message = "Please answer all the questions to finish journalling for the day. If you do not wish to complete, please return to the homepage")
        if not answer2:
            return render_template("journal.html", message = "Please answer all the questions to finish journalling for the day. If you do not wish to complete, please return to the homepage")
        if not answer3:
            return render_template("journal.html", message = "Please answer all the questions to finish journalling for the day. If you do not wish to complete, please return to the homepage")
        if not answer4:
            return render_template("journal.html", message = "Please answer all the questions to finish journalling for the day. If you do not wish to complete, please return to the homepage")
        if not answer5:
            return render_template("journal.html", message = "Please answer all the questions to finish journalling for the day. If you do not wish to complete, please return to the homepage")
        date = datetime.datetime.now()
        day = date.strftime("%d")
        month = date.strftime("%B")
        year = date.strftime("%G")
        submitted = True
        user_id = session["user_id"]
        db.execute("INSERT INTO journal(user_id, date, day, month, year) VALUES(?, ?, ?, ?, ?)", user_id, date, day, month, year)
        return render_template("journalled.html")
    else:
        return render_template("journal.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/selfhelp", methods=["GET", "POST"])
def selfhelp():
    if request.method == "POST":
        db.execute("INSERT INTO feedback(user_id, feedback) VALUES(?,?);", session["user_id"], request.form.get("feedback"))
        return render_template("index.html")
    else:
        return render_template("guides.html")

@app.route("/form", methods=["GET", "POST"])
def findaplaylistform():
    message = "Hello, as you know, The Orchid Project aims to aid mental health by employing music. We have a playlist that will guarantee to improve your mood, to build that playlist, please answer the following questions!"
    
    if request.method == "POST":
        answer1 = request.form.get("answer1")
        answer2 = request.form.get("answer2")
        answer3 = request.form.get("answer3")
        answer4 = request.form.get("answer4")
        answer5 = request.form.get("answer5")
        answer6 = request.form.get("answer6")
        answer7 = request.form.get("answer7")
        answer8 = request.form.get("answer8")
        if not answer1:
            return render_template("form-playlist.html", message = "Please answer all the questions.")
        if not answer2:
            return render_template("form-playlist.html", message = "Please answer all the questions.")
        if not answer3:
            return render_template("form-playlist.html", message = "Please answer all the questions.")
        if not answer4:
            return render_template("form-playlist.html", message = "Please answer all the questions.")
        if not answer5:
            return render_template("form-playlist.html", message = "Please answer all the questions.")
        if not answer6:
            return render_template("form-playlist.html", message = "Please answer all the questions.")
        if not answer7:
            return render_template("form-playlist.html", message = "Please answer all the questions.")
        if not answer8:
            return render_template("form-playlist.html", message = "Please answer all the questions.")
        
        
        return render_template("form-playlist.html")
    else:
        return render_template("form-playlist.html")

@app.route("/result", methods=["GET", "POST"])
def findaplaylistresult():
    return render_template("result-playlist.html")

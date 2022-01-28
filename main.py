from flask import Flask, render_template, request
app = Flask('app')
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/njhs")
def njhs():
    return render_template("njhs.html")
@app.route("/hour-tracker")
def hour_tracker():
    return render_template("hourtracker.html")
@app.route("/njhs/hour-tracker")
def njhs_hour_tracker():
    return render_template("njhshourtracker.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/login", methods=["POST"])
def loginpost():
    user = request.get("e")
    password = request.get("p")
    from schoology import checkLogin
    response = checkLogin(user, password)
    try:
        if response[0] == "error":
            return "error!!!"
    except Exception as t:
        t = t

    return t["name_display"]
app.run(host='0.0.0.0', port=8080)
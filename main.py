from flask import Flask, render_template, request, session, redirect
app = Flask('app')
app.secret_key = '12345678987654321'

@app.route("/")
def home():
    try:
        user = session["name"]
    except:
        user = None

    return render_template("index.html", user=user)
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
    try:
        a = (session["name"]+session["email"])
    except:
        return render_template("login.html")

    return redirect("/")


@app.route("/login", methods=["POST"])
def loginpost():
    user = request.form["e"]
    password = request.form["p"]
    from schoology import checkLogin
    response = checkLogin(user, password)
    try:
        if response == "error":
            return "error!!!"
    except Exception as t:
        t = t
    session["email"] = user
    session["name"] = response
    return str(response)

app.run(host='0.0.0.0', port=8080)
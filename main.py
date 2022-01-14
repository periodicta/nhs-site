from flask import Flask, render_template
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
app.run(host='0.0.0.0', port=8080)
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

@app.route("/close")
def close():
    session['token'] = request.args.get("oauth_token")
    return "<script>window.close();</script>"
    
@app.route("/login")
def login():
    try:
        a = (session["name"]+session["email"])
    except:
        import schoolopy
        key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
        secret = "59ccaaeb93ba02570b1281e1b0a90e18"
        # Instantiate with 'three_legged' set to True for three_legged oauth.
        # Make sure to replace 'https://www.schoology.com' with your school's domain.
        # DOMAIN = 'https://www.schoology.com'
        DOMAIN = 'https://bins.schoology.com'

        auth = schoolopy.Auth(key, secret, three_legged=True, domain=DOMAIN)
        # Request authorization URL to open in another window.
        url = auth.request_authorization("https://NHS.nicholasxwang.repl.co/close")
        session["request_token"] = auth.request_token
        session["request_token_secret"] = auth.request_token_secret
        session["access_token_secret"] = auth.access_token_secret
        session["access_token"] = auth.access_token

        # Open OAuth authorization webpage. Give time to authorize.
        return render_template("login.html", url = url)

    return redirect("/")

@app.route("/logout")
def logout():
    session["name"] = None
    session["email"] = None
    session['token'] = None
    session["request_token"] = None
    session["request_token_secret"] = None
    session["access_token_secret"] = None
    session["access_token"] = None
    return redirect("/")
@app.route("/login", methods=["POST"])
def loginpost():
  import schoolopy, random, time
  key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
  secret = "59ccaaeb93ba02570b1281e1b0a90e18"
  sc = schoolopy.Schoology(schoolopy.Auth(key, secret))
  sc.limit = 10
  request_token = session["request_token"]
  request_token_secret = session["request_token_secret"]
  access_token_secret = session["access_token_secret"]
  access_token = session["access_token"]
  auth = schoolopy.Auth(key, secret, domain='https://bins.schoology.com', three_legged=True,
                 request_token=request_token, request_token_secret=request_token_secret, access_token=access_token, access_token_secret=access_token_secret)
  print(auth.authorized)
  print(auth.authorize())
  a = auth.authorized
  print(a)
  if (a == False):
    return "error!!!"
  sc = schoolopy.Schoology(auth)
  sc.limit = 10
  print(sc.get_me().name_display)
  session["name"] = sc.get_me().name_display
  session["email"] = sc.get_me().primary_email

  return str(sc.get_me().name_display)

app.run(host='0.0.0.0', port=8080)
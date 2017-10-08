import json
import os
import requests
from static.User import User
import datetime
import pytz
from flask import Flask, request, render_template, url_for, jsonify
from db import DB
from flask_oauthlib.client import OAuth, session, redirect
from werkzeug.exceptions import BadRequest
from werkzeug.wrappers import BaseResponse as Response

app = Flask(__name__, static_folder="static", static_url_path="/static",
            template_folder="templates")
database = DB(app.root_path)

app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_ID'),
    consumer_secret=os.environ.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/calendar.readonly email profile https://www.googleapis.com/auth/gmail.readonly'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

currentUser = User("", "", "")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True)
                            , prompt='consent')


@app.route('/logout')
def logout():
    if isLoggedIn():
        session.pop('google_token', None)
        return Response("User logged out", status=200)
    else:
        return Response("User is not logged in", status=403)


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    _me = google.get("https://www.googleapis.com/plus/v1/people/me").data
    currentUser.name = _me["displayName"]
    currentUser.email = _me["emails"][0]["value"]
    # Uncomment the line below for local testing
    # return webbrowser.open_new_tab(url_for('getProfile',currentUser.email))
    return redirect(url_for('enterRegistration'))


@app.route('/session/<sess>', methods=['POST', 'GET'])
def transfersession(sess):
    session['google_token'] = sess
    return redirect(url_for('index'))

@app.route('/currentUser', methods=['GET'])
def getcurrentUser():
    return jsonify({"name":currentUser.name, "email":currentUser.email})

@google.tokengetter
def get_google_oauth_token():
    if isLoggedIn():
        return session.get('google_token')


@app.route('/delete', methods=['GET'])
def deleteUser():
    if isLoggedIn():
        email = currentUser.email
        pin = request.args.get('pin')
        try:
            database.deleteUser(email, pin)
        except BadRequest:
            return jsonify({"error":"Either the user"
                                             " was not found or"
                                             " the pin was incorrect"})

        return Response("User deleted", status=202)
    else:
        return Response("NOT LOGGED IN", status=403)

#('/register/<user>',
# def enterRegistration(user)
@app.route('/register/', methods=['GET'])
def enterRegistration():
    if isLoggedIn():
        return render_template('Register.html')
    else:
        return render_template('index.html')


@app.route('/events', methods=['GET'])
def getEvents():
    if isLoggedIn():
        # get events from calendar for the next 3 days
        cest = pytz.timezone('America/New_York')
        now = datetime.datetime.now(tz=cest)  # timezone?
        timeMin = datetime.datetime(year=now.year, month=now.month, day=now.day, tzinfo=cest) + datetime.timedelta(
            days=1)
        timeMin = timeMin.isoformat()
        timeMax = datetime.datetime(year=now.year, month=now.month, day=now.day, tzinfo=cest) + datetime.timedelta(
            days=300)
        timeMax = timeMax.isoformat()
        events = google.get(
            'https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=' + timeMin + '&timeMax=' + timeMax).data
        return jsonify({"list": events["items"]})
    return Response(status=403)


@app.route('/register', methods=['POST'])
def getPreferences():
    content = request.get_json(force=True)
    try:
        database.addProfile(content)
    except BadRequest as e:
        return Response("Error: " + e.description, status=400)
    return Response("Added: " + content['name'] + " to the DB", status=202)


@app.route('/profile', methods=['GET'])
def getProfile():
    email = request.args.get('email') or currentUser.email
    if (database.isUserRegistered(email)):
        try:
            profileData = database.getUser(email)
            profileData = jsonify(profileData)
            return profileData
        except BadRequest:
            return Response("Not an email", status=403)
        return (jsonify(profileData))
    else:
        return Response("Profile not found", status=404)

@app.route('/weather', methods=['GET'])
def weather():
    send_url = 'http://freegeoip.net/json'
    LocationRequest = requests.get(send_url)
    LocationResponse = json.loads(LocationRequest.text)
    lat = LocationResponse['latitude']
    lon = LocationResponse['longitude']
    weather__key = os.environ.get('WEATHER_KEY')
    url = 'http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&units=imperial'+'&APPID='+str(weather__key)
    openWeatherRequest = requests.get(url)
    return jsonify(openWeatherRequest.json())

def isLoggedIn():
    if 'google_token' in session:
        return True
    return False

@app.route('/change',methods=['GET'])
def changepreferences():
    return render_template('change.html')

if __name__ == '__main__':
    app.run()

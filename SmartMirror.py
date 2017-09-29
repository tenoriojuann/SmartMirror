import os

import datetime
import pytz
from flask import Flask, request, render_template, url_for, jsonify
from db import DB
from flask_oauthlib.client import  OAuth, session, redirect
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
        'scope': 'https://www.googleapis.com/auth/calendar.readonly profile https://www.googleapis.com/auth/gmail.readonly'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@app.route('/')
def index():
    if isLoggedIn():
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True)
                            ,prompt='consent')


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
    me = google.get('userinfo')
    #return jsonify({"data": me.data})
    return render_template('index.html')

@google.tokengetter
def get_google_oauth_token():
    if isLoggedIn():
        return session.get('google_token')


@app.route('/delete', methods=['GET'])
def deleteUser():
    if isLoggedIn():
        email = request.args.get('email')
        pin = request.args.get('pin')
        if database.isUserRegistered(email):
            try:
                database.deleteUser(email, pin)
            except BadRequest:
                return Response("Wrong pin", status=403)

            return Response("User deleted", status=202)
        else:
            return Response("User is not in the database", status=404)
    else:
        return Response("NOT LOGGED IN", status=403)

@app.route('/register', methods=['GET'])
def enterRegistration():
    if isLoggedIn():
        print()
        return render_template('Register.html')
    else:
        return Response("User is not logged in", status=403)

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
            days=1000)
        timeMax = timeMax.isoformat()
        events = google.get('https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin='+timeMin+'&timeMax='+timeMax).data
        return jsonify({"list": events["items"]})
    return Response(status=403)


@app.route('/register', methods=['POST'])
def getPreferences():
    content = request.get_json(force=True)
    try:
        database.addProfile(content)
    except BadRequest as e:
        return Response("Error: "+e.description, status=400)
    return Response("Added: "+ content['name']+ " to the DB", status=202)

def isLoggedIn():
    if 'google_token' in session:
        return True
    return False

if __name__ == '__main__':
    app.run()

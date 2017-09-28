import os

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
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@app.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True)
                            ,prompt='consent')


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return Response("User logged out", status=200)


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
    return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/delete', methods=['GET'])
def deleteUser():
    if 'google_token' in session:
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
    return render_template('Register.html')

@app.route('/register', methods=['POST'])
def getPreferences():
    content = request.get_json(force=True)
    try:
        database.addProfile(content)
    except BadRequest as e:
        return Response("Error: "+e.description, status=400)
    return Response("Added: "+ content['name']+ " to the DB", status=202)

if __name__ == '__main__':
    app.run()

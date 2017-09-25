from flask import Flask, request, render_template
from db import DB
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.wrappers import BaseResponse as Response
app = Flask(__name__, static_folder="static", static_url_path="/static",
            template_folder="templates")
database = DB(app.root_path)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/delete', methods=['GET'])
def deleteUser():
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

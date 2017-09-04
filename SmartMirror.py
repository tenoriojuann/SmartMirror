from flask import Flask, request, jsonify
import db
app = Flask(__name__)
database = db.DB()


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


@app.route('/register', methods=['POST', 'GET'])
def getPreferences():
    if request.method == 'POST':
        content = request.get_json(force=True)
        print(content)

        database.addProfile(content['name'], content['email'], content['token'], content['preferences'])
        return "hi"
    else:
        return """<html><body>
        A record with that email has already been set up.
        </body></html>"""

if __name__ == '__main__':
    app.run()

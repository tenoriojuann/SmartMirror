from flask import Flask, request, jsonify
import db
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


@app.route('/register', methods=['GET'])
def register():
    return 'register'


@app.route('/register', methods=['POST'])
def getPreferences():
    if request.method == 'POST':
        content = request.get_json()
        db.DB.addToken(content['name'], content['email'], content['token'], content['preferences'])
    else:
        return """<html><body>
        Something went horribly wrong
        </body></html>"""

if __name__ == '__main__':
    app.run()

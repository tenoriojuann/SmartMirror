from flask import Flask, request, render_template
import db
from werkzeug.exceptions import BadRequest
app = Flask(__name__, static_folder="static", static_url_path="/static",
            template_folder="templates")
database = db.DB(app.root_path)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def enterRegistration():
    return render_template('Register.html')

@app.route('/register', methods=['POST'])
def getPreferences():
    content = request.get_json(force=True)
    try:
        database.addProfile(content)
    except BadRequest as e:
        return e
    return render_template('register.html')

if __name__ == '__main__':
    app.run()

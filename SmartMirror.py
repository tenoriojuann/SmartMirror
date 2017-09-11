from flask import Flask, request, render_template
import db
from werkzeug.exceptions import HTTPException, BadRequest
app = Flask(__name__, static_folder="static", static_url_path="/static",
            template_folder="templates")
database = db.DB(app.root_path)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def getPreferences():
    if request.method == 'POST':
        content = request.get_json(force=True)
        print(content)
        try:
            database.addProfile(content)
        except BadRequest as e:
            return e
        return render_template('register.html')
    else:
        return """<html><body>
        A record with that email has already been set up.
        </body></html>"""

if __name__ == '__main__':
    app.run()

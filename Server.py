from Main import *
import flask
from flask import request, jsonify

API_dictionary = getAPIdetails()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Recommendations for the API store</h1>
<p>A prototype API to show the recommended APIs for a given user.\n The recommended APIs are: </p>'''

@app.route('/recommendations/<user>', methods=['GET'])
def api_all(user):
    recommendation = getRecommendations(user,API_dictionary)
    return jsonify({'User': user,'User Recommendations': recommendation})
app.run()

from Recommendation import *
import flask
from flask import request, jsonify

API_dictionary = get_API_dictionaries()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Recommendations for the API store</h1>
<p>A prototype API to show the recommended APIs for a given user. </p>'''

@app.route('/recommendations/<user>', methods=['GET'])
def api_all(user):
    recommendation = get_recommendations(user,API_dictionary)
    return jsonify({'User': user,'User Recommendations': recommendation})
app.run()

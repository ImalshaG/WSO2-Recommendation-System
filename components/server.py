from db_modifier import * 
import flask
from flask import request, current_app
from flask import jsonify, Response
from flask import Flask, render_template
from flask_basicauth import BasicAuth
from werkzeug import serving
import ssl
import sys
import yaml
import atexit
from apscheduler.scheduler import Scheduler

API_CRT = "utils/Certificates/server.crt"
API_KEY = "utils/Certificates/server.key"
CONFIG_FILE = 'config/config.yaml'

HTTPS_ENABLED = True
VERIFY_USER = True

with open(CONFIG_FILE, 'r') as stream:
    config_properties = yaml.safe_load(stream)

API_HOST = config_properties['host']
API_PORT = config_properties['port']

RECOMMENDATION_COUNT = config_properties['recommendations_count']
SEARCH_DETAILS_VALID_TIME = config_properties['search_details_valid_months']
MINIMUM_SEARCH_QUERIES = config_properties['minimum_search_queries']

cron = Scheduler(daemon=True)
app = flask.Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = config_properties['username']
app.config['BASIC_AUTH_PASSWORD'] = config_properties['password']
basic_auth = BasicAuth(app)

@cron.interval_schedule(hours=24) 
def update_user_recommendations_db():
    """
    Processing recommendations periodically with a time interval of 24 hours and 
    storing them in a db so that these pre-processed recommendations can be retrieved whenever needed.
    """
    try:
        process_user_info(SEARCH_DETAILS_VALID_TIME, MINIMUM_SEARCH_QUERIES)
        logging.info("Processing periodic user recommendations")
    except Exception as e:
        logging.error(e)

@app.route('/recommendations', methods=['GET'])
@basic_auth.required
def recommend_apis():
    """
    Returns API recommendations for a given user in the requested tenant domain.
    """
    try:
        requested_tenant = request.headers['Account']
        user = request.headers['User']
        recommendations = get_user_recommendations(user, requested_tenant, RECOMMENDATION_COUNT)
        if recommendations:
            response = jsonify({'user': user, 'requestedTenantDomain': requested_tenant, 'userRecommendations': recommendations})
        else:
            response = jsonify({'user': user, 'requestedTenantDomain': requested_tenant, 'userRecommendations':[]})
    except Exception as e:
        logging.error(e)
        response = jsonify({'user': user, 'requestedTenantDomain': requested_tenant, 'userRecommendations':[]})
    return response

@app.route('/addapi', methods=['POST']) 
@basic_auth.required
def add_API():
    try:
        API_data = request.json
        add_api_to_db(API_data)
    except Exception as e:
        logging.error(e)
    return Response()
    
@app.route('/deleteapi', methods=['DELETE'])
@basic_auth.required
def delete_API():
    try:
        tenant = request.args.get('tenant')
        api = request.args.get('api')
        delete_API_from_db(tenant,api)
        response = "API: " + api + " deleted from db successfully!!!"
    except Exception as e:
        logging.error(e)
        response = "[Error] Deleteing API from db for recommendation system!"
    return response

@app.route('/addapplication', methods=['POST']) 
@basic_auth.required
def add_application():
    try:
        application_data = request.json
        add_application_to_db(application_data)
        response = Response()
    except Exception as e:
        logging.error(e)
        response = Response()
    return response

@app.route('/updateapplication', methods=['POST']) 
@basic_auth.required
def update_application():
    try:
        application_data = request.json
        update_app_in_db(application_data)
        response = "Application updated to db successfully!!!"
    except Exception as e:
        logging.error(e)
        response = "[Error] Updating application in db for recommendation system!"
    return response

@app.route('/deleteapplication', methods=['DELETE'])
@basic_auth.required
def delete_application():
    try:
        app_id = request.args.get('appid')
        delete_application_from_db(app_id)
        response = "Application deleted from db successfully!"
    except Exception as e:
        logging.error(e)
        response = "[Error] Deleting application from db for recommendation system!"
    return response

@app.route('/addsearchquery', methods=['POST']) 
@basic_auth.required
def add_search_query():
    try:
        search_query = request.json
        add_search_query_to_db(search_query)
        response = "Search query added to db successfully!"
    except Exception as e:
        logging.error(e)
        response = "[Error] Publishing searched query to db for recommendation system!"
    return Response()

@app.route('/addclickedapi', methods=['POST']) 
@basic_auth.required
def add_clicked_API():
    try:
        clicked_API = request.json
        add_search_query_to_db(clicked_API)
        # response = "Clicked API: " + clicked_API['API_name'] + " added to db successfully!!!"
        response = Response(status=200)
    except Exception as e:
        logging.error(e)
        # response = "[Error] Publishing clicked API to db for recommendation system!"
        response = Response(status=404)
    return response   

def main():
    cron.start()
    context = None
    if HTTPS_ENABLED:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain(API_CRT, API_KEY)
        except Exception as e:
            sys.exit("Error starting flask server. " +
                "Missing cert or key. Details: {}"
                .format(e))

    update_user_recommendations_db()
    serving.run_simple(API_HOST, API_PORT, app, ssl_context=context, use_debugger=True)

if __name__ == '__main__':
    main()


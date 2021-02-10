import json
import pandas as pd
import pymysql
import pymongo
import sqlalchemy
from sqlalchemy import create_engine 
from flask import Flask, request, render_template, jsonify, make_response
import os 
from RB_dbFunctions import insert_user, view_exists
from RB_Scrape import scrape_title
from collections import Counter
import plotly.express as px

app = Flask(__name__)  

# # # # # # # # # # # # # # # #   
# Heroku check 
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True  

if is_heroku == True:
    # if IS_HEROKU is found in the environment variables, then use the rest
    # NOTE: you still need to set up the IS_HEROKU environment variable on Heroku (it is not there by default)
    mongoConn = os.environ.get('mongoConn')
    remote_db_endpoint = os.environ.get('remote_db_endpoint')
    remote_db_port = os.environ.get('remote_db_port')
    remote_db_name = os.environ.get('remote_db_name')
    remote_db_user = os.environ.get('remote_db_user')
    remote_db_pwd = os.environ.get('remote_db_pwd')
else:
    # use the config.py file if IS_HEROKU is not detected
    from config import mongoConn, remote_db_endpoint, remote_db_port, remote_db_name, remote_db_user, remote_db_pwd

# # # # # # # # # # # # # # # #   
## MY SQL CONN 
pymysql.install_as_MySQLdb() 
engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")

# # # # # # # # # # # # # # # #  
## ROUTES   

@app.route("/")
def index(): 
    return render_template("index.html") 

@app.route("/search")
def search(): 
    return render_template("search.html") 

@app.route("/maps")
def maps(): 
    return render_template("maps.html") 

@app.route("/plots", methods=['GET'])
def plots():
    #query = request.form['media_title'] 
    return render_template("plots.html")

@app.route("/lookup_result", methods=['GET'])
def form():
    #query = request.form['media_title'] 
    return render_template("lookup_result.html")
########################
## FIND A TITLE 
@app.route("/api/lookup", methods=['POST'])
def get_title():
    query = request.form['media_title'] 
    return lookup(query)

@app.route("/api/lookup/<query>")
def lookup(query):
  
    #MONGO CACHE CONN
    client = pymongo.MongoClient(mongoConn) 
    db = client.shows_db
    collection = db.items

  # TRY EXACT MATCH
    title_filter = {  
        "title": {"$regex": f'^{query}', "$options": 'i'}
    }
    #FIND TITLE IN MONGO CACHE
    dict_title = collection.find(title_filter, {'_id': False})
    df = pd.DataFrame(dict_title)
    print(len(df))
    if len(df) < 1:  # NO EXACT MATCH
        title_filter = { 
            # TRY LIKE * MATCH
            "title": {"$regex": f'.*{query}.*', "$options": 'i'}
        }
        #FIND TITLE IN MONGO CACHE
        dict_title = collection.find(title_filter, {'_id': False})
        df = pd.DataFrame(dict_title)

    print(title_filter)
    if len(df) < 1:  # NO RESULT FOUND IN CACHE
        # SCRAPE TITLE  
        dict_title = scrape_title(query)
        #LOAD TITLE
        df = pd.DataFrame([dict_title])
        #CACHE TITLE
        collection.insert_one(dict_title)
 
    try:
        _json = df.to_json(orient='records', default_handler=str) 
    except:
        _json = '{"title":"' + query + ' not found" }'
        
    _json = df.to_json(orient='records', default_handler=str)
  
    print(_json)
 
    resp = make_response(_json)
    resp.headers['content-type'] = 'application/json'
    return resp

########################
## GET DATA FROM DB RETURN JSON
@app.route("/api/view/<db_view_name>") #set up for testing need to SECCURE!!!!!
def get_db_view(db_view_name): 

    conn = engine.connect()  
    if not view_exists(db_view_name):
        return 'db view object not found / invalid'

    sql = f''' SELECT * FROM {db_view_name}'''
    df = pd.read_sql(sql, con=conn)
    _json = df.to_json(orient='records')
    resp = make_response(_json)
    resp.headers['content-type'] = 'application/json' 
    conn.close()
    return resp


########################
## INSERT FOR WHEN SERVICE IS SELECTED
@app.route("/insert_service_selection", methods=['GET', 'POST'])
def insert_service_selection():  
    ## INSERT HERE 
    return ''

########################
## INSERT USER DATA
@app.route("/create_user", methods=['GET', 'POST'])
def create_user():
    
    user_dict = {
        'User_Name': '',
        'First_Name': '',
        'Last_Name': '',
        'Age': 0,
        'Gender': '',
        'Frequency_ID': '',
        'Zip_Code': 20004,
        'Audit': 'test',
        'Services': ['']
    }
    userid = insert_user(user_dict)
    
    return ''

########################
## SEE IF TABLE / VIEW IN DB


########################
## BAR CHART OF SERVICES
@app.route("/services-viz/")
def services_viz(): 

    client = pymongo.MongoClient(mongoConn)
    db = client.shows_db
    items = db.items.find()
    service_list = []

    services = db.items.find({},{"_id":0, "services":1});
    for service in services:
        if (len(list(service.values())) != 0):
            for opt in list(service.values())[0]:
                service_list.append(opt)

    service_dict = dict(Counter(service_list))
    service_df = pd.DataFrame.from_dict(service_dict, orient='index')
    sds = service_df.sort_values(by=0, ascending=False)
    sds.reset_index(inplace=True)
    sds.rename(columns={'index':'service preferred by user', 0:'count'}, inplace=True)

    sds_short = sds[0:30]
    fig = px.bar(sds_short, x="service preferred by user", y="count")
    fig.write_html("templates/services-viz.html")

    return render_template("services-viz.html")

########################
## BAR CHART OF RECOMMENDATIONS
@app.route("/recommendations-viz/")
def recommendations_viz():

    client = pymongo.MongoClient(mongoConn)
    db = client.shows_db
    items = db.items.find()

    rec_list = []
    recs = db.items.find({},{"_id":0, "recommended":1});
    for rec in recs:
        if (len(list(rec.values()))!= 0):
            for opt in list(rec.values())[0]:
                if isinstance(opt, str):
                    rec_list.append(opt)

    rec_dict = dict(Counter(rec_list))
    rec_df = pd.DataFrame.from_dict(rec_dict, orient='index')
    rds = rec_df.sort_values(by=0, ascending=False)
    rds.reset_index(inplace=True)
    rds.rename(columns={'index':'recommendation', 0:'count'}, inplace=True)

    rds_short = rds[0:30]
    fig = px.bar(rds_short, x="recommendation", y="count")
    fig.write_html("templates/recommendations-viz.html")

    return render_template("recommendations-viz.html")


# run the app in debug mode
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)

#     ____                           ___
#    |  _ \  ___              _   _.' _ `.
# _  | [_) )' _ `._   _  ___ ! \ | | (_) |    _
#|:;.|  _ <| (_) | \ | |' _ `|  \| |  _  |  .:;|
#|   `.[_) )  _  |  \| | (_) |     | | | |.',..|
#':.   `. /| | | |     |  _  | |\  | | |.' :;::'
# !::,   `-!_| | | |\  | | | | | \ !_!.'   ':;!
# !::;       ":;:!.!.\_!_!_!.!-'-':;:''    '''!
# ';:'        `::;::;'             ''     .,  .
#   `:     .,.    `'    .::... .      .::;::;'
#     `..:;::;:..      ::;::;:;:;,    :;::;'
#       "-:;::;:;:      ':;::;:''     ;.-'
#           ""`---...________...---'"" 
#------------------------------------------------

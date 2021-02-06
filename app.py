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

# @app.route("/")
# def index(): 
#     return render_template("index.html") 

@app.route("/search")
def search(): 
    return render_template("search.html") 

########################
## FIND A TITLE 
@app.route("/api/lookup", methods=['POST'])
def lookup():

    query = request.form['media_title']

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
        #SCRAPE TITLE
        dict_title = scrape_title(query)
        #LOAD TITLE
        df = pd.DataFrame([dict_title])
        #CACHE TITLE
        collection.insert_one(dict_title)

    _json = df.to_json(orient='records', default_handler=str)
<<<<<<< HEAD

    print(_json)

=======
>>>>>>> a85067f1ca51ceb75b140fba7dc8000c97824407
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

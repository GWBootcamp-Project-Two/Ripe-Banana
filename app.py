import json
import pandas as pd
import pymysql
import pymongo
import sqlalchemy
from sqlalchemy import create_engine 
from flask import Flask, request, render_template, jsonify, make_response, redirect
import os 
from RB_dbFunctions import insert_user, view_exists, get_dataframe_from_db
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
    accessToken = os.environ.get('accessToken')
    
else:
    # use the config.py file if IS_HEROKU is not detected
    from config import mongoConn, remote_db_endpoint, remote_db_port, remote_db_name, remote_db_user, remote_db_pwd, accessToken
# # # # # # # # # # # # # # # #   
## MY SQL CONN 
pymysql.install_as_MySQLdb() 
engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")

# # # # # # # # # # # # # # # #  
## ROUTES   


@app.route("/", methods=['GET', 'POST'])
def index(): 
    tab = ''
    df_titles = pd.DataFrame()
    if request.method == 'POST':
        query = request.form['media_title']
        if query != '':
            df_titles = lookup(query)
            tab = 'search'
    return render_template("index.html", titles=df_titles.to_dict(orient='records'), accessToken=accessToken, tab=tab)

@app.route("/search")
def search(): 
    return render_template("search.html") 

@app.route("/maps")
def maps():
    return render_template("maps.html", accessToken=accessToken)


@app.route("/map")
def map():
    return render_template("maps.html", accessToken=accessToken)

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/lookup_result", methods=['GET', 'POST'])
def plots():
    #query = request.form['media_title'] 
    df_titles = pd.DataFrame()
    if request.method == 'POST': 
        query = request.form['media_title']
        if query != '':
            df_titles = lookup(query)
            print(df_titles.to_dict(orient='records'))
  
    return render_template("lookup_result.html", titles=df_titles.to_dict(orient='records'))
 
########################
## FIND A TITLE 
#Look up by 'Post' (a request)
@app.route("/api/lookup", methods=['POST'])
def post_title():
    query = request.form['media_title']  
    df = lookup(query)
    return render_template("plots.html", titles=df.to_dict(orient='records'))

#Look up - 
@app.route("/api/lookup/<query>")
def get_title(query):
    df = lookup(query)
    _json = df.to_json(orient='records', default_handler=str) 
    #print(_json) 
    resp = make_response(_json)
    resp.headers['content-type'] = 'application/json'
    return resp
 
def lookup(query): 
    #MONGO DB CONNECTION FOR CACHED TITLES
    client = pymongo.MongoClient(mongoConn) 
    db = client.shows_db
    collection = db.items

  # TRY EXACT MATCH : With Exact Regular Expression
    title_filter = {  
        "title": {"$regex": f'^{query}', "$options": 'i'}
    }
    #FIND TITLE IN MONGO CACHE
    dict_title = collection.find(title_filter, {'_id': False})
    df_title = pd.DataFrame(dict_title)
  
    if len(df_title) < 1:  #IF NO EXACT MATCH
        title_filter = { 
            # TRY LIKE * MATCH : Regular Expression w/broader search capacity
            "title": {"$regex": f'.*{query}.*', "$options": 'i'}
        }
        #FIND TITLE IN MONGO CACHE
        dict_title = collection.find(title_filter, {'_id': False})
        df_title = pd.DataFrame(dict_title)

    print(title_filter)
    if len(df_title) < 1:  # NO RESULT FOUND IN CACHE 
        dict_title = scrape_title(query)  # SCRAPE TITLE 
        df_title = pd.DataFrame([dict_title])  # LOAD TITLE 
        collection.insert_one(dict_title)  # CACHE TITLE
    df_title = df_title.drop_duplicates(subset='title', keep='last', inplace=False) #Drop any duplicate search results
    try:# TO MAP SERVICE(from mySQL) INFO TO MONGO DATA
        df_StreamingServices = get_dataframe_from_db('streamingservices') #calls function from RB_dbFunctions.py bring in mySQL services table data

        #For Line 135: Had issues with columns returning with numbers instead of column names. May not need this line need to test      
        df_StreamingServices.rename(columns={0: 'Service_ID', 1: 'Service_Name',
                            2: 'Service_Type', 3: 'Service_Img', 4: 'Service_Url'}, inplace=True)
 
        dic_titles = df_title.to_dict(orient='records')#Turn data frame into dictionary

        #Loop 
        for title in dic_titles: #for each title in list
            title['services_info'] = [] #create empty list for service info
            for service in title['services']: #Loop through service for each title
                try:
                    df_services_info = df_StreamingServices.loc[df_StreamingServices['Service_Name'] == service] #Filter to match up service name to record in mySQL services
                    dict_services_info = df_services_info.to_dict(orient='records')[0] #turn data frame into dictionary
                    print(f'StreamingServices Record : {dict_services_info}')
                    title['services_info'].append(dict_services_info) #appends dictionary to list
                    print(f'Scraped Service : {service} ')
                except:
                    print(f'{service} meta not found')
                    #raise
        df_title = pd.DataFrame(dic_titles)

    except:
        print(f' Services Failed to Map') 
        #raise
         
    return df_title
    

########################
## GET DATA FROM DB RETURN JSON
@app.route("/api/view/<db_view_name>") #set up for testing need to SECCURE!!!!!
def get_db_view(db_view_name): 
 
    df = get_dataframe_from_db(db_view_name)
    _json = df.to_json(orient='records')
    resp = make_response(_json)
    resp.headers['content-type'] = 'application/json'  
    return resp
 

########################
## INSERT USER DATA
@app.route("/create_user", methods=['GET', 'POST'])
def create_user(): 
    if request.method == "POST":
        try:
            age = request.form["userAge"]
            zips = request.form["userZip"]
            frequency = request.form["userFreq"] 
            service = request.form.getlist('userServ')
            stream_dict = {
                "User_Name":'',
                "First_Name":'',
                "Last_Name":'',
                'Age': age,
                'Gender':'',
                'Frequency_ID': frequency,
                'Zip_Code': zips,
                'Audit':'TEST',
                'Services': service
            }  
            user_id = insert_user(stream_dict) 
            print(f'{str(user_id)}{stream_dict}')
        except:
            print(f'create user fail')
        return redirect("/thankyou", code=302)

    return render_template("create_user.html")

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

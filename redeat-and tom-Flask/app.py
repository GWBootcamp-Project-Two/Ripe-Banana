from flask import Flask, render_template, redirect
import pymongo
import scrape_reelgood
app = Flask(__name__)

conn = 'mongodb://localhost:27017/craigslist_app'
client = pymongo.MongoClient(conn)
db = client.craigslist_app

@app.route("/")
def index():
    listings = db.listings.find_one()
    return render_template("index.html", listings=listings)

@app.route("/scrape")
def scraper():
    listings = db.listings
    listings_data = scrape_craigslist.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
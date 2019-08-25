from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_scrape = mongo.db.mars_scrape.find_one()
    return render_template("index.html", mars_scrape=mars_scrape)
    
@app.route("/scrape")
def scraper():
    mars_scrape = mongo.db.mars_scrape
    mars_scrape = mars_scrape.scrape()
    mars_scrape.update({}, mars_scrape, upsert=True)
    return redirect("/", code=302)
    
if __name__ == "__main__":
    app.run(debug=True)
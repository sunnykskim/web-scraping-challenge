from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return "Done"

# Define Main Behavior
if __name__ == "__main__":
    app.run()
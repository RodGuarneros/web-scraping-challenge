# Creating an instance of Flask
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db 

# Creating the routes
@app.route("/")
def home():
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraping():
    main_dict = scrape_mars.scrape()
    db.mars.update({}, main_dict, upsert=True)

if __name__ == "__main__":
    app.run(debug=True)


# import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping 
# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
# The second line says we'll use PyMongo to interact with our Mongo database.
# The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection, port 27017 is the default for mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # URI: uniform resource identifier, similar to URL
#This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".

# a port is a number assigned to uniquely identify a connection endpoint and to direct data to a specific service. 
# At the software level, within an operating system, 
# a port is a logical construct that identifies a specific process or a type of network service.

mongo = PyMongo(app)

# define the route for the html page:
@app.route("/") # tells Flask what to display when we're looking at the home page, index.html 

def index():
    # uses PyMongo to find the "mars" collection in our database, 
    # which we will create when we convert our Jupyter scraping code to Python Script. 
    mars = mongo.db.mars.find_one()

    # tells Flask to return an HTML template using an index.html file. We'll create this file after we build the Flask routes.
    return render_template("index.html", mars = mars)  # mars=mars tells Python to use the "mars" collection in MongoDB.


# define flask route that will run the function below
@app.route("/scrape")

def scrape():

    mars = mongo.db.mars # assign a new variable that points to our database

    mars_data = scraping.scrape_all() # referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.

    # Now that we've gathered new data, we need to update the database using .update_one()
    # syntax: .update_one(query_parameter, {"$set": data}, options)
    mars.update_one({}, {"$set": data}, upsert = True)
    # In the query_parameter, we can specify a field (e.g. {"news_title": "Mars Landing Successful"}), 
    # and MongoDB will update a document with a matching news_title. 
    # Or it can be left empty ({}) to update the first matching document in the collection.
    # Next, we'll use the data we have stored in mars_data. The syntax used here is {"$set": data}. 
    # This means that the document will be modified ("$set") with the data in question.
    # upsert=True indicates to Mongo to create a new document if one doesn't already exist, 
    # and new data will always be saved (even if we haven't already created a document for it).

    # Finally, we will add a redirect after successfully scraping the data: return redirect('/', code=302). 
    # This will navigate our page back to / where we can see the updated content.
    return redirect('/', code = 302)

    # tell flask to run

    if __name == "__main__":

        app.run()
        
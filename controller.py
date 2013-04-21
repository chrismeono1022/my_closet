from flask import Flask, render_template, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy
import model
from geopy import geocoders
import requests

app = Flask(__name__)

# from http://postgresapp.com/documentation
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/my_closet.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
	user_id = 1
	user_location_query = model.session.query(model.User).filter_by(id=user_id).one()
	location = user_location_query.location
	g = geocoders.GoogleV3()
	place,(lat, lng) = g.geocode(location)
	r = requests.get("foreign key here"+"/" + str(lat) + "," + str(lng))
	temp_json = r.json()
	temp = temp_json['currently']['temperature']

	# top = model.session.query(model.Item).filter_by(type="top").first()
	#bottom = 
	#print top.name
	return render_template("home.html", location = location, temp = temp) 

if __name__ == "__main__":
	print "we are in controller.py"
	app.run(debug = True)
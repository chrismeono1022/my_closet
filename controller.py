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
	# user_id = 1
	# user_location_query = model.session.query(model.User).filter_by(id=user_id).one()
	# location = user_location_query.location
	# g = geocoders.GoogleV3()
	# place,(lat, lng) = g.geocode(location)
	# r = requests.get("insert api key here"+"/" + str(lat) + "," + str(lng))
	# temp_json = r.json()
	# temp = temp_json['currently']['temperature']
	test_temp = 65
	test_location = 90291

	top = model.session.query(model.Item).filter_by(type="top").first()
	top_image = top.image_url
	bottoms = model.session.query(model.Item).filter_by(type="bottoms").first()
	bottoms_image = bottoms.image_url
	outer = model.session.query(model.Item).filter_by(type="outerwear").first()
	outer_image = outer.image_url
	shoes = model.session.query(model.Item).filter_by(type="shoes").first()
	shoes_image = shoes.image_url
	jewelry = model.session.query(model.Item).filter_by(type="jewelry").first()
	jewelry_image = jewelry.image_url
	accessories = model.session.query(model.Item).filter_by(type="accessories").first()
	accessories_image = accessories.image_url

	return render_template("home.html", location=test_location, temp=test_temp, top=top_image, bottoms=bottoms_image, outer=outer_image, shoes=shoes_image, jewelry=jewelry_image, accessories=accessories_image) 

if __name__ == "__main__":
	print "we are in controller.py"
	app.run(debug = True)
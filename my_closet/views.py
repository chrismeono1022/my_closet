from flask import render_template
from my_closet import app
from my_closet.models import Item
from my_closet.models import DBSession
from geopy import geocoders
import requests
import random
import os


# api key stored as environment variable
FORECAST_IO = os.environ.get('forecast_io')


@app.route("/")
def index():

    #query user location, based on user_id
    #location = DBSession.query(User).filter_by(id=1)
    test_location = 90291
    # g = geocoders.GoogleV3()
    # place,(lat, lng) = g.geocode(test_location) #change to location
    # r = requests.get("https://api.forecast.io/forecast/"+str(FORECAST_IO)+"/" + str(lat) + "," + str(lng))
    # temp_json = r.json()
    # temp = temp_json['currently']['temperature']
    test_temp = 65
    

    items = DBSession.query(Item).all()

    items_group = {}

    for item in items:
        if item.type not in items_group:
            items_group[item.type] = []
        items_group[item.type].append(item)


    blacklist_rules = {
        'dress': ['top', 'bottoms'],
        'top': ['dress'],
        'bottom': ['dress']
    }

    outfits = []

    # Run the logic 3 times
    for i in xrange(3):
        outfit_items = []
        matched_rules = []

        keys = items_group.keys()

        # keys is the collection of the types we have in the 
        # database, we want to sort them randomly so that we 
        # can get tops and dresses.  Our algorithm right now
        # says if you get a top, you can't have a dress, so 
        # we want to make sure we don't loop in the same order
        # every time
        random.shuffle(keys)

        for type_ in keys:
            blacklisted = False
            
            # check if this type has been blacklisted
            for rule in matched_rules:
                if type_ == rule:
                    blacklisted = True

            if not blacklisted:
                # if we haven't blacklisted the type, get any blacklist
                # rules it has, for instance if this is a shirt, lets
                # blacklist dresses
                if type_ in blacklist_rules:
                    matched_rules += blacklist_rules[type_]

                # get a random item for this specific type and
                # add it to the outfit
                item = random.choice(items_group[type_])
                outfit_items.append(item)

        outfits.append(outfit_items)


    return render_template("home.html", outfits=outfits, temp=test_temp, location=test_location)

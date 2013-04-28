from flask import render_template, session, request, flash, redirect, url_for, g
from my_closet import app
from my_closet.models import Item #user, outfit
from my_closet.models import DBSession
from my_closet.forms import Login
from geopy import geocoders
import requests
import random
import os


# app.secret_key = str(app.config['secret_key'])

@app.route("/", methods=["GET", "POST"])
def root():

    form = Login()
    return render_template("login.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():

    email = form.email.data
    password = form.password.data

    try:
        user = DBSession.query(User).filter_by(email=email).one() #, password=password

    except:
        flash("Invalid username or password", "error")
        return render_template("login.html")

    session['user_id'] = user.id
    return render_template("home.html")



@app.route("/home")
def home():

    #query user location, based on user_id
    #user_id=acquire from user session
    #location = DBSession.query(User).filter_by(id=user_id)
    location = 90291
    # g = geocoders.GoogleV3()
    # place,(lat, lng) = g.geocode(location) #change to location
    # url = ("https://api.forecast.io/forecast/"+str(app.config['forecast_io'])+"/" + str(lat) + "," + str(lng))
    # r = requests.get(url)
    # temp_json = r.json()
    # temp = temp_json['currently']['temperature']
    temp = 46 #random.randint(0, 100)


    items = DBSession.query(Item).filter(Item.low_temp<temp, Item.high_temp>temp)

    #organize items by type e.g. shoes, tops, bottoms, etc
    items_by_type = {}

    for item in items:
        if item.type not in items_by_type:
            items_by_type[item.type] = []
        items_by_type[item.type].append(item)


    #create a list of dress vs bottom type of outfit, which is weighted based on the results from the DB

    weighted_picker = []

    if 'bottoms' in items_by_type:
        for i in range(len(items_by_type['bottoms'])):
            weighted_picker.append('bottoms')

    if 'dress' in items_by_type:
        for i in range(len(items_by_type['dress'])):
            weighted_picker.append('dress')



    outfits = [] #list is composed of [outfit_items] lists

    for i in range(3):

        outfit_items = []

        #pick dress or bottom, and return outfit items based on this choice
        random.shuffle(weighted_picker)
        a = random.choice(weighted_picker)  

        #for key in dict, select random value 
        for key in items_by_type:
            item = random.choice(items_by_type[key])

            if a == 'bottoms' and item.type == 'dress' : #if outfit choice bottom, and item is dress, skip
                pass 
            elif a == 'dress' and (item.type == 'bottoms' or item.type == 'top'): # if outfit choice is dress, and item bottoms or top, pass
                pass
            else: 
                outfit_items.append(item) #append all other items

        outfits.append(outfit_items) # append to list outside loop


    return render_template("home.html", temp=temp, location=location, outfits=outfits)




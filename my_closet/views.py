from flask import render_template, session, request, flash, redirect, url_for, g
from flask.ext.wtf import Form
from my_closet import app
from my_closet.models import Item, User
from my_closet.models import DBSession
from my_closet.forms import Login
from geopy import geocoders
import requests
import random
import os
import pdb

app.secret_key = 'development_key'

@app.before_request
def before_request():

    if not request.path.startswith("/static"):

        try:
            g.user = DBSession.query(User).filter_by(id=session.get('user_id')).one()

            # print "session %s" % session['user_id']
            # print "g.user is %s" % g.user.email
        except Exception:
            print Exception



@app.route("/", methods=["GET", "POST"])
def root():

    form = Login(csrf_enabled=True)
    return render_template("login.html", form=form)


@app.route("/login", methods=["POST"])
def login():

    form = Login(request.form)
    email = form.email.data
    password = form.password.data


    try:
        g.user = DBSession.query(User).filter_by(email=email, password=password).one()
        session['user_id'] = g.user.id
        print "user is %s " % session['user_id']
        return redirect(url_for("home"))

    except: #Exception as inst:
        # print type(inst)
        # print inst.args
        flash("Invalid username or password", "error")
        return render_template("login.html", form=form)



@app.route("/home")
def home():
    print os.environ['FORECASTIO']
    user_location = DBSession.query(User).filter_by(email=g.user.email).one()
    location = user_location.location
    geo = geocoders.GoogleV3()
    place,(lat, lng) = geo.geocode(location) #change to location
    # url = ("https://api.forecast.io/forecast/"+str(app.config['forecast_io'])+"/" + str(lat) + "," + str(lng))
    # app.config['forecast_io']
    url = ("https://api.forecast.io/forecast/"+str(os.environ['FORECASTIO'])+"/" + str(lat) + "," + str(lng))

    r = requests.get(url)
    temp_json = r.json()
    temp = temp_json['currently']['temperature']
    icon = temp_json['currently']['icon']
    forecast = temp_json['currently']['summary']
    daily_low = temp_json['daily']['data'][0]['temperatureMin']
    daily_high = temp_json['daily']['data'][0]['temperatureMax']
    place = temp_json['timezone']
    loc = place.split('/')[1]
    # location = "San Francisco, CA"
    # temp = random.randint(55, 70)
    # forecast = 'Clear all day'
    # daily_low = 55
    # daily_high = 65
    session['location']=loc
    session['forecast']=forecast
    session['daily_low']=round(daily_low)
    session['daily_high']=round(daily_high)
    session['current']=round(temp)


    items = DBSession.query(Item).filter(Item.low_temp<session.get('current'), Item.high_temp>session.get('current')).filter_by(user_id=g.user.id).all()


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

            if a == 'bottoms' and item.type == 'dress': #if outfit choice bottom, and item is dress, skip
                pass 
            elif a == 'dress' and (item.type == 'bottoms' or item.type == 'top'): # if outfit choice is dress, and item bottoms or top, pass
                pass
            else: 
                outfit_items.append(item) #append all other items

        outfits.append(outfit_items) # append to list outside loop


    return render_template("home.html", outfits=outfits, location=session.get('location'), forecast=session.get('forecast'), daily_high=session.get('daily_high'), daily_low=session.get('daily_low'), temp=session.get('current'))

@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("root"))


@app.route("/my_closet", methods=['GET'])
def my_closet():
    items = DBSession.query(Item).filter_by(user_id=g.user.id).all()

    return render_template("my_closet.html", items=items, location=session.get('location'), forecast=session.get('forecast'), daily_high=session.get('daily_high'), daily_low=session.get('daily_low'), temp=session.get('current'))

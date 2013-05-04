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

app.secret_key = 'development_key'


@app.before_request
def before_request():
    try:
        g.user = session.get('user_id')
        print "session %s" % session['user_id']
        print "g.user is %s" % g.user
        print "development key %s" % app.secret_key
    except:
        g.user = False
        form = Login(request.form)
        return render_template("login.html", form=form)



@app.route("/", methods=["GET", "POST"])
def root():

    FORM = Login(csrf_enabled=True)
    return render_template("login.html", form=form)


@app.route("/login", methods=["POST"])
def login():

    form = Login(request.form)
    email = form.email.data
    password = form.password.data


    if g.user == None:
        return render_template("login.html", form=form)
    else:
        try:
            user = DBSession.query(User).filter_by(email=email, password=password).one()
            session['user_id'] = user.id
            print "user is %s " % session['user_id']
            return redirect(url_for("home"))

        except: #Exception as inst:
            # print type(inst)
            # print inst.args
            flash("Invalid username or password", "error")
            return render_template("login.html", form=form)

    # if g.user is None:
    #     try:
    #         user = DBSession.query(User).filter_by(email=email, password=password).one()
    #         session['user_id'] = user.id
    #         print "user is %s " % session['user_id']
    #         return redirect(url_for("home"))

    #     except: #Exception as inst:
    #         # print type(inst)
    #         # print inst.args
    #         flash("Invalid username or password", "error")
    #         return render_template("login.html", form=form)
    # else:
    #     return redirect(url_for("home"))

@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("root"))


@app.route("/home")
def home():
    if g.user != False:
        id = g.user
        #query user location, based on user_id
        #user_id=acquire from user session
        # location = DBSession.query(User).filter_by(id=user_id)
        location = "Los Angeles, CA"
        # g = geocoders.GoogleV3()
        # place,(lat, lng) = g.geocode(location) #change to location
        # url = ("https://api.forecast.io/forecast/"+str(app.config['forecast_io'])+"/" + str(lat) + "," + str(lng))
        # r = requests.get(url)
        # temp_json = r.json()
        # temp = temp_json['currently']['temperature']
        # icon = temp_json['currently']['icon']
        # forecast = temp_json['currently']['summary']
        # daily_low = temp_json['daily']['data'][0]['temperatureMin']
        # daily_high = temp_json['daily']['data'][0]['temperatureMax']
        # place = temp_json['timezone']
        temp = 64 #random.randint(0, 100)
        forecast = 'Clear all day'
        daily_low = 50
        daily_high = 64



        items = DBSession.query(Item).filter(Item.low_temp<temp, Item.high_temp>temp).filter_by(id=id)

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

        # ["bottoms|"] * len(items_by_time['bottoms'])
        # weighted_picker[0].split('|')



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


        return render_template("home.html", temp=temp, location=location, outfits=outfits, forecast=forecast, daily_high=daily_high, daily_low=daily_low,)




from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from itertools import *
from asst.models import hotel
import traceback, sys
import math
import random
import json
import time

page = Blueprint('reservation', __name__, template_folder='templates')

@page.route("/",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def reservation(role):
    return render_template('reservation/index.html', logged_in=True,role=role)


@page.route("/load_hotel",methods=['POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def get_hotels(role):
    try:
        data = request.get_json()
        country = data['country']
        state = data['state']
        hotels = []
        for h in hotel.Hotel.select().where(hotel.Hotel.State == state, hotel.Hotel.Country == country):
            hotels.append([h.HotelID, h.City, h.State, h.Country])
        print(hotels)
        return json.dumps(hotels)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return "Error", 500

    return render_template('reservation/index.html', logged_in=True,role=role)

@page.route('/search_reg',methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def search_reg(role):
    if request.method == 'POST':
        try:
            country = request.form['country']
            state = request.form['state']
        except:
            flash("Please enter a country and state to search", 'danger')
            return render_template('reservation/index.html', logged_in=True,role=role)  
    return render_template('reservation/index.html', logged_in=True,role=role)




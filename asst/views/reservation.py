from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from itertools import *
from asst.models import hotel, room, breakfast, service
from flask_table import Table, Col, ButtonCol
import traceback, sys
import math
import random
import json
import time

page = Blueprint('reservation', __name__, template_folder='templates')

# Declare your table
class ItemTable(Table):
    '''
    This is a itemTable class that generates text/html automatically to create a table for created reservations
    '''
    html_attrs = {'class': 'table table-striped'}
    room_no = Col('Room Number')
    max_guests = Col('Max Guests')
    description = Col('Description')
    price = Col('Price')
    r_type = Col('Room Type')
    order = ButtonCol('Order','reservation.order',url_kwargs=dict(rn='room_no', hid = 'hotel_id'),button_attrs={'class': 'btn btn-success'})


@page.route("/",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def reservation(role):
    return render_template('reservation/index.html', logged_in=True,role=role)

@page.route("/submit_order",methods=['POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def submit_order(role):
    try:
        services = request.form.getlist('services')
        cc = request.form['cc']
    except:
        traceback.print_exc(file=sys.stdout)
        flash("Please enter a country and state to search", 'danger')
        return render_template('reservation/index.html', logged_in=True,role=role)  
    return render_template('reservation/thanks.html', logged_in=True,role=role)

@page.route("/order",methods=['GET', 'POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def order(role):
    hotel_id = request.args.get('hid')
    room_no = request.args.get('rn')
    break_off = {}
    serv_off = {}
    for r in breakfast.Breakfast.select().where(breakfast.Breakfast.HotelID == hotel_id):
        try:
            break_off[r.BType] = dict(price = r.bPrice, desc =  r.Description, type =  r.BType)
        except:
            continue;
    for s in service.Service.select().where(service.Service.HotelID == hotel_id):
        try:
            serv_off[s.sType] = dict(price = s.sCost, type =  s.sType)
        except:
            continue;
    room_s = {}
    for r in room.Room.select().where(room.Room.HotelID == hotel_id, room.Room.Room_no == room_no):
        try:
            room_s = dict(hotel_id = r.HotelID, room_no = r.Room_no, max_guests = r.Capacity, description = r.Description, price = r.Price, r_type = r.Type)
        except:
            continue;
    return render_template('reservation/order_page.html', logged_in=True,role=role, break_off = break_off, room = room_s, serv_off = serv_off) 


@page.route("/make_res",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def make_res(role):
    hotel_id = request.args.get('id')

    rooms = []
    for r in room.Room.select().where(room.Room.HotelID == hotel_id):
        try:
            rooms.append(dict(hotel_id = r.HotelID, room_no = r.Room_no, max_guests = r.Capacity, description = r.Description, price = r.Price, r_type = r.Type))
        except:
            continue;
    table = ItemTable(rooms)


    return render_template('reservation/room_list.html', logged_in=True,role=role,table=table)


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




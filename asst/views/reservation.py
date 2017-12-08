from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from itertools import *
from asst.models import hotel, room, breakfast, service, card, res, discount, includes
from flask_table import Table, Col, ButtonCol
import flask_login
import datetime
from dateutil.parser import parse
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
    order = ButtonCol('Order','reservation.order',url_kwargs=dict(rn='room_no', hid = 'hotel_id', checkin='checkin',checkout='checkout', price = 'price_num'),button_attrs={'class': 'btn btn-success'})


@page.route("/",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def reservation(role):
    return render_template('reservation/index.html', logged_in=True,role=role)

@page.route("/submit_order",methods=['POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def submit_order(role):
    try:
        user = flask_login.current_user
        cid = user.CID
        now = datetime.datetime.now()
        date_now =  now.strftime("%Y-%m-%d")
        hotel_id = request.form['hotelid']
        room_no = request.form['room_no']
        guests = request.form['guests']
        checkin = parse(request.form['checkin'])
        checkout = parse(request.form['checkout'])
        services = request.form.getlist('services')
        amer_break = int(request.form['b1'])
        beng_break = int(request.form['b2'])
        chin_break = int(request.form['b3'])
        mexi_break = int(request.form['b4'])
        card_name = request.form['cname']
        cc = request.form['cc']
        price = float(request.form['price'])
        ctype = request.form['ctype']
        csv = request.form['csv']
        billaddr = request.form['baddr']
        cc_exp = request.form['ccexpire']
        # make cc first
        try:
            card.CreditCard.create_card(cc, billaddr, card_name, csv, ctype, cc_exp)
        except:
            pass
        # make res next
        reser = res.Reservation.create_res(date_now, checkout, checkin, room_no, hotel_id, cc, cid, price)
        # make breakfast
        if amer_break > 0:
            includes.Inc_Breakfast.create_i_b("american", reser.InvoiceNo, hotel_id)
        if beng_break > 0:
            includes.Inc_Breakfast.create_i_b("bengali", reser.InvoiceNo, hotel_id)
        if chin_break > 0:
            includes.Inc_Breakfast.create_i_b("chinese", reser.InvoiceNo, hotel_id)
        if mexi_break > 0:
            includes.Inc_Breakfast.create_i_b("mexican", reser.InvoiceNo, hotel_id)
        # make services
        for smile in services:
            includes.Cont_Service.create_c_s(smile.split()[0], reser.InvoiceNo, hotel_id)
    except:
        traceback.print_exc(file=sys.stdout)
        flash("There was an error processing your request. Please try again", 'danger')
        return render_template('reservation/index.html', logged_in=True,role=role)  
    return render_template('reservation/thanks.html', logged_in=True,role=role)

@page.route("/order",methods=['GET', 'POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def order(role):
    hotel_id = request.args.get('hid')
    room_no = request.args.get('rn')
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    price = request.args.get('price')
    break_off = {}
    serv_off = {}
    for r in breakfast.Breakfast.select().where(breakfast.Breakfast.HotelID == hotel_id):
        try:
            break_off[r.BType] = dict(price = r.bPrice, desc =  r.Description, type =  r.BType)
        except:
            continue
    for s in service.Service.select().where(service.Service.HotelID == hotel_id):
        try:
            serv_off[s.sType] = dict(price = s.sCost, type =  s.sType)
        except:
            continue
    room_s = {}
    for r in room.Room.select().where(room.Room.HotelID == hotel_id, room.Room.Room_no == room_no):
        try:
            room_s = dict(hotel_id = r.HotelID, room_no = r.Room_no, max_guests = r.Capacity, description = r.Description, price = r.Price, r_type = r.Type)
        except:
            continue
    return render_template('reservation/order_page.html', logged_in=True,role=role, break_off = break_off, price = price, room = room_s, serv_off = serv_off, checkin = checkin, checkout = checkout, prev_inf = [hotel_id, room_no]) 


@page.route("/make_res",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def make_res(role):
    hotel_id = -1
    try:
        hotel_id = request.args.get('id')
        checkin = parse(request.args.get('checkin'))
        checkout = parse(request.args.get('checkout'))
    except:
        traceback.print_exc(file=sys.stdout)
        flash("Could not find any rooms for the specified dates", 'danger')
    rooms = []
    for r in room.Room.select().where(room.Room.HotelID == hotel_id):
        try:
            dc = 0
            price = str(r.Price)
            for sav in  discount.Discount.select().where(discount.Discount.HotelID == hotel_id,discount.Discount.Room_no == r.Room_no, 
               discount.Discount.SDate <= checkin, discount.Discount.EDate >= checkout):
                dc = sav.Discount
                price = '\u0336'.join(price) + '\u0336' + " " + str(round((1- dc) * r.Price,2))
            rooms.append(dict(hotel_id = r.HotelID, room_no = r.Room_no, max_guests = r.Capacity, description = r.Description, price = price, r_type = r.Type, \
                checkin = checkin, checkout = checkout, price_num = (1- dc) * r.Price))
        except:
            traceback.print_exc(file=sys.stdout)
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




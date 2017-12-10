from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from itertools import *
from asst.models import hotel, room, breakfast, service,  res, review, includes
from flask_table import Table, Col, ButtonCol
import flask_login
import datetime
from dateutil.parser import parse
import traceback, sys
import math
import random
import json
import time

page = Blueprint('feedback', __name__, template_folder='templates')
inv_no = '1'
class ItemTable(Table):
    '''
    This is a itemTable class that generates text/html automatically to create a table for created reservations
    '''
    html_attrs = {'class': 'table table-striped'}
    inv = Col('Invoice No')
    out_date = Col('Check Out')
    in_date = Col('Check In')
    room_no = Col('Room Number')
    hotel_id = Col('Hotel ID')


@page.route('/', methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def feedback(role):
    return render_template('feedback/index.html', logged_in=True,role=role)

@page.route("/pick_res",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def pick_res(role):
    reserv = []
    hotel_id = -1
    global inv_no
    try:
        user = flask_login.current_user
        cid = user.CID
        INV_NO = request.args.get('id')
        inv_no = INV_NO
    except:
        traceback.print_exc(file=sys.stdout)
        flash("Could not find any rooms for the specified dates", 'danger')
        return render_template('feedback/index.html', logged_in=True,role=role)
    for r in res.Reservation.select().where(res.Reservation.CID == cid, res.Reservation.InvoiceNo == inv_no):
        try:
            reserv.append(dict(inv = r.InvoiceNo, ordered = r.ResDate, out_date = r.OutDate, in_date = r.InDate, room_no = r.Room_no, hotel_id = r.HotelID, \
                               cnumber = r.CNumber, totalamt = r.TotalAmt, cid = r.CID))
        except:
            traceback.print_exc(file=sys.stdout)
            continue
    table = ItemTable(reserv)
    return render_template('feedback/make_rev.html', logged_in=True,role=role, table = table)

@page.route("/load_Res", methods=['POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def get_reserv(role):
    try:
        data = request.get_json()
        RevType = data['RevType']
        reserv = []
    #    bf = 'none'
    #    serv = 'none'
        rmtype = 'none'
        user = flask_login.current_user
        cid = user.CID
        for r in res.Reservation.select().where(res.Reservation.CID == cid):
            invoic_no = r.InvoiceNo
           # for b in includes.Inc_Breakfast.select().where(includes.Inc_Breakfast.InvoiceNo == invoic_no):
            #    bf.append(b)
           # for se in includes.Cont_Service.select().where(includes.Cont_Service.InvoiceNo == invoic_no):
           #     serv.append(se)
            for rt in room.Room.select().where(room.Room.Room_no == r.Room_no):
                rmtype = rt.Type
            reserv.append([r.HotelID, rmtype, r.Room_no, r.InvoiceNo])
        return json.dumps(reserv)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return "Error", 500

    return render_template('feedback/index.html', logged_in=True,role=role)
@page.route('/success',methods=['GET', 'POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def rreview(role):
    SCounter = 0
    try:
        user = flask_login.current_user
        cid = user.CID
        RevType = request.form['rest']
        rrate = int(request.form['optradio'])
        bfrate = int(request.form['optradio2'])
        srate = int(request.form['optradio3'])
        roomtype = request.form['rtype']
        bftype = request.form['bftype']
        stype = request.form['stype']
        global inv_no
        q = res.Reservation.select().where(res.Reservation.CID == cid, res.Reservation.InvoiceNo == inv_no)
        if RevType == '1':
            try:
                rm = room.Room.select().where(room.Room.HotelID == q.HotelID, room.Room.Room_no == q.Room_no)
                if rm.Type == roomtype:
                    Text = request.form['description']
                    review.Review.create_review(rrate, Text, cid, inv_no)
                    SCounter = 1
            except:
                traceback.print_exc(file=sys.stdout)
                flash("There was an error processing your request. Please try again", 'danger')
                return render_template('feedback/index.html', logged_in=True, role=role)
        elif RevType == '2':
            try:
                for food in includes.Inc_Breakfast.select().where(includes.Inc_Breakfast.InvoiceNo == inv_no):
                    try:
                        if food.BType == bftype:
                            Text = request.form['description2']
                            review.Review.create_review(bfrate, Text, cid, inv_no)
                            SCounter = 1
                    except:
                        continue
            except:
                traceback.print_exc(file=sys.stdout)
                flash("There was an error processing your request. Please try again", 'danger')
                return render_template('feedback/index.html', logged_in=True, role=role)
        elif RevType == '3':
            try:
                for ser in includes.Cont_Service.select().where(includes.Cont_Service.InvoiceNo == inv_no):
                    try:
                        if ser.SType == stype:
                            Text = request.form['description3']
                            review.Review.create_review(srate, Text, cid, inv_no)
                            SCounter = 1
                    except:
                        continue
            except:
                traceback.print_exc(file=sys.stdout)
                flash("There was an error processing your request. Please try again", 'danger')
                return render_template('feedback/index.html', logged_in=True, role=role)
    except:
        traceback.print_exc(file=sys.stdout)
        flash("There was an error processing your request. Please try again", 'danger')
        return render_template('feedback/index.html', logged_in=True,role=role)
    if SCounter != 0:
        return render_template('feedback/success.html', logged_in=True, role=role)
    else:
        flash("error", 'danger')
        return render_template('feedback/index.html',logged_in=True, role=role)
@page.route('/success',methods=['GET', 'POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def submit(role):
    return render_template('feedback/success.html', logged_in=True, role=role)
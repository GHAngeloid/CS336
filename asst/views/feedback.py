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

@page.route('/', methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def feedback(role):
    return render_template('feedback/index.html', logged_in=True,role=role)
@page.route("/load_Res", methods=['POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def get_reserv(role):
    try:
        data = request.get_json()
        reserv = []
        bf = []
        serv = []
        user = flask_login.current_user
        cid = user.CID
        for r in res.Reservation.select().where(res.Reservation.CID == cid):
            print(str(r.InvoiceNo))
            invoic_no = r.InvoiceNo
            for b in includes.Inc_Breakfast.select().where(includes.Inc_Breakfast.InvoiceNo == invoic_no):
                bf.append(b)
            for se in includes.Cont_Service.select().where(includes.Cont_Service.InvoiceNo == invoic_no):
                serv.append(se)
            rmtype = room.Room.Type.select().where(room.Room.Room_no == r.Room_no)
            reserv.append([r.HotelID, rmtype, r.Room_no, serv, bf])
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
        revtype = request.args.get('res')
        if revtype == '1':
            roomtype = request.args.get('rtype')
            for q in res.Reservation.select().where(res.Reservation.CID == cid):
                try:
                    inv_no = q.InvoiceNo
                    for rm in room.Room.select().where(room.Room.HotelID == q.HotelID, room.Room.Room_no == q.Room_no):
                        try:
                            if rm.Type == roomtype:
                                rrate = request.args.get('optradio1')
                                rdes = request.args.get('description')
                                review.Review.create_review(rrate, rdes, cid, inv_no)
                                SCounter = 1
                        except:
                            continue
                except:
                    continue
        elif revtype == '2':
            bftype = request.args.get('bftype')
            for q in res.Reservation.select().where(res.Reservation.CID == cid):
                try:
                    inv_no = q.InvoiceNo
                    for food in includes.Inc_Breakfast.select().where(includes.Inc_Breakfast.InvoiceNo == inv_no):
                        try:
                            if food.BType == bftype:
                                bfrate = request.args.get('optradio2')
                                bfdes = request.args.get('description2')
                                review.Review.create_review(bfrate, bfdes, cid, inv_no)
                                SCounter = 2
                        except:
                            continue
                except:
                    continue
        elif revtype == '3':
            stype = request.args.get('stype')
            for q in res.Reservation.select().where(res.Reservation.CID == cid):
                try:
                    inv_no = q.InvoiceNo
                    for ser in includes.Cont_Service.select().where(includes.Cont_Service.InvoiceNo == inv_no):
                        try:
                            if ser.SType == stype:
                                srate = request.args.get('optradio3')
                                sdes = request.args.get('description3')
                                review.Review.create_review(srate, sdes, cid, inv_no)
                                SCounter = 3
                        except:
                            continue
                except:
                    continue
    except:
        traceback.print_exc(file=sys.stdout)
        flash("There was an error processing your request. Please try again", 'danger')
        return render_template('feedback/index.html', logged_in=True,role=role)
    if SCounter != 0:
        return render_template('feedback/success.html', logged_in=True, role=role)
    else:
        flash("error", 'danger')
        return render_template('feedback/index.html',logged_in=True, role=role)

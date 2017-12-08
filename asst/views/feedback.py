from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from itertools import *
from asst.models import hotel, room, breakfast, service,  res, review
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

@page.route('/',methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def feedback(role):
    return render_template('feedback/index.html', logged_in=True,role=role)

@page.route('/success',methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def rreview(role):
    Scounter = -1
    try:
        user = flask_login.current_user
        cid = user.CID
        revtype = request.args.get('res')
        if revtype == '1':
            roomtype = request.args.get('rtype')
            if res.Reservation.CID == cid:
                if room.Room.Type.where(room.Room.HotelID == res.Reservation.HotelID.where(res.Reservation.CID == cid)) == roomtype:
                    rrate = request.args.get('optradio1')
                    rdes = request.args.get('description')
                    review.review.create_review(rrate,rdes,cid)
                    Scounter = 1
        elif revtype == '2':
            bftype = request.args.get('bftype')
            if res.Reservation.CID == cid:
                if breakfast.Breakfast.BType.where(breakfast.Breakfast.HotelID == res.Reservation.HotelID.where(res.Reservation.CID == cid)) == bftype:
                    bfrate = request.args.get('optradio2')
                    bfdes = request.args.get('description2')
                    review.review.create_review(bfrate,bfdes,cid)
                    Scounter = 2
        elif revtype == '3':
            stype = request.args.get('stype')
            if res.Reservation.CID == cid:
                if service.Service.sType.where(service.Service.HotelID == res.Reservation.HotelID.where(res.Reservation.CID == cid)) == stype:
                    srate = request.args.get('optradio3')
                    sdes = request.args.get('description3')
                    review.review.create_review(srate,sdes,cid)
                    Scounter = 3
    except:
        traceback.print_exc(file=sys.stdout)
        flash("There was an error processing your request. Please try again", 'danger')
        return render_template('feedback/index.html', logged_in=True,role=role)
    if Scounter == 1:
        return render_template('feedback/success.html', logged_in=True, role=role)
    elif Scounter == 2:
        return render_template('feedback/success.html', logged_in=True, role=role)
    elif Scounter == 3:
        return render_template('feedback/success.html',logged_in=True,role=role)
    else:
        flash("The kind of reservation does not exist for this account. Please review only what you have reserved before",'danger')
        return render_template('feedback/index.html', logged_in=True,role=role)

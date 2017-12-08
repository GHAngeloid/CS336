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

@page.route("/",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def feedback(role):
    return render_template('feedback/index.html', logged_in=True,role=role)
@page.route("/one",methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def rreview(role):
    try:
        user = flask_login.current_user
        cid = user.CID
        revtype = request.args.get('res')
        if revtype == '1':
            roomtype = request.args.get('rtype')
            if res.Reservation.CID == cid and room.Room.Type.where(room.Room.HotelID == res.Reservation.HotelID.where(res.Reservation.CID == cid)) == roomtype:
                rrate = request.args.get('optradio1')
                rdes = request.args.get('description')
                review.review.create_review(rrate,rdes,cid)
            else:
                flash("No reservations of this room type were made by the user.", 'danger')
                return render_template('feedback/index.html', logged_in=True, role=role)
    except:
        traceback.print_exc(file=sys.stdout)
        flash("There was an error processing your request. Please try again", 'danger')
        return render_template('feedback/index.html', logged_in=True,role=role)
    return render_template('feedback/success.html', logged_in=True,role=role)

@page.route("/two", methods=['GET', 'POST'])
@require_role(['admin', 'manager', 'customer'],  getrole=True)  # Example of requireing a role(and authentication)
def bfreview(role):
    try:
        user = flask_login.current_user
        cid = user.CID
        revtype = request.args.get('res')
        if revtype == '2':
            bftype = request.args.get('bftype')
            if res.Reservation.CID == cid and breakfast.Breakfast.BType.where(breakfast.Breakfast.HotelID == res.Reservation.HotelID.where(res.Reservation.CID == cid)) == bftype:
                bfrate = request.args.get('optradio2')
                bfdes = request.args.get('description2')
                review.review.create_review(bfrate,bfdes,cid)
            else:
                flash("This breakfast type was not ordered by user.", 'danger')
                return render_template('feedback/index.html', logged_in=True, role=role)
    except:
        traceback.print_exc(file=sys.stdout)
        flash("There was an error processing your request. Please try again", 'danger')
        return render_template('feedback/index.html', logged_in=True,role=role)
    return render_template('feedback/success.html', logged_in=True,role=role)
@page.route("/two", methods=['GET', 'POST'])
@require_role(['admin', 'manager', 'customer'],  getrole=True)  # Example of requireing a role(and authentication)
def sreview(role):
    try:
        user = flask_login.current_user
        cid = user.CID
        revtype = request.args.get('res')
        if revtype == '3':
            stype = request.args.get('stype')
            if res.Reservation.CID == cid and service.Service.sType.where(service.Service.HotelID == res.Reservation.HotelID.where(res.Reservation.CID == cid)) == stype:
                srate = request.args.get('optradio3')
                sdes = request.args.get('description3')
                review.review.create_review(srate,sdes,cid)
            else:
                flash("This service was not ordered by the user.", 'danger')
                return render_template('feedback/index.html', logged_in=True,role=role)
    except:
        traceback.print_exc(file=sys.stdout)
        flash("There was an error processing your request. Please try again", 'danger')
        return render_template('feedback/index.html', logged_in=True,role=role)
    return render_template('feedback/success.html', logged_in=True,role=role)

from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from asst.models import res, user, room
from itertools import *
import traceback, sys
import math
import random
import json
import time

import datetime

# indicator that when starting up the site, it initializes every file, including possible global variables
#print("TEST")

class reser:
    date1=datetime.date(2015, 1, 1)
    date2=datetime.date(2018, 4, 5)
    spent = 0
    egg=0
    bacon= 0
    sandwich=0
    cleaning = 0

r1= reser()
r2 = reser()
r2.date1= datetime.date(2016, 6, 7)




'''
x=tst1.date2-tst1.date1
y=x.days*2
'''



page = Blueprint('stats', __name__, template_folder='templates')

@page.route("/",methods=['GET'])
@require_role(['admin','manager'],getrole=True) # Example of requireing a role(and authentication)
def stats(role):
    return render_template('stats/index.html', logged_in=True,role=role)



@page.route('/stat_list',methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def result(role):
    if request.method == 'POST':
        result = request.form['res']
        dateB = request.form['dateB']
        dateE = request.form['dateE']
        print(result)
        print(dateB)
        print(dateE)
        test=[]
        if result == 'Highest Rated Room Type':
            #res.Reservation.InDate
            #res.Reservation.OutDate
            try:
                #data = request.get_json()
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB, res.Reservation.OutDate <= dateE):
                    test.append([r.InDate, r.OutDate])
                print(test)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(1)
            # need Room_no and HotelID to access Room data
            # need review.py
        if result == '5 Best Customers':
            try:
                print(" ")
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(2)
            # need CID of Customer to access User data
            # goes by costs
        if result == 'Highest Rated Breakfast':
            try:
                print(" ")
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(3)
            # need bType and HotelID to access breakfast data
            # need review.py
        if result == 'Highest Rated Service':
            try:
                print(" ")
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(4)
            # need sType and HotelID to access Service data
            # need review.py

        # might need a try/except when fetching for dates
        # idea: for each result, have the result page include a list. this result page is called stat_list.html
        # question, how am i fetching review data???
    return render_template('stats/stat_list.html', logged_in=True,role=role)

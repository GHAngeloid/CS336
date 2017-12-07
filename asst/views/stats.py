from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from asst.models import res, user, room, review
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
        #print(dateB)
        #print(dateE)
        test=[]
        if result == 'Highest Rated Room Type':
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB, res.Reservation.OutDate <= dateE):
                    temp = r.CID
                    test.append([r.InDate, r.OutDate, temp])
                    #print(temp)
                    for s in review.review.select().where(review.review.CID == temp):
                        # Anthony, how the heck did you forget parentheses on IntegerFields?????
                        print(s.ReviewID, s.Rating, s.TextComment)
                        # prints every single review from given CID

                        #print(review.review.CID)
                #review.Review.CID
                #review.Review.Rating
                #review.Review.TextComment

                print(test)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(1)
            # need Room_no and HotelID to access Room data
            # need review.py
            # must access ONLY Room Reviews
            # Status: Incomplete
        if result == '5 Best Customers':
            try:
                CIDArray = []
                TotalAmountArray = []
                i = 0
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB, res.Reservation.OutDate <= dateE):
                    temp = r.CID
                    test.append([r.InDate, r.OutDate, temp, r.TotalAmt])
                    #print(temp, r.TotalAmt)

                    if r.CID in CIDArray:
                        key = CIDArray.index(r.CID)
                        TotalAmountArray[key] += r.TotalAmt
                    else:
                        CIDArray.append(r.CID)
                        TotalAmountArray.append(r.TotalAmt)
                        i += 1
                x = 0
                print(CIDArray, TotalAmountArray)
                sortedList = sorted(TotalAmountArray, reverse=True)
                i = 0  # sorted index
                newCIDArray = []
                #print(sortedList)
                while i < len(CIDArray):
                    j = 0  # unsorted index
                    while sortedList[i] != TotalAmountArray[j] and j < len(CIDArray):
                        j += 1
                    newCIDArray.append(CIDArray[j])
                    i += 1
                print(newCIDArray, sortedList)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(2)
            # need CID of Customer to access User data
            # goes by costs
            # need TotalAmt : DONE
            # Status: Incomplete
        if result == 'Highest Rated Breakfast':
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB, res.Reservation.OutDate <= dateE):
                    temp = r.CID
                    test.append([r.InDate, r.OutDate, temp])
                    #print(temp)
                    for s in review.review.select().where(review.review.CID == temp):
                        print(s.ReviewID, s.Rating, s.TextComment)
                        # prints every single review from given CID
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(3)
            # need bType and HotelID to access breakfast data
            # need review.py
            # must access ONLY Breakfast Reviews
            # Status: Incomplete
        if result == 'Highest Rated Service':
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB, res.Reservation.OutDate <= dateE):
                    temp = r.CID
                    test.append([r.InDate, r.OutDate, temp])
                    #print(temp)
                    for s in review.review.select().where(review.review.CID == temp):
                        # Anthony, how the heck did you forget parentheses on IntegerFields?????
                        print(s.ReviewID, s.Rating, s.TextComment)


                        # prints every single review from given CID
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(4)
            # need sType and HotelID to access Service data
            # need review.py
            # must access ONLY Service Reviews
            # Status: Incomplete

        # might need a try/except when fetching for dates
        # idea: for each result, have the result page include a list. this result page is called stat_list.html
        # question, how am i fetching review data???
    return render_template('stats/stat_list.html', logged_in=True,role=role)

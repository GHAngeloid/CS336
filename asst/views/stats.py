from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from asst.models import res, user, room, review, breakfastreview_asseses
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

    if request.method == 'GET':
        return render_template('stats/stat_list.html', logged_in=True, role=role)
    if request.method == 'POST':
        result = request.form['res']
        dateB = request.form['dateB']
        dateE = request.form['dateE']
        print(result)
        #print(dateB)
        #print(dateE)

        if result == 'Highest Rated Room Type':
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                and res.Reservation.OutDate <= dateE):

                    print(r.CID)
                    #for s in review.review.select().where(review.review.CID == temp):
                        # Anthony, how the heck did you forget parentheses on IntegerFields?????
                        #print(s.ReviewID, s.Rating, s.TextComment)
                        # prints every single review from given CID

                        #print(review.review.CID)
                #review.Review.CID
                #review.Review.Rating
                #review.Review.TextComment

                #print(test)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(1)
            # need Room_no and HotelID to access Room data
            # need review.py
            # must access ONLY Room Reviews
        if result == '5 Best Customers':
            try:
                CIDArray = []
                TotalAmountArray = []
                i = 0
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                and res.Reservation.OutDate <= dateE):
                    #print(temp, r.TotalAmt)

                    if r.CID in CIDArray:
                        key = CIDArray.index(r.CID)
                        TotalAmountArray[key] += r.TotalAmt
                    else:
                        CIDArray.append(r.CID)
                        TotalAmountArray.append(r.TotalAmt)
                        i += 1

                #print(CIDArray, TotalAmountArray)
                sortedList = sorted(TotalAmountArray, reverse=True)
                i = 0  # sorted index
                newCIDArray = []
                #print(sortedList)

                while i < len(CIDArray):
                    j = 0  # unsorted index
                    while sortedList[i] != TotalAmountArray[j] and j < len(CIDArray):
                        j += 1
                    newCIDArray.append(CIDArray[j])
                    if len(newCIDArray) == 5:
                        break
                    i += 1
                #print(newCIDArray, sortedList)

                i = 0
                name = []

                while i < len(newCIDArray):
                    for u in user.User.select().where(user.User.CID == newCIDArray[i]):
                        name.append(u.Name)
                    i += 1

                output = []
                for i in range(len(newCIDArray)):
                    output.append([name[i], '{:.2f}'.format(sortedList[i])])

                return render_template('stats/stat_list.html', logged_in=True, role=role, result=result,
                                       output=output)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            #print(2)
            # need CID of Customer to access User data
            # goes by costs
            # need TotalAmt : DONE
        if result == 'Highest Rated Breakfast':
            hotels = []
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                and res.Reservation.OutDate <= dateE):

                    if r.HotelID not in hotels:
                        hotels.append(r.HotelID)

                i = 0
                while i < len(hotels):  # iterates through each hotel
                    for b in breakfastreview_asseses.BreakfastReview_asseses.select().where(
                    breakfastreview_asseses.BreakfastReview_asseses.HotelID == hotels[i]):
                        print(b.ReviewID, b.BType)
                    i += 1


                    #print(temp)
                    #for s in review.review.select().where(review.review.CID == temp):
                        #print(s.ReviewID, s.Rating, s.TextComment)
                        # prints every single review from given CID
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(3)
            # need bType and HotelID to access breakfast data
            # need review.py
            # must access ONLY Breakfast Reviews
        if result == 'Highest Rated Service':
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                and res.Reservation.OutDate <= dateE):

                    print(r.CID)
                    #for s in review.review.select().where(review.review.CID == temp):
                        # Anthony, how the heck did you forget parentheses on IntegerFields?????
                        #print(s.ReviewID, s.Rating, s.TextComment)


                        # prints every single review from given CID
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500
            print(4)
            # need sType and HotelID to access Service data
            # need review.py
            # must access ONLY Service Reviews

        # might need a try/except when fetching for dates
        # idea: for each result, have the result page include a list. this result page is called stat_list.html
        # question, how am i fetching review data???
    return render_template('stats/stat_list.html', logged_in=True, role=role, result=result)

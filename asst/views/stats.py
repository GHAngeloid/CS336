from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from asst.models import res, user, room, review, breakfastreview_asseses, servicereview_rates, roomreview_evaluates
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

        # Highest Rated Room Type
        if result == 'Highest Rated Room Type':
            hotels = []
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                and res.Reservation.OutDate <= dateE):
                    if r.HotelID not in hotels:
                        hotels.append(r.HotelID)

                i = 0
                Room_no_list = []  # list of all room #s
                reviewcnt = []  # list that keeps track of sums of each room review
                k = 0
                while i < len(hotels):
                    for r in roomreview_evaluates.RoomReview_evaluates.select().where(
                    roomreview_evaluates.RoomReview_evaluates.HotelID == hotels[i]):
                        print("Review ID:", r.ReviewID, "Room_no:", r.Room_no)
                        if(r.Room_no not in Room_no_list):
                            Room_no_list.append(r.Room_no)
                            reviewcnt.append(1)
                            k += 1
                        #else:

                    i += 1

                for r in room.Room.select().where(
                room.Room.HotelID == hotels[0] and room.Room.Room_no == Room_no_list[0]):
                    print("Room Type:", r.Type)


                #print(test)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500

            # need Room_no and HotelID to access Room data
            # need review.py
            # must access ONLY Room Reviews

        # 5 Best Customers
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

            # need CID of Customer to access User data
            # goes by costs
            # need TotalAmt : DONE

        # Highest Rated Breakfast
        if result == 'Highest Rated Breakfast':
            hotels = []  # list of every hotel
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                and res.Reservation.OutDate <= dateE):
                    if r.HotelID not in hotels:
                        hotels.append(r.HotelID)

                i = 0
                btypes = []  # list of all breakfast types per hotel
                while i < len(hotels):  # iterates through each hotel
                    for b in breakfastreview_asseses.BreakfastReview_asseses.select().where(
                    breakfastreview_asseses.BreakfastReview_asseses.HotelID == hotels[i]):
                        print("Review ID:", b.ReviewID, "Breakfast Type:", b.BType)
                        if b.BType not in btypes:
                            btypes.append(b.BType)
                    i += 1



            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500

            # need bType and HotelID to access breakfast data
            # need review.py
            # must access ONLY Breakfast Reviews

        # Highest Rated Services
        if result == 'Highest Rated Service':
            hotels = []
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                and res.Reservation.OutDate <= dateE):
                    if r.HotelID not in hotels:
                        hotels.append(r.HotelID)

                i = 0
                servicetypes = []  # list of all service types per hotel
                while i < len(hotels):
                    for s in servicereview_rates.ServiceReview_rates.select().where(
                    servicereview_rates.ServiceReview_rates.HotelID == hotels[i]):
                        print("Review ID:", s.ReviewID, "Service Type:", s.sType)
                        if s.sType not in servicetypes:
                            servicetypes.append(s.sType)
                    i += 1



            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500

            # need sType and HotelID to access Service data
            # need review.py
            # must access ONLY Service Reviews

        # might need a try/except when fetching for dates
        # idea: for each result, have the result page include a list. this result page is called stat_list.html
        # question, how am i fetching review data???
    return render_template('stats/stat_list.html', logged_in=True, role=role, result=result)

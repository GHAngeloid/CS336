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
# print("TEST")

class reser:
    date1 = datetime.date(2015, 1, 1)
    date2 = datetime.date(2018, 4, 5)
    spent = 0
    egg = 0
    bacon = 0
    sandwich = 0
    cleaning = 0


r1 = reser()
r2 = reser()
r2.date1 = datetime.date(2016, 6, 7)

'''
x=tst1.date2-tst1.date1
y=x.days*2
'''

page = Blueprint('stats', __name__, template_folder='templates')


@page.route("/", methods=['GET'])
@require_role(['admin', 'manager'], getrole=True)  # Example of requireing a role(and authentication)
def stats(role):
    return render_template('stats/index.html', logged_in=True, role=role)


@page.route('/stat_list', methods=['GET', 'POST'])
@require_role(['admin', 'manager', 'customer'], getrole=True)  # Example of requireing a role(and authentication)
def result(role):
    if request.method == 'GET':
        return render_template('stats/stat_list.html', logged_in=True, role=role)
    if request.method == 'POST':
        result = request.form['res']
        dateB = request.form['dateB']
        dateE = request.form['dateE']
        print(result)
        # print(dateB)
        # print(dateE)

        # Highest Rated Room Type
        if result == 'Highest Rated Room Type':
            hotels = []
            cids = []
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                                                        and res.Reservation.OutDate <= dateE):
                    if r.HotelID not in hotels:
                        hotels.append(r.HotelID)
                    if r.CID not in cids:
                        cids.append(r.CID)

                i = 0
                reviewIDs = []
                while i < len(hotels):
                    for r in roomreview_evaluates.RoomReview_evaluates.select().where(
                            roomreview_evaluates.RoomReview_evaluates.HotelID == hotels[i]):
                        #print("Review ID:", r.ReviewID, "Room_no:", r.Room_no)
                        if r.ReviewID not in reviewIDs:
                            reviewIDs.append(r.ReviewID)
                    i += 1

                i = 0
                revID = []
                revR = []
                while i < len(reviewIDs):
                    for u in review.review.select().where(review.review.ReviewID == reviewIDs[i]):
                        revID.append(u.ReviewID)
                        revR.append(u.Rating)
                    i += 1

                single = []
                double = []
                i = 0
                #print(revID, revR)
                while i < len(revID):
                    for r in roomreview_evaluates.RoomReview_evaluates.select().where(
                            roomreview_evaluates.RoomReview_evaluates.ReviewID == revID[i]):
                        #print("Room #:", r.Room_no)
                        if room.Room.Room_no == r.Room_no:
                            if room.Room.Type == 'Single':
                                single.append(revR[i])
                            if room.Room.Type == 'Double':
                                double.append(revR[i])
                    i += 1

                s = 0
                d = 0
                if len(single) != 0:
                    s = sum(single)/len(single)
                if len(double) != 0:
                    d = sum(double)/len(double)

                sol = []
                sol.append(s)
                sol.append(d)

                sol2 = sorted(sol, reverse=True)
                #print(sol, sol2)

                output = 'hi'
                if sol2[0] == s:
                    output = 'Single'
                if sol2[0] == d:
                    output = 'Double'

                return render_template('stats/stat_var.html', logged_in=True, role=role, result=result,
                                       output=output)

                # print(test)
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
                    # print(temp, r.TotalAmt)

                    if r.CID in CIDArray:
                        key = CIDArray.index(r.CID)
                        TotalAmountArray[key] += r.TotalAmt
                    else:
                        CIDArray.append(r.CID)
                        TotalAmountArray.append(r.TotalAmt)
                        i += 1

                # print(CIDArray, TotalAmountArray)
                sortedList = sorted(TotalAmountArray, reverse=True)
                i = 0  # sorted index
                newCIDArray = []
                # print(sortedList)

                while i < len(CIDArray):
                    j = 0  # unsorted index
                    while sortedList[i] != TotalAmountArray[j] and j < len(CIDArray):
                        j += 1
                    newCIDArray.append(CIDArray[j])
                    if len(newCIDArray) == 5:
                        break
                    i += 1
                # print(newCIDArray, sortedList)

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
            cids = []
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                                                        and res.Reservation.OutDate <= dateE):
                    if r.HotelID not in hotels:
                        hotels.append(r.HotelID)
                    if r.CID not in cids:
                        cids.append(r.CID)

                i = 0
                reviewIDs = []  # list of all breakfast types per hotel
                while i < len(hotels):  # iterates through each hotel
                    for b in breakfastreview_asseses.BreakfastReview_asseses.select().where(
                            breakfastreview_asseses.BreakfastReview_asseses.HotelID == hotels[i]):
                        #  print("Review ID:", b.ReviewID, "Breakfast Type:", b.BType)
                        if b.ReviewID not in reviewIDs:
                            reviewIDs.append(b.ReviewID)
                    i += 1

                # print(reviewIDs)
                #find

                revID = []
                revR = []
                i = 0
                while i < len(reviewIDs):
                    for u in review.review.select().where(review.review.ReviewID == reviewIDs[i]):
                        revID.append(u.ReviewID)
                        revR.append(u.Rating)
                    i += 1

                af = []
                bf = []
                cf = []
                mf = []
                i = 0
                while i < len(revID):
                    for m in breakfastreview_asseses.BreakfastReview_asseses.select().where(
                            breakfastreview_asseses.BreakfastReview_asseses.ReviewID == revID[i]):
                        if m.BType == "Bengali":
                            bf.append(revR[i])
                        if m.BType == "American":
                            af.append(revR[i])
                        if m.BType == "Chinese":
                            cf.append(revR[i])
                        if m.BType == "Mexican":
                            mf.append(revR[i])
                    i += 1

                a = 0
                b = 0
                c = 0
                m = 0
                if len(af) != 0:
                    a = sum(af)/len(af)

                if len(bf) != 0:
                    b = sum(bf)/len(bf)

                if len(cf) != 0:
                    c = sum(cf)/len(cf)

                if len(mf) != 0:
                    m = sum(mf)/len(mf)

                sol = []
                sol.append(a)
                sol.append(b)
                sol.append(c)
                sol.append(m)

                sol2 = sorted(sol, reverse=True)
                #print(sol, sol2)

                output = 'hi'

                if sol2[0] == a:
                    output = 'American'

                if sol2[0] == b:
                    output = 'Bengali'

                if sol2[0] == c:
                    output = 'Chinese'

                if sol2[0] == m:
                    output = 'Mexican'

                return render_template('stats/stat_var.html', logged_in=True, role=role, result=result,
                                       output=output)

            # qq

            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return "Error", 500

            # need bType and HotelID to access breakfast data
            # need review.py
            # must access ONLY Breakfast Reviews

        # Highest Rated Services
        if result == 'Highest Rated Service':

            hotels = []  # list of every hotel
            cids = []
            try:
                for r in res.Reservation.select().where(res.Reservation.InDate >= dateB
                                                        and res.Reservation.OutDate <= dateE):
                    if r.HotelID not in hotels:
                        hotels.append(r.HotelID)
                    if r.CID not in cids:
                        cids.append(r.CID)

                i = 0
                reviewIDs = []  # list of all breakfast types per hotel
                while i < len(hotels):  # iterates through each hotel
                    for b in servicereview_rates.ServiceReview_rates.select().where(
                            servicereview_rates.ServiceReview_rates.HotelID == hotels[i]):
                        #  print("Review ID:", b.ReviewID, "Breakfast Type:", b.BType)
                        if b.ReviewID not in reviewIDs:
                            reviewIDs.append(b.ReviewID)
                    i += 1

                revID = []
                revR = []
                i = 0
                while i < len(reviewIDs):
                    for u in review.review.select().where(review.review.ReviewID == reviewIDs[i]):
                        revID.append(u.ReviewID)
                        revR.append(u.Rating)
                    i += 1

                cl = []
                la = []
                wi = []

                i = 0
                while i < len(revID):
                    for m in servicereview_rates.ServiceReview_rates.select().where(
                            servicereview_rates.ServiceReview_rates.ReviewID == revID[i]):
                        if m.sType == "cleaning":
                            cl.append(revR[i])
                        if m.sType == "laundry":
                            la.append(revR[i])
                        if m.sType == "wifi":
                            wi.append(revR[i])

                    i += 1

               # print(cl, la, wi)
                c = 0
                l = 0
                w = 0

                if len(cl) != 0:
                    c = sum(cl)/len(cl)

                if len(la) != 0:
                    l = sum(la)/len(la)

                if len(wi) != 0:
                    w = sum(wi)/len(wi)


                sol = []
                sol.append(c)
                sol.append(l)
                sol.append(w)


                sol2 = sorted(sol, reverse=True)
                #print(sol, sol2)

                output = 'hi'

                if sol2[0] == c:
                    output = 'Cleaning'

                if sol2[0] == l:
                    output = 'Laundry'

                if sol2[0] == w:
                    output = 'Wifi'

                return render_template('stats/stat_var.html', logged_in=True, role=role, result=result,
                                       output=output)

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

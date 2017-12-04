from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from itertools import *
import traceback
import math
import random
import json
import time

import datetime

print("TEST")

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



@page.route('/result',methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def result(role):
    if request.method == 'POST':
        res = request.form['res']
        dateB = request.form['dateB']
        dateE = request.form['dateE']
        print(res)
        print(dateB)
        print(dateE)
        if res == 'Highest Rated Room Type':
            print(1)
        if res == '5 Best Customers':
            print(2)
        if res == 'Highest Rated Breakfast':
            print(3)
        if res == 'Highest Rated Service':
            print(4)
    return render_template('stats/index.html', logged_in=True,role=role)

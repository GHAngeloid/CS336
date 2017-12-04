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



@page.route('/number1',methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def number1(role):
    if request.method == 'POST':
       dateB = request.form['dateB']
       dateE = request.form['dateE']

    return render_template('reservation/index.html', logged_in=True,role=role)

def number1_ex(dateB,dateE):
   x=8


@page.route('/number2',methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def number2(role):
    if request.method == 'POST':
       dateB2 = request.form['dateB2']
       dateE2 = request.form['dateE2']

    return render_template('reservation/index.html', logged_in=True,role=role)

@page.route('/number3',methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def number3(role):
    if request.method == 'POST':
       dateB3 = request.form['dateB3']
       dateE3 = request.form['dateE3']

    return render_template('reservation/index.html', logged_in=True,role=role)

@page.route('/number4',methods=['GET','POST'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def number4(role):
    if request.method == 'POST':
       dateB4 = request.form['dateB4']
       dateE4 = request.form['dateE4']

    return render_template('reservation/index.html', logged_in=True,role=role)
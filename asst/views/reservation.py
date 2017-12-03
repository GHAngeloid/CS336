from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from itertools import *
import traceback
import math
import random
import json
import time

page = Blueprint('reservation', __name__, template_folder='templates')

@page.route("/",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def reservation(role):
    return render_template('reservation/index.html', logged_in=True,role=role)
import datetime
class Hotel:
    Country = 'America'#default america
    State= 'NJ'


class Room(Hotel):
    #manually add in service later Room.services = 'clean'
    rType='single' # single,double,deluxe,suite
    date1 = datetime.date.today()
    date2 = datetime.date(2018, 1, 14)
    eggs=0
    orangeJuice=0
    bacon=0


'''
x=tst1.date2-tst1.date1
y=x.days*2
'''
'''
5 hotels 3 in america-NJ,NY,FL-  2 in canada -ON,QC-
'''

H1R1 = Room()

H1R2 = Room()
H1R2.state='NY'

H1R3 = Room()
H1R3.state='FL'

H2R1 = Room()
H1R2.state='ON'
H2R1.Country='Canada'

H2R2 = Room()
H2R2.state='QC'
H2R2.Country='Canada'






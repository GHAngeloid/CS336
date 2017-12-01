from flask import Blueprint, render_template, abort, flash
from flask import request
from itertools import *
from asst import DB as db
from asst.models import user
import sys, traceback
import math
import random
import json
import time

page = Blueprint('main', __name__, template_folder='templates')


def connect_to_db():
    """Connect to the database before each request."""
    try:
        db.connect()
        flash('Connected to db', 'success')
    except:
        traceback.print_exc(file=sys.stdout)
        flash('Cannot connect to database', 'danger')
        pass

@page.route("",methods=['POST'])
def register():
    connect_to_db()
    try:
        print(request.form['phone'])
        cust = user.User.create_user(
                name=request.form['name'],
                password=request.form['password'],
                email=request.form['email'],
                phone_no = request.form['phone'],
                address = request.form['address'],
                role = request.form['role']
            )
        db.close()
    except:
        traceback.print_exc(file=sys.stdout)
        flash('Form failed', 'danger')
    # user = User.create(
    #         username=request.form['username'],
    #         password=md5(request.form['password']).hexdigest(),
    #         email=request.form['email'],
    #         join_date=datetime.datetime.now()
    #     )
    return render_template('/index.html')
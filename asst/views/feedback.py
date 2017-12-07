from flask import Blueprint, render_template, abort, flash
from flask import request
from asst.auth import require_role
from itertools import *
from asst import DB as db
from asst.models import user
import sys,traceback
import math
import random
import json
import time

page = Blueprint('feedback', __name__, template_folder='templates')

@page.route("/",methods=['GET'])
@require_role(['admin','manager', 'customer'],getrole=True) # Example of requireing a role(and authentication)
def feedback(role):
    return render_template('feedback/index.html', logged_in=True,role=role)
def connect_to_db():
    """Connect to the database before each request."""
    try:
        db.connect()
        flash('Connected to db', 'success')
    except:
        traceback.print_exc(file=sys.stdout)
        flash('Cannot connect to database', 'danger')
        pass

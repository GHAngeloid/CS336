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
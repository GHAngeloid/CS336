from flask import Blueprint, render_template, abort, flash
from flask import request
from itertools import *
import traceback
import math
import random
import json
import time

page = Blueprint('main', __name__, template_folder='templates')

@page.route("/",methods=['GET'])
def showhello():
    return render_template('/index.html')
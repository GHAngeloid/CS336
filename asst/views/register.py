from flask import Blueprint, render_template, abort, flash
from flask import request
from itertools import *
from asst import DB as db
from asst.models import user
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import BooleanField, StringField, PasswordField, validators, IntegerField, SelectField
from wtforms_alchemy import PhoneNumberField
import sys, traceback
import math
import random
import json
import time

page = Blueprint('register', __name__, template_folder='templates')


def connect_to_db():
    """Connect to the database before each request."""
    try:
        db.connect()
        flash('Connected to db', 'success')
    except:
        traceback.print_exc(file=sys.stdout)
        flash('Cannot connect to database', 'danger')
        pass

class RegistrationForm(FlaskForm):
    '''
    This is the form that displays fields to make a reservation
    '''
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    name = StringField('Name', [validators.DataRequired()])
    phone = PhoneNumberField('Phone Number',[validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=2, max=250),validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    role = SelectField('Role',  [validators.DataRequired()], choices=[('customer', 'Customer'), ('manager', 'Manager'), ('admin', 'Administrator')])
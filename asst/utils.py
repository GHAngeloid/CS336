from flask import flash
from asst import DB as db
import sys, traceback



def connect_to_db():
    """Connect to the database before each request."""
    try:
        db.connect()
    except:
        traceback.print_exc(file=sys.stdout)
        flash('Cannot connect to database', 'danger')
        pass
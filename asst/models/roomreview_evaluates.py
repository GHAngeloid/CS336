'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, FloatField, CompositeKey
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class RoomReview_evaluates(UserMixin, BaseModel):
    class Meta:
        db_table = 'RoomReview_evaluates'
    '''A User model for who will be using the software. Users have different levels of access with different roles

    Current active roles:

        - customer
        - manager
    '''
    ReviewID = IntegerField(primary_key=True)
    Room_no = IntegerField()
    HotelID = IntegerField()
